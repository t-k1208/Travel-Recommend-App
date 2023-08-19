# 類似するスポットを抽出
import collections
import pickle

# スポット名を渡して、類似スポットを5つ返す
def get_similar_title(title_target, titles, labels, similar_labels):
    title_similar = []
    print(title_target)
    #print(high_rated_dic[title_target]["text"])
    print("\n","="*50,"\n")

    # ラベルに相当するインデックスを取り出す
    index = titles.index(title_target)
    a = similar_labels[labels==index, :]
    # ターゲットスポットのテキストそれぞれの上位3つの類似スポットをカウントする
    count = collections.Counter(a[:, 0:4].reshape(-1))
    # 値の大きい順にforで類似スポットのラベルを得てテキストを表示する
    for i, values in enumerate(count.most_common()):
        label = values[0]
        # 同じスポットならスキップ
        if label == index: continue
        title = titles[label]
        title_similar.append(title)
        if len(title_similar) == 5: break
        print(label)
        print(title)
        #print(high_rated_dic[title]["text"])
        print()
        
    return title_similar
        
#if __name__ == "__main__":
    ## BERTで算出したデータの読み出し
    #path = "../travel/data/"
    #with open(path+'high_rated_dic.pkl', 'rb') as f:
        #high_rated_dic = pickle.load(f)
    #with open(path+'title_list.pkl', 'rb') as f:
        #title_list = pickle.load(f)
    #with open(path+'result_high_sim.pkl', 'rb') as f:
        #result_high_sim = pickle.load(f)
    #titles = result_high_sim["titles"]
    #labels = result_high_sim["labels"]
    #similar_labels = result_high_sim["similar_labels"]
    #sim_matrix = result_high_sim["sim_matrix"]

    ## 類似spot表示
    #title_target = title_list[4]
    #title_similar = get_similar_title(title_target)
    #print(title_target)
    #print(title_similar)