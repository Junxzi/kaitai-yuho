import os
import re

import pandas as pd
from sudachipy import dictionary, tokenizer
from sudachipy.tokenizer import Tokenizer

def clean_text(text: str) -> str:
    """
    金融文章向けの日本語テキストクリーニング関数。
    """
    if not isinstance(text, str):
        return ""
    
    # 全角スペース → 半角
    text = text.replace("\u3000", " ")
    
    # 記号の除去（日本語・英語・数字・スペース以外）
    text = re.sub(r"[^\w\sぁ-んァ-ン一-龥]", "", text)
    
    # 連続空白を1つに
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()


# 初期化
tokenizer_obj = dictionary.Dictionary().create()
split_mode = Tokenizer.SplitMode.C
MAX_BYTES = 49000

# ストップワード例（必要に応じて追加）
DEFAULT_STOPWORDS = set([
    "ある", "いる", "こと", "これ", "それ", "ため", "よう", "もの", "ところ", "及び", "にて",
    "ので", "として", "において", "により", "について", "に関する", "また", "など", "及び",
    "の", "に", "へ", "と", "が", "を", "で", "や", "から", "まで", "より", "ば", "か", "な", "だ", "です", "ます"
])

# 許可する品詞（動詞・名詞・形容詞など）
ALLOWED_POS = {"名詞", "動詞", "形容詞", "副詞"}

def tokenize_with_filters(text, mode=split_mode, allowed_pos=ALLOWED_POS, stopwords=DEFAULT_STOPWORDS):
    """
    長文に対応したSudachiトークナイズ + 品詞フィルタ + ストップワード除去。

    Parameters
    ----------
    text : str
        入力テキスト
    mode : SplitMode
        Sudachiの分割モード（通常C）
    allowed_pos : set
        残す品詞のセット（例: {"名詞", "動詞"}）
    stopwords : set
        除去したい単語のセット

    Returns
    -------
    List[str]
        フィルタ済みトークンのリスト
    """
    tokens = []
    start = 0
    while start < len(text):
        chunk = text[start:]
        while len(chunk.encode("utf-8")) > MAX_BYTES:
            chunk = chunk[:-100]
        try:
            morphemes = tokenizer_obj.tokenize(chunk, mode)
            for m in morphemes:
                surface = m.surface()
                pos = m.part_of_speech()[0]
                if surface not in stopwords and pos in allowed_pos and re.match(r"\S", surface):
                    tokens.append(surface)
        except Exception:
            pass
        start += len(chunk)
    return tokens