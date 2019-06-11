DATA_PATH = 'data/'
FORMAT = '.json'

WX_JS_CODE2SESSION = 'jscode2session'
USER_INFO = 'user_info'

DISCOVER_LIST = 'discover_list'
AD_LIST = 'ad_list'
AD_GOODS_LIST = 'ad_goods_list'
SEARCH_GOODS_LIST = 'search_goods_list'
GOODS_DETAIL = 'goods_detail'
ROOT_CATEGORY_LIST = 'root_category_list'
CHILD_CATEGORY_LIST = 'child_category_list'

def ad_list():
    return AD_LIST + FORMAT

def discover_list():
    return DISCOVER_LIST + FORMAT

def ad_goods_list(code, page, sort):
    return '{}_{}_{}_{}{}'.format(AD_GOODS_LIST, code, page, sort, FORMAT)

def goods_detail(id):
    return '{}_{}{}'.format(GOODS_DETAIL, id, FORMAT)

def root_category_list():
    return ROOT_CATEGORY_LIST + FORMAT

def child_category_list(root):
    return '{}_{}{}'.format(CHILD_CATEGORY_LIST, root, FORMAT)

def search_goods_list(keyword, code, page, sort):
    return '{}_{}_{}_{}_{}{}'.format(SEARCH_GOODS_LIST, keyword, code, page, sort, FORMAT)
