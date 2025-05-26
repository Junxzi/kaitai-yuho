import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

import pandas as pd

def parse_risk_section_from_all_xml(
    doc_id,
    extract_dir="data/extracted_reports",
    save_dir="data/parsed_sections",
    log_path="logs/risk_extract_errors.txt"
):
    """
    解凍済みXBRLフォルダ内のすべてのXMLファイルから「事業等のリスク」セクションを抽出する。
    成功すれば .txt に保存。失敗ログはファイルにのみ記録。
    """
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)  # ← これが重要！

    xbrl_dir = os.path.join(extract_dir, doc_id)
    if not os.path.exists(xbrl_dir):
        with open(log_path, "a") as f:
            f.write(f"[{doc_id}] 解凍ディレクトリが見つかりません: {xbrl_dir}\n")
        return None

    ns = {"jpcrp": "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-01-01"}
    candidate_tags = ["BusinessRisks", "BusinessRisk"]

    xml_files = []
    for root, _, files in os.walk(xbrl_dir):
        for file in files:
            if file.endswith(".xbrl") and "jpcrp" in file:
                xml_files.append(os.path.join(root, file))

    for path in tqdm(xml_files, desc=f"🔍 {doc_id} 内XML探索", ncols=100, leave=False):
        try:
            tree = ET.parse(path)
            root_el = tree.getroot()
            for tag in candidate_tags:
                el = root_el.find(f".//jpcrp:{tag}", ns)
                if el is not None and el.text:
                    out_path = os.path.join(save_dir, f"{doc_id}.txt")
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(el.text.strip())
                    return el.text.strip()
        except Exception as e:
            with open(log_path, "a") as f:
                f.write(f"[{doc_id}] XML parse error: {path} - {e}\n")

    with open(log_path, "a") as f:
        f.write(f"[{doc_id}] リスク文が見つかりませんでした\n")

    return None


def extract_risk_from_all_csvs(
    extract_dir="data/extracted_reports",
    save_dir="data/parsed_sections_csv",
    log_path="logs/risk_extract_errors.txt"
):
    """
    解凍済みの XBRL_TO_CSV フォルダから「事業等のリスク」セクションを抽出し、CSVで保存。
    """
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    doc_ids = sorted(os.listdir(extract_dir))
    success, skipped, failed = 0, 0, 0

    for doc_id in tqdm(doc_ids, desc="🧠 Extracting Risk CSVs", ncols=100):
        out_path = os.path.join(save_dir, f"{doc_id}.csv")
        if os.path.exists(out_path):
            skipped += 1
            continue

        xbrl_csv_dir = os.path.join(extract_dir, doc_id, "XBRL_TO_CSV")
        if not os.path.exists(xbrl_csv_dir):
            failed += 1
            with open(log_path, "a") as f:
                f.write(f"[{doc_id}] ❌ XBRL_TO_CSV ディレクトリが見つかりません\n")
            continue

        csv_files = [f for f in os.listdir(xbrl_csv_dir) if f.startswith("jpcrp") and f.endswith(".csv")]
        if not csv_files:
            failed += 1
            with open(log_path, "a") as f:
                f.write(f"[{doc_id}] ❌ jpcrp*.csv が見つかりません\n")
            continue

        try:
            path = os.path.join(xbrl_csv_dir, csv_files[0])
            df = pd.read_csv(path, encoding="utf-16", sep="\t")
            risk_df = df[df["項目名"].str.contains("事業等のリスク", na=False)]

            if not risk_df.empty:
                risk_df.to_csv(out_path, index=False)
                success += 1
            else:
                failed += 1
                with open(log_path, "a") as f:
                    f.write(f"[{doc_id}] ⚠️ リスク項目が見つかりませんでした\n")
        except Exception as e:
            failed += 1
            with open(log_path, "a") as f:
                f.write(f"[{doc_id}] ⚠️ 読み込みエラー: {e}\n")

    print(f"\n✅ 完了: {success} 件抽出, {skipped} 件スキップ, {failed} 件失敗")