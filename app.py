import pandas as pd
import pickle
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from crypt import methods
from flask import *
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False

import sys
sys.path.append('./src')
from search import similar_words, find_brands, find_customer

#load data
with open("./data/res_dict_w2v.pickle",'rb') as f:
    brand_data = pickle.load(f)

txn_df = pd.read_csv('./data/txn_data.csv')
txn_df['time'] = txn_df['time'].apply(lambda x: datetime.strptime(str(x),'%Y%M%d').date())



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/ml', methods=["POST"])
def ml():
    # 搜尋關鍵字
    keywords = request.json.get("keyword")
    #  有勾選同義詞:true 沒有:false
    synonym = request.json.get("synonym")
    if synonym:
    # 若有：搜尋關鍵字
        s1_1 = keywords.split(' ')
        keywords, s1_2,  s1_3 = similar_words(keywords.split(' '))
    # 若無：直接split to list
    else:
        s1_1 = s1_2 = s1_3 = ''
        keywords = keywords.split(' ')

    section_1 = {"s1_1": s1_1,"s1_2": s1_2,"s1_3":s1_3} 
  
    target_brand, brand_words = find_brands(keywords,brand_data)
    section_2 =  {'s2_1':target_brand, 's2_2':brand_words}
 
    target_customer = find_customer(target_brand, txn_df, 'brand')

    #---plot---#
    # tar_txn_df = txn_df[txn_df['ID'].isin(set(target_customer))]
    # non_tar_txn_df = txn_df[~txn_df['ID'].isin(set(target_customer))]

    # test = tar_txn_df.groupby('time').agg({'txn_num':'sum'}).reset_index()
    # test['flag']='target'

    # test_1 = non_tar_txn_df.groupby('time').agg({'txn_num':'sum'}).reset_index()
    # test_1['flag']='non_target'

    # test = pd.concat([test,test_1],axis=0)

    # fig, ax = plt.subplots()
    # sns.barplot(ax = ax, data = test, x = 'time', y = 'txn_num', hue = 'flag')
    # plt.show()

    # 回傳資料格式弄成這樣
    return jsonify({"section1":section_1, "section2":section_2})

if __name__=='__main__':
    app.run(port=3000, debug=True)












#     return jsonify(
#         # 回傳資料格式弄成這樣
#         {
#             "section1": {
#                 "s1_1": ["時尚", "經典"],
#                 "s1_2": [["潮流", "流行"], ["雋永", "不敗"]],
#                 "s1_3": [[0.7, 0.5], [0.4, 0.55]]
#             },
#             "section2": {
#                 "s2_1": ["gucci", "coach"],
#                 "s2_2": ["時尚 時裝", "流行 經典"]
#             }
#         }
#     )

# if __name__=='__main__':
#     app.run(port=4000, debug=True)
