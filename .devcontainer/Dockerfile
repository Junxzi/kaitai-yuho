FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# 作業ディレクトリ
WORKDIR /app

# システムパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3.10-dev \
    build-essential curl git unzip libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# pip を最新にして依存をインストール（.venv を有効化して実行）
COPY requirements.txt .

# 例
RUN python3 -m venv /app/.venv \
    && . /app/.venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install ipykernel


# Jupyter 起動用スクリプト（.venv の python で起動）
CMD ["/app/.venv/bin/jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
