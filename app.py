import io
from helper import util, filename
from flask import Flask, jsonify, send_file, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/images/<filename>")
def get_image(filename):
    image_binary = util.read_image(filename)
    return send_file(
        io.BytesIO(image_binary),
        mimetype = 'image/jpeg',
        as_attachment = True,
        attachment_filename = filename)

@app.route("/api/wechat/jscode2session")
def wx_jscode_2_session():
    return jsonify({})

@app.route("/api/userCenter/getUserInfo")
def get_user_info():
    return jsonify({})

@app.route("/api/adverts/list")
def get_ads_list():
    data = util.read_data(filename.ad_list())
    return jsonify(data)

@app.route("/api/mall/discoverList")
def get_discover_list():
    data = util.read_data(filename.discover_list())
    return jsonify(data)

@app.route("/api/home/hostGoodsList")
def get_ad_goods_list():
    page = request.args.get('page')
    sort = request.args.get('sort')
    code = request.args.get('cateCode')
    data = util.read_data(filename.ad_goods_list(code, page, sort))
    return jsonify(data)

@app.route("/api/mall/searchGoodsList")
def get_search_goods_list():
    keyword = request.args.get('searchKeyWords')
    code = request.args.get('cateCode')
    page = request.args.get('page')
    sort = request.args.get('sort')
    data = util.read_data(filename.search_goods_list(keyword, code, page, sort))
    return jsonify(data)

@app.route("/api/mall/goods")
def get_goods_detail():
    goods_id = request.args.get('id')
    data = util.read_data(filename.goods_detail(goods_id))
    return jsonify(data)

@app.route("/api/mall/rootCtegoryList")
def get_root_category_list():
    data = util.read_data(filename.root_category_list())
    return jsonify(data)

@app.route("/api/mall/childGoodsCatetoryList")
def get_child_category_list():
    rootCode = request.args.get('rootCategoryCode')
    data = util.read_data(filename.child_category_list(rootCode))
    return jsonify(data)

@app.route("/api/mall/goodsFavorite/add")
def favorite_goods():
    return jsonify({})

@app.route("/api/mall/goodsFavorite/delete")
def unfavorite_goods():
    return jsonify({})

@app.route("/api/mall/goodsFavorite/goodsIsFavorite")
def is_goods_favorite():
    return jsonify({})

@app.route("/api/mall/goodsCart/add")
def add_to_cart():
    return jsonify({})

@app.route("/api/searchkeyword/add")
def add_search_keyword():
    return jsonify({})

@app.route("/api/searchkeyword/list")
def get_search_keywords():
    return jsonify({})

@app.route("/api/searchkeyword/clear")
def clear_search_keywords():
    return jsonify({})

app.run()
