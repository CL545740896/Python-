# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import requests
from Db_Bilibili import Db
db=Db()  #数据库
'''
Day1
正则表达式的练习
抓取B站的视频,将抓取的数据导入到sql中
'''
'''
加入多线程分布式爬取
'''

def get_html(page,search_list):
    '''
    获取html源码 并保存到列表中 key 作映射
    :param page: 查询页数
    :param search_list: 查询列表
    :return: search_list 关键词与html源码映射的列表
    '''
    for keywords in search_list:
            while True: # 循环获取 直到获取html源码成功
                headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
                cookies={'finger':'edc6ecda', 'LIVE_BUVID':'AUTO8415287052851554','buvid3':'C9D3B003-4294-42C4-94CA-AD6684D75C3528955infoc'}
                res=requests.get(url='https://search.bilibili.com/all?keyword={0}&from_source=banner_search&page={1}'.format(keywords,page),cookies=cookies,headers=headers)
                html=res.text
                if ('出错啦' not in html) and  ('搜索结果' in html):  #当出现 网页中出现 搜索结果 并且无出错啦 的文字时  爬取网页成功
                    search_list[keywords]=html
                    break
                else:
                    pass
    return search_list


def parse_detail(html,keywords,page):
    '''
    解析html 获取对应数据导入数据库
    :param html: 待解析的html 源码
    :param keywords: 关键词
    :param page: 页数
    :return: 
    '''
    results=re.findall(r'<div class="watch-later-trigger watch-later">.*?<a.*?title="(.*?)".*?href="//(.*?)".*?<i class="icon-playtime"></i>(.*?)</span>.*?<i class="icon-subtitle"></i>(.*?)</span>.*?<i class="icon-date"></i>(.*?)</span>.*?</div>',html,re.S)
    print '抓取关键词:{0} 第{1}页 数量{2}'.format(keywords,page,len(results))
    for result in results:
        title,href,playtime,subtitle,date=result
        tuple=(keywords, page, title.strip(), href.strip(), playtime.strip(), subtitle.strip(), date.strip())
        flag=db.inser_data(tuple=tuple)
        if flag==1:
            print 'Success'
        else:
            print 'Erro'
        # print '发布日期 : {0}\t\t播放量 : {1}\t\t标题:{2}\t\t链接 : {3}\t\t弹幕数量 : {4}'.format(date.strip(),playtime.strip(),title.strip(),href.strip(),subtitle.strip())

search_list={'python爬虫':'','j2ee':'','python大数据':'','信誓旦旦':''}   #待抓取的关键词列表
for page in range(1,20):  #爬取12页
    htmls=get_html(page=page,search_list=search_list)
    for keywords in htmls:
        parse_detail(html=htmls[keywords],keywords=keywords,page=page)





