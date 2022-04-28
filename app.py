from crypt import methods
from flask import *
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/ml', methods=["POST"])
def ml():

    # 搜尋關鍵字
    keyword = request.json.get("keyword")

    #  有勾選同義詞:true 沒有:false
    synonym = request.json.get("synonym")

    return jsonify(
        # 回傳資料格式弄成這樣
        {
            "section1": {
                "s1_1": ["時尚", "經典"],
                "s1_2": [["潮流", "流行"], ["雋永", "不敗"]],
                "s1_3": [[0.7, 0.5], [0.4, 0.55]]
            },
            "section2": {
                "s2_1": ["gucci", "coach"],
                "s2_2": ["時尚 時裝", "流行 經典"]
            }
        }
    )


app.run(port=5000, debug=True)
