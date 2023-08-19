import torch
from transformers import BertJapaneseTokenizer, BertModel
import pickle
import numpy as np


def find(text):
    # 口コミから得たデータの読込
    path = "/Users/tk/卒業研究/myproject/travel/travelrecommend/travel/data/bert_result_dic.pkl"
    with open(path, "rb") as f:
        bert_result_dic = pickle.load(f)

    titles = bert_result_dic["titles"]
    brd_labels = bert_result_dic["labels"]
    brd_vec = bert_result_dic["sentence_vectors"]


    # BERTの日本語モデル
    MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
    # トークナイザとモデルのロード
    tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)

    # text = "歴史 家族"  # 検索欄から取得
    max_length = 256

    encoding = tokenizer( # torch.Size([1, 256, 768])
        text,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    # GPU使用
    # encoding = { k: v.cuda() for k, v in encoding.items() }
    attention_mask = encoding["attention_mask"] # torch.Size([1, 256])

    # 文章ベクトルを計算
    # BERTの最終層の出力の平均を計算する。（ただし、[PAD]は除く）
    with torch.no_grad():
        output = model(**encoding)
        last_hidden_state = output.last_hidden_state
         # torch.Size([1, 768])
        avg_hidden_state = \
            (last_hidden_state * attention_mask.unsqueeze(-1)).sum(1) \
            / attention_mask.sum(1, keepdim=True)

    # 検索した文字列のベクトル
    sentence_vector = avg_hidden_state[0].numpy() # shape(768,)

    # 口コミデータと検索文字列の類似度行列
    sim_matrix = brd_vec.dot(sentence_vector) # shape(17900,)

    similar_texts = np.argsort(-(sim_matrix))
    similar_labels = brd_labels[similar_texts]

    """ 検索文字列と口コミ行列の類似度からスポットごとの類似度の強度を求める """
    label_strength = {}
    for label in range(len(titles)):
        indices = [ (len(similar_labels) - i) for i, similar_label in enumerate(similar_labels) if similar_label==label]
        label_strength[label] = sum(indices) / len(indices)



    # 関連強度が強い順にソート
    sorted_label_strength = sorted(label_strength.items(), key=lambda x:x[1], reverse=True)

    similar_title = []
    for i in sorted_label_strength:
        print(titles[i[0]])
        similar_title.append(titles[i[0]])
        
    return similar_title
