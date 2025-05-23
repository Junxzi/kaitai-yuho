import requests
from datetime import datetime, timedelta
from pathlib import Path
import time
import json
import os

import pandas as pd
from tqdm import tqdm
import urllib
from dotenv import load_dotenv

from src.config import API_KEY

# .envからAPIキーを読み込む
load_dotenv()
API_KEY = os.getenv("EDINET_API_KEY")

# EDINET書類リスト取得関数
def fetch_document_list(date, save_path=None):
    url = "https://api.edinet-fsa.go.jp/api/v2/documents.json"
    params = {"date": date, "type": 2, "Subscription-Key": API_KEY}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ {date}: status {response.status_code}")
            return None

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            print(f"❌ {date}: Content-Type not JSON → {content_type}")
            print(response.text[:300])
            return None

        data = response.json()
        if save_path:
            with open(save_path, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return data

    except Exception as e:
        print(f"💥 {date}: {e}")
        return None
    

# EDINET書類のZIPをダウンロードする関数
def download_document_zip(doc_id: str, save_dir: str = "../data/raw_reports") -> bool:
    url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{doc_id}"
    params = {"type": 1, "Subscription-Key": API_KEY}
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, f"{doc_id}.zip"), "wb") as f:
            f.write(response.content)
        print(f"✅ {doc_id} downloaded")
        return True
    else:
        print(f"Failed to download {doc_id}: {response.status_code}")
        return False
    

# 全社・全日付ループダウンロード処理
def fetch_all_yuho_documents(doc_list_csv="data/processed/yuho_doc_list.csv",
                             save_dir="data/raw_reports",
                             log_path="logs/download_errors.txt",
                             max_retries=3):
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    df = pd.read_csv(doc_list_csv)
    doc_ids = df["docID"].unique().tolist()

    downloaded_files = set([
        f.replace(".zip", "") for f in os.listdir(save_dir)
        if f.endswith(".zip")
    ])

    with open(log_path, "a") as logf:
        for doc_id in tqdm(doc_ids, desc="⬇️ Downloading Yuho ZIPs", ncols=100):
            if doc_id in downloaded_files:
                continue

            success = False
            url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{doc_id}?type=5&Subscription-Key={API_KEY}"
            output_path = os.path.join(save_dir, f"{doc_id}.zip")

            for attempt in range(1, max_retries + 1):
                try:
                    with urllib.request.urlopen(url) as res:
                        content = res.read()
                    with open(output_path, 'wb') as f:
                        f.write(content)
                    success = True
                    break
                except urllib.error.HTTPError as e:
                    if e.code >= 400:
                        logf.write(f"{doc_id}\tHTTP {e.code}: {e.reason}\n")
                        break
                    else:
                        time.sleep(1)
                except Exception as e:
                    logf.write(f"{doc_id}\tUnexpected: {str(e)}\n")
                    time.sleep(1)

            if not success:
                logf.write(f"{doc_id}\tFailed after {max_retries} retries\n")


def fetch_all_yuho_documents(
    start: str,
    end: str,
    edinet_codes_csv: str,
    save_path: str,
    log_path: str,
    max_retries: int = 3,
    sleep: float = 1.0
):
    BASE_URL = "https://api.edinet-fsa.go.jp/api/v2/documents.json"
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    edinet_df = pd.read_csv(edinet_codes_csv)
    target_edinet_codes = edinet_df["ＥＤＩＮＥＴコード"].dropna().astype(str).unique().tolist()

    save_path = Path(save_path)
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if save_path.exists():
        existing_df = pd.read_csv(save_path)
        collected_doc_ids = set(existing_df["docID"])
        results = existing_df.to_dict(orient="records")
    else:
        collected_doc_ids = set()
        results = []

    log_file = open(log_path, "a")

    def log(msg):
        print(msg)
        log_file.write(msg + "\n")
        log_file.flush()

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        for attempt in range(1, max_retries + 1):
            try:
                params = {
                    "date": date_str,
                    "type": 2,
                    "Subscription-Key": API_KEY
                }
                response = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
                if response.status_code != 200:
                    raise Exception(f"Status {response.status_code}")

                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    raise Exception(f"Invalid Content-Type: {content_type}")

                data = response.json()

                added = 0
                for doc in data.get("results", []):
                    if (
                        doc.get("docTypeCode") == "120"
                        and doc.get("edinetCode") in target_edinet_codes
                        and doc.get("docID") not in collected_doc_ids
                    ):
                        results.append({
                            "docID": doc["docID"],
                            "date": date_str,
                            "edinetCode": doc.get("edinetCode"),
                            "secCode": doc.get("secCode", ""),
                            "filerName": doc.get("filerName", "")
                        })
                        collected_doc_ids.add(doc["docID"])
                        added += 1
                if added != 0:
                    log(f"✅ {date_str}: {added} 件追加")
                break

            except Exception as e:
                if attempt < max_retries:
                    log(f"⚠️  {date_str}: 試行 {attempt} 回目に失敗: {e}（再試行）")
                    time.sleep(2)
                else:
                    log(f"❌ {date_str}: 最大試行回数に達しました: {e}")
        current_date += timedelta(days=1)
        time.sleep(sleep)
        pd.DataFrame(results).to_csv(save_path, index=False)

    log("Process Complete")
    log_file.close()