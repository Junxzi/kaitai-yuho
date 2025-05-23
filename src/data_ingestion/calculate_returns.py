import pandas as pd
import os
from typing import List

def calculate_one_year_return(tickers: List[str], price_dir: str = "data/stock_data", 
                               start_date: str = "2022-06-30", end_date: str = "2023-06-30") -> pd.DataFrame:
    """
    指定されたティッカーの株価データから1年リターンを計算し、DataFrameで返す。

    Parameters:
        tickers (List[str]): ティッカーリスト（例: ['6758.T', '7203.T']）
        price_dir (str): 株価CSVファイルの保存ディレクトリ
        start_date (str): 開始日（例: '2022-06-30'）
        end_date (str): 終了日（例: '2023-06-30'）

    Returns:
        pd.DataFrame: {ticker, return_2022_2023} のDataFrame
    """
    results = []

    for ticker in tickers:
        code = ticker.replace(".T", "")
        path = os.path.join(price_dir, f"{code}.csv")
        if not os.path.exists(path):
            print(f"[!] Missing: {path}")
            continue

        try:
            df = pd.read_csv(path, parse_dates=["Date"])
            df.set_index("Date", inplace=True)
            
            price_start = df.loc[start_date, "Close"] if start_date in df.index else None
            price_end = df.loc[end_date, "Close"] if end_date in df.index else None

            if price_start and price_end:
                ret = (price_end - price_start) / price_start
                results.append({"ticker": ticker, "return_2022_2023": ret})
            else:
                print(f"[!] Price missing for {ticker} at {start_date} or {end_date}")
        except Exception as e:
            print(f"[x] Error with {ticker}: {e}")

    return pd.DataFrame(results)