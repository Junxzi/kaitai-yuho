import os
import pandas as pd

def aggregate_risk_texts(doc_csv_path="data/processed/yuho_doc_list.csv",
                         risk_dir="data/parsed_sections_csv",
                         output_csv_path="data/risk_dataset.csv"):
    """
    メタ情報CSVと、リスクCSV群を統合し、1レコード＝1有報のDataFrameに変換。
    """
    doc_df = pd.read_csv(doc_csv_path)
    risk_rows = []

    for doc_id in doc_df["docID"]:
        path = os.path.join(risk_dir, f"{doc_id}.csv")
        if os.path.exists(path):
            try:
                risk_df = pd.read_csv(path, encoding="utf-8")
                text = risk_df["値"].dropna().astype(str).str.cat(sep="\n")
            except Exception as e:
                text = f"（読み込み失敗: {e}）"
        else:
            text = "（記載なし or 抽出失敗）"

        risk_rows.append({"docID": doc_id, "【事業等のリスク】": text})

    risk_df_all = pd.DataFrame(risk_rows)
    merged_df = pd.merge(doc_df, risk_df_all, on="docID", how="left")
    merged_df.to_csv(output_csv_path, index=False)
    return merged_df