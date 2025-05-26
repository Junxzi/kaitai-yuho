import pandas as pd
import os
from typing import List, Tuple, Dict

def calculate_annual_return(
    ticker: str, 
    price_dir: str = "data/stock_prices",
    year_start: int = 2022
) -> Tuple[str, float]:
    """
    1年ごとの株価リターンを計算

    Parameters:
        ticker (str): 銘柄コード（例：'6758.T'）
        price_dir (str): 株価CSVファイルの保存先
        year_start (int): 比較開始の年（例：2022 → 2022-06-30 〜 2023-06-30）

    Returns:
        (ticker, return) のタプル
    """
    code = ticker.replace(".T", "")
    path = os.path.join(price_dir, f"{code}.csv")

    try:
        df = pd.read_csv(path, header=None)
        df.columns = df.iloc[0]  # 1行目を列名にする（0行目は列名、1行目は空行）
        df = df[2:]  # 実データ開始

        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        df = df.astype(float, errors="ignore")

        start_date = pd.to_datetime(f"{year_start}-06-30")
        end_date = pd.to_datetime(f"{year_start+1}-06-30")

        price_start = df.loc[start_date, "Close"] if start_date in df.index else None
        price_end = df.loc[end_date, "Close"] if end_date in df.index else None

        if price_start and price_end:
            ret = (price_end - price_start) / price_start
            return ticker, ret
        else:
            return ticker, None
    except:
        return ticker, None

def batch_calculate_returns(
    tickers: List[str],
    price_dir: str,
    year_start: int
) -> pd.DataFrame:
    """
    複数銘柄の1年リターンをまとめて計算し、DataFrameで返す。

    Returns:
        pd.DataFrame: {ticker, return_YYYY_YYYY} の形式
    """
    results = []
    for ticker in tickers:
        code, ret = calculate_annual_return(ticker, price_dir, year_start)
        results.append({
            "ticker": code,
            f"return_{year_start}_{year_start+1}": ret
        })
    return pd.DataFrame(results)