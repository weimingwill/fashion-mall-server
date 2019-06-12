# Fashion Mall Server

微信小程序 [fashion-mall](https://github.com/weimingwill/fashion-mall) 的 mock server，供大家学习使用。

[fashion-mall](https://github.com/weimingwill/fashion-mall) 这个小程序是按照 [wepy-mall](https://github.com/dyq086/wepy-mall) 去实现的，主要是个人学习用，担心 wepy-mall 在哪天突然不提供 server 了，没法看到数据，所以爬了一些 API 数据，做了一个 mock server。

## 功能

[fashion-mall](https://github.com/weimingwill/fashion-mall) 这个小程序里显示需要的数据的 API 都有了，学习测试没有问题。原版 API 测试版没有的功能也没有实现，比如说 收藏商品，加入购物车等，有兴趣的朋友可以在这个基础上去继续开发。

## 使用指南

### 安装

```python
virtualenv -p python3 venv
source venv/bin/activate
pip install requirement.txt
```

### 启动 server

```bash
python app.py
```

### 爬数据

```bash
python crawler.py
```

数据量较大，图片爬的时间较长，没有做优化，全部大小大概有2G。

### 缺陷

1. 所有分页的 API 只取了**两页**，**每页10个数据**供测试使用。测试小程序的显示够用了，但是在要加载更多数据时，会出现错误。主要是在两个地方: `api/home/hostGoodsList` 和 `/api/mall/searchGoodsList`

2. 搜索功能有比较大的局限，只能搜索分类出现的那些词，比如说 上衣，风衣，裙子 等。
