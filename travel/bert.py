import torch
from torch.utils.data import DataLoader
from transformers import BertJapaneseTokenizer, BertModel
import numpy as np
from sklearn.manifold import TSNE

def get_spot_vector(spot):
    MODEL_NAME = "cl-tohoku/bert-base-japanese-whole-word-masking"

    tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)

    max_length = 256
    search_vector = []  # 検索ワードのベクトルを追加

    encoding = tokenizer(
        spot,
        max_length=max_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    attention_mask = encoding["attention_mask"]

    with torch.no_grad():
        output = model(**encoding)
        last_hidden_state = output.last_hidden_state
        avg_hidden_state = \
            (last_hidden_state * attention_mask.unsqueeze(-1)).sum(1) \
                / attention_mask.sum(1, keepdim=True)

    search_vector = np.array(avg_hidden_state[0].cpu().numpy)
    # t-sne
    search_vector_tsne = TSNE(n_components=2).fit_transform(search_vector)
    return search_vector_tsne


if __name__ == "__main__":
    print(get_spot_vector("歴史"))