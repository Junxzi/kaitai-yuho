日経225銘柄 事業リスクの時系列分析とLLMによる要約
概要 (Overview)
本プロジェクトは、日経225銘柄の2018年から2024年までの有価証券報告書「事業等のリスク」セクションを分析し、企業が認識しているリスクの主要なテーマとその時系列での変遷を明らかにする。テキストクラスタリングと、ローカルで動作する大規模言語モデル (LLM) による要約技術を組み合わせることで、膨大な非構造化データから効率的に洞察を抽出する。

プロジェクトの目的 (Project Goals)
日経225銘柄が認識する事業リスクの主要なカテゴリを特定する。
2018年から2024年という期間におけるリスク認識のトレンドと変化を分析する。
特に、パンデミックや地政学的緊張、AIの台頭といった外部環境の変化が企業のリスク認識に与えた影響を考察する。
llama.cpp を活用したローカルLLM推論環境とLlamaIndexを組み合わせることで、テキスト分析パイプラインの有効性を検証する。
使用技術 (Technologies Used)
主要なライブラリとツール
Python: データ処理とスクリプト実行の基盤言語。
Llama.cpp: ローカルGPU (NVIDIA CUDA) 上でGGUF形式のLlamaモデルを高速に推論するためのC++ライブラリ。llama-server を介してOpenAI互換APIとして利用する。
Llama 3 ELYZA JP 8B (GGUF q4_k_m): 要約タスクに用いる日本語に特化した大規模言語モデル。
LlamaIndex: RAG (Retrieval Augmented Generation) パイプラインを構築するためのフレームワーク。ベクトルストア、リトリーバー、レスポンスシンセサイザーの管理を行う。
HuggingFace pkshatech/RoSEtta-base: リスク文の埋め込み (Embedding) 生成に使用する。
SentenceTransformerRerank hotchpotch/japanese-reranker-cross-encoder-base-v1: 検索結果のリランカー（再ランク付け）に使用する。
FAISS (faiss-cpu): 大規模なベクトル検索インデックスの構築に使用する。
Pandas: データフレーム操作、データ管理に使用する。
JSON: 要約結果の出力形式。
WSL2 (Windows Subsystem for Linux 2): Windows環境上でのLinux開発環境およびGPUアクセラレーションを提供する。
動作環境
OS: Ubuntu on WSL2
GPU: NVIDIA GeForce RTX 4060 Ti (VRAM 8GB)
CUDA Toolkit: 12.0 (または互換バージョン)
Python Version: 3.12.3
仮想環境: venv
ライセンス (License)
MIT License

連絡先 (Contact)
[junish826@gmail.com]