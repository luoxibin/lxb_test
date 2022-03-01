#读取数据集
content = []
with open('./phone.txt', encoding='utf-8') as fp:
    content = fp.readlines()

#格式化数据集
data = {}
for line in content:
    line = line.strip().replace("\n", '').split(',')
    if not line[0] in data.keys():
        data[line[0]] = {line[1]:line[2]}
    else:
        data[line[0]][line[1]] = line[2]

#计算用户相似度(欧几里得距离公式，计算两点间的距离，值越小说明相似度越高)
from math import *

def Euclid(user1, user2):

    #取出两个用户都购买过的手机
    user1_data = data[user1]
    user2_data = data[user2]
    #默认距离
    distance = 0
    #是否有相似的标识
    xs = False
    #遍历找出都购买过的手机
    for key in user1_data.keys():
        if key in user2_data.keys():
            xs = True
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)
    if xs:
        return 1/(1+sqrt(distance))
    else:
        return  -1

#计算某个用户和其他用户相似度比对
def top_simliar(user):

    res = []

    for userid in data.keys():

        #移除当前用户
        if not userid == user:
            simliar = Euclid(user, userid)
            res.append((userid, simliar))
    res.sort(key=lambda  val:val[1], reverse=True)
    return res

print(top_simliar('5'))

#构建推荐方法
def recommend(user):
    top_user = top_simliar(user)
    if top_user:
        #先拿一个相似度最高的用户
        top_user = top_user[0][0]
        #如果没有一个用户与当前用户相似，那么推荐列表就为空，
        if top_simliar(user)[0][1] == -1: # 如果没有一个用户与当前用户相似，又不想推荐列表为空的话就注释掉判断
            recommend_list = []
        else:
            #相似度最高的用户的购买记录
            items = data[top_user]
            #推荐列表
            recommend_list = []
            for item in items.keys():
                if item not in data[user].keys():
                    recommend_list.append((item, items[item]))
            #排序，多个手机按照评分排序，分数高的优先级高
            recommend_list.sort(key=lambda val:val[1], reverse=True)
    else:
        recommend_list = []
    return recommend_list[:10]


try:  # 如果data里没有user1或user2就会异常
    recommend_list = recommend('8')
except:
    recommend_list = []
print(recommend_list)
