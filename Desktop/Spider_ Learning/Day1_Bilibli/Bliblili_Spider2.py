# -*- coding:utf-8 -*-
import aiohttp
import asyncio
import time,re

'''
运行环境 Python3
使用了aiphttp,asyncio 极速加快了抓取的速度
'''

html_list={''}

async def get_html(session,page,keywords):
        while True:  # 循环获取 直到获取html源码成功
            res =await session.get(
                url='https://search.bilibili.com/all?keyword={0}&from_source=banner_search&page={1}'.format(keywords, page)
                )
            html= await  res.text(encoding="utf-8")
            if ('出错啦' not in html) and ('搜索结果' in html):  # 当出现 网页中出现 搜索结果 并且无出错啦 的文字时  爬取网页成功
                    return html
            else:
                pass

async def main(loop,keywords):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    cookies = {'finger': 'edc6ecda', 'LIVE_BUVID': 'AUTO8415287052851554',
               'buvid3': 'C9D3B003-4294-42C4-94CA-AD6684D75C3528955infoc'}
    async with aiohttp.ClientSession(cookies=cookies,headers=headers) as session:
        tasks=[loop.create_task(get_html(session,page,keywords)) for page in range(1,20)]
        finished,unfinished=await asyncio.wait(tasks)
        print(len(finished))
        htmls=[r.result() for r in finished]
        search_list[keywords]=htmls
        # [parse_detail(keywords=keywords,html=html) for html in htmls]


def parse_detail(html,keywords):
    '''
    解析html 获取对应数据导入数据库
    :param html: 待解析的html 源码
    :param keywords: 关键词
    :param page: 页数
    :return: 
    '''
    results=re.findall(r'<div class="watch-later-trigger watch-later">.*?<a.*?title="(.*?)".*?href="//(.*?)".*?<i class="icon-playtime"></i>(.*?)</span>.*?<i class="icon-subtitle"></i>(.*?)</span>.*?<i class="icon-date"></i>(.*?)</span>.*?</div>',html,re.S)
    print ('抓取关键词:{0}  数量{1}'.format(keywords,len(results)))
    for result in results:
        title,href,playtime,subtitle,date=result
        #tuple=(keywords, page, title.strip(), href.strip(), playtime.strip(), subtitle.strip(), date.strip())
        # flag=db.inser_data(tuple=tuple)
        # if flag==1:
        #     print 'Success'
        # else:
        #     print 'Erro'
        print ('发布日期 : {0}\t\t播放量 : {1}\t\t标题:{2}\t\t链接 : {3}\t\t弹幕数量 : {4} '.format(date.strip(),playtime.strip(),title.strip(),href.strip(),subtitle.strip()))

start_time=time.time()
loop=asyncio.get_event_loop()
search_list={'Python爬虫':'','j2ee':'','大数据':'','一加6':'','吃鸡':'','人工智能':''}
for keywords in search_list:
    print(keywords)
    loop.run_until_complete(main(loop,keywords))
loop.close()
for keywords in search_list:
    htmls=search_list[keywords]
    for html in htmls:
        parse_detail(html=html,keywords=keywords)
end_time=time.time()
run_time=end_time-start_time
print('单线程aiohttp爬取时间:{}'.format(run_time))

# pool=mp.Pool(4)
# start_time=time.time()
# craw_jobs=[ pool.apply_async(get_html,args=(page,))for page in range(1,10) ]
# htmls =[j.get() for j in craw_jobs]
# end_time=time.time()
# run_time=end_time-start_time
# print '多进程爬取时间 : {}s \t数量 : {}'.format(run_time,str(len(htmls)))