import pandas as pd
import pickle
import gensim #3.7.0
from gensim.models import KeyedVectors
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# brand[tags]
with open("./data/res_dict_w2v.pickle",'rb') as f:
    brand_data = pickle.load(f)


txn_df = pd.read_csv('./data/txn_data.csv')
txn_df['time'] = txn_df['time'].apply(lambda x: datetime.strptime(str(x),'%Y%M%d').date())

gensim_model = KeyedVectors.load_word2vec_format('./model/w2v_CNA_ASBC_300d.vec' ,binary=False, encoding='utf-8', unicode_errors='ignore')

# 1. 先回傳關鍵字集合
#input: keywords -> return similar words
keywords = ['時尚','經典']
def similar_words(input_keywords, w2v_model=gensim_model):
    s = set()
    for tags in keywords:
        s.add(tags)
        for sim_tag in gensim_model.most_similar(tags,topn=3):
            if sim_tag[1]>0.6:
                s.add(sim_tag[0])    
    return list(s)
keywords = similar_words(keywords)

# 2. 找哪些牌子有這些tag
def find_brands(input_keywords, input_brand_data=brand_data):
    '''
    input_keywords: list(tag)
    brand_data: brand:[tag1, tag2, tag3...]
    '''
    res_s = set()
    for tag in input_keywords:
        for k,v in input_brand_data.items():
            if tag in v:
                res_s.add(k)
    print(f'input_keywords: {input_keywords}')
    return res_s

find_brands(['時尚','經典','潮流'],brand_data)
target_brand = find_brands(keywords,brand_data)

# 3. 找到牌子後, 有哪些人曾購買過這個品牌
def find_customer(input_target_brand, input_txn_data, brand_col_name):
    '''
    input_target_brand: set(tag)
    input_txn_data: brand:[tag1, tag2, tag3...]
    '''
    return input_txn_data[input_txn_data[brand_col_name].isin(input_target_brand)]['ID']

target_customer = find_customer(target_brand, txn_df, 'brand')

target_customer

# 4. 這群客戶與在資料期間內各月購買的金額 / 名單內購買比率比名單外高幾倍
tar_txn_df = txn_df[txn_df['ID'].isin(set(target_customer))]
non_tar_txn_df = txn_df[~txn_df['ID'].isin(set(target_customer))]



test = tar_txn_df.groupby('time').agg({'txn_num':'sum'}).reset_index()
test['flag']='target'

test_1 = non_tar_txn_df.groupby('time').agg({'txn_num':'sum'}).reset_index()
test_1['flag']='non_target'

test = pd.concat([test,test_1],axis=0)

fig, ax = plt.subplots()
sns.barplot(ax = ax, data = test, x = 'time', y = 'txn_num', hue = 'flag')
plt.show()