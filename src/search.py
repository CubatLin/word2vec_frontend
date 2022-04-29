import gensim #3.7.0
from gensim.models import KeyedVectors
gensim_model = KeyedVectors.load_word2vec_format('./model/w2v_CNA_ASBC_300d.vec' ,binary=False, encoding='utf-8', unicode_errors='ignore')

def similar_words(input_keywords, w2v_model=gensim_model):
    s = set() #keyword set
    s1_2 = [] #similar words
    s1_3 = [] #similar score
    for tags in input_keywords:
        tmp_words = []; tmp_score = []
        s.add(tags)
        for sim_tag in gensim_model.most_similar(tags,topn=3):
            if sim_tag[1]>0.65:
                s.add(sim_tag[0]) 
                tmp_words.append(sim_tag[0])
                tmp_score.append(round(sim_tag[1],3)) 
            s1_2.append(tmp_words)
            s1_3.append(tmp_score)

    return list(s), s1_2 ,s1_3


def find_brands(input_keywords, input_brand_data):
    '''
    input_keywords: list(tag)
    brand_data: brand:[tag1, tag2, tag3...]
    '''
    res_s = set()
    for tag in input_keywords:
        for k,v in input_brand_data.items():
            if tag in v:
                res_s.add(k)
    
    res_l = list(res_s); del res_s
    s2_2 = []
    for brand in res_l:
        s2_2.append(list( set(input_brand_data[brand]).intersection(input_keywords)) )
    return res_l, s2_2


def find_customer(input_target_brand, input_txn_data, brand_col_name):
    '''
    input_target_brand: set(tag)
    input_txn_data: brand:[tag1, tag2, tag3...]
    '''
    return input_txn_data[input_txn_data[brand_col_name].isin(input_target_brand)]['ID']




