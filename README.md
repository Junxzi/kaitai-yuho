# 日経225銘柄 事業リスクの時系列分析とLLMによる要約

## 概要 (Overview)

本プロジェクトは、日経225銘柄の2018年から2024年までの有価証券報告書「事業等のリスク」セクションを分析し、企業が認識しているリスクの主要なテーマとその時系列での変遷を明らかにすることを目的としています。  
テキストクラスタリングと、ローカルで動作する大規模言語モデル (LLM) による要約技術を組み合わせることで、膨大な非構造化データから効率的に洞察を抽出します。

---

## プロジェクトの目的 (Project Goals)

- 日経225銘柄が認識する事業リスクの主要なカテゴリを特定する。
- 2018年から2024年という期間におけるリスク認識のトレンドと変化を分析する。
- パンデミック、地政学的緊張、AIの台頭などの外部環境変化が企業のリスク認識に与えた影響を考察する。
- `llama.cpp` を活用したローカルLLM推論環境と `LlamaIndex` を組み合わせ、テキスト分析パイプラインの有効性を検証する。

---

## 使用技術 (Technologies Used)

### 主要なライブラリとツール

- **Python**: データ処理とスクリプト実行の基盤言語  
- **llama.cpp**: ローカルGPU (CUDA) 上で GGUF 形式モデルを推論する高速C++ライブラリ  
- **Llama 3 ELYZA JP 8B (GGUF q4_k_m)**: 日本語に特化した大規模言語モデル  
- **LlamaIndex**: Retrieval Augmented Generation (RAG) パイプライン構築フレームワーク  
- **HuggingFace `pkshatech/RoSEtta-base`**: 埋め込み生成用日本語モデル  
- **SentenceTransformerRerank `hotchpotch/japanese-reranker-cross-encoder-base-v1`**: 検索結果のリランク用  
- **FAISS (`faiss-gpu`)**: ベクトル検索用インデックス構築ライブラリ  
- **Pandas**: データフレーム操作と管理  
- **JSON**: 要約結果の出力形式  
- **WSL2**: Windows上のLinux環境およびGPUアクセラレーション用  

---

## 動作環境 (Environment)

- **OS**: Ubuntu on WSL2  
- **GPU**: NVIDIA GeForce RTX 4060 Ti (VRAM 8GB)  
- **CUDA Toolkit**: 12.0（または互換バージョン）  
- **Python**: 3.12.3  
- **仮想環境**: `venv`

---

## ライセンス (License)

MIT License

---

## 連絡先 (Contact)

junish826@gmail.com
