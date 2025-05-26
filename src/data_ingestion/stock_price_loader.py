import yfinance as yf
import os
import pandas as pd
from typing import List
from tqdm import tqdm

def download_stock_prices(tickers: List[str], start_date: str, end_date: str, interval: str = "1mo", output_dir: str = "data/stock_data"):
    """
    指定したティッカーの株価データを yfinance から取得し、CSV として保存する。

    Parameters:
        tickers (List[str]): 取得対象のティッカー一覧（例: ['6758.T', '7203.T']）
        start_date (str): 取得開始日（例: '2020-01-01'）
        end_date (str): 取得終了日（例: '2024-12-31'）
        interval (str): データ間隔（例: '1d', '1wk', '1mo'）
        output_dir (str): 保存先ディレクトリ
    """
    os.makedirs(output_dir, exist_ok=True)

    for ticker in tqdm(tickers, desc="Downloading stock data"):
        try:
            df = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
            if df.empty:
                continue
            df.to_csv(os.path.join(output_dir, f"{ticker.replace('.T', '')}.csv"))
        except Exception:
            continue