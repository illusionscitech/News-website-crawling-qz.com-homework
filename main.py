import urllib.request,urllib.error
from bs4 import BeautifulSoup
import time
import csv


# 定义要提取新闻的URL
url = 'https://qz.com/'

# 定义要匹配的关键词
keywords = ['US', 'China']

#解析url
def askURL(url):  #用户代理，告诉服务器，机器类型，，，本质是告诉浏览器我们可以接受文件水平
    head = {      #模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 84.0 .4147 .89 Safari / 537.36 SLBrowser / 7.0 .0 .11261 SLBChan / 103"
    }
    request  = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):   #标签
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html



def ask_deta_page(link):
    author = []
    time_str = []
    subtitle_str = []
    subdigest_str = []
    source = []
    for link1 in link:
        # if is_url(link1):
        r = askURL(link1)
        soup = BeautifulSoup(r, 'html.parser')
        # print(soup)
        divs = soup.select('div.sc-9tztzq-2')
        for div in divs:
            for headline in div.find_all('h1'):
                # print("ziyemian:", headline)
                subtitle = headline.text.strip()
                subtitle_str.append((subtitle))

            for headline in div.find_all('h2'):
                # print("ziyemian:", headline)
                # info_tag = headline.text.strip()
                subdigest = headline.text.strip()
                subdigest_str.append((subdigest))


            divss = soup.select('div.sc-1jc3ukb-4')
            for sdiv in divss:
                for headline in sdiv.find_all('a'):   #.select_one('a')['href']
                    # print("ziyemian:", headline)
                    subauthor = headline.text.strip()
                    author.append((subauthor))

            divsss = soup.select('div.sc-1jc3ukb-2')
            for ssdiv in divsss:
                for headline in ssdiv.find_all('time'):  # .select_one('a')['href']
                    # print("ziyemian:", headline)
                    datetime_value = headline['datetime']
                    date_part = datetime_value[:10]  # 提取日期部分，即前10个字符
                    time_part = datetime_value[11:19]  # 提取时间部分，即第11到19个字符
                    datetime_value = date_part +" "+ time_part
                    # print(datetime_value)
                    # subauthor = headline.text.strip()
                    time_str.append((datetime_value))

        divs = soup.select('div.sc-gkv9lo-3')
        for div in divs:
            for headline in div.find_all('h1'):
                # print("ziyemian:", headline)
                subtitle = headline.text.strip()
                subtitle_str.append((subtitle))
                # print(subtitle)

            # for headline in div.find_all('div'):
            headline = div.find_all('div')

            if len(headline) == 1:
                subdigest = ""
                subdigest_str.append((subdigest))
            else:

                subdigest = headline[1].text.strip()
                subdigest_str.append((subdigest))

            divss = soup.select('div.sc-1jc3ukb-4')
            for sdiv in divss:
                for headline in sdiv.find_all('a'):  # .select_one('a')['href']
                    # print("ziyemian:", headline)
                    subauthor = headline.text.strip()
                    author.append((subauthor))

            divsss = soup.select('div.sc-1jc3ukb-2')
            for ssdiv in divsss:
                for headline in ssdiv.find_all('time'):  # .select_one('a')['href']
                    # print("ziyemian:", headline)
                    datetime_value = headline['datetime']
                    date_part = datetime_value[:10]  # 提取日期部分，即前10个字符
                    time_part = datetime_value[11:19]  # 提取时间部分，即第11到19个字符
                    datetime_value = date_part + " " + time_part
                    # print(datetime_value)
                    # subauthor = headline.text.strip()
                    time_str.append((datetime_value))

    # print(subtitle_str)
    # print(subdigest_str)
    # print(author)
    # print(time_str)
    # print(len(subtitle_str), len(subdigest_str), len(author), len(time_str))

    return subtitle_str,time_str,source,subdigest_str,author

def ask_page(soup):
    news_title = []
    link = []
    minlink = []
    divs = soup.select('div.sc-11qwj9y-0')
    for div in divs:
        for headline in div.find_all('div', class_='sc-1pw4fyi-7'):
            # print("tit:", headline)

            if headline.find('div',class_ ='sc-1hjwdsc-2'):
                title = headline.find('h4').text.strip()
                news_title.append((title))
                # print("4:",title)
                minlink = []
                for lik in headline:
                    minlink.append(lik)
                    # print("555:",lik)
                    # if div
                # print("224:",minlink[1])
                mlink = minlink[1]['href']#.find('a')
            else:
                # print("解析不正确")
                title = headline.find('h4').text.strip()
                news_title.append((title))
                # print(title)
                links = headline.select_one('a')['href']
                link.append(links)
                # print(links)
    # print(link)
    # print(len(link))
    return news_title,link

# 定义一个函数来提取页面信息
def get_news():
    # r = requests.get(url)
    r = askURL(url)
    # soup = BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r, 'html.parser')
    news,link = ask_page(soup)   #访问当前页面，提取链接和标题
    subtitle_s,time_s,source,digest,subauthor= ask_deta_page(link) # 访问每篇文章的详情页面，提取标题，发行社和作者信息

    return subtitle_s,time_s,source,digest,subauthor


#添加引用
def key_matched(subtitle_s, digest):
    matched = []
    for title, summary in zip(subtitle_s, digest):
        if any(keyword in element for keyword in keywords for element in [title, summary]):
            matched.append('Yes')
        else:
            matched.append('')

    return matched


#保存结果
def savefile(subtitle_s, time_s, source, digest,subauthor):

    # Создаем список данных
    # data = zip(subtitle_s, time_s,subauthor, digest)
    file_path = 'result.csv'
    match = key_matched(subtitle_s, digest)


    # Сохраняем данные в файле CSV
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file,delimiter='\t')
        # Записываем заголовки столбцов
        writer.writerow(['title', 'time', 'author', 'digest', 'matched'])

        # 写入数据行
        for data_row in zip(subtitle_s, time_s, subauthor, digest, match):

            # Записываем данные
            writer.writerow(data_row)


    print('Результаты сохранены в JSON файл:', file_path)

# 定义一个函数来下载新闻
def download_news():
    # 获取新闻
    subtitle_s,time_s,source,digest,subauthor = get_news()
    savefile(subtitle_s,time_s,source,digest,subauthor)

# 循环运行脚本，每隔一段时间下载新的新闻
while True:
    download_news()
    time.sleep(86400)  # 每隔24小时下载一次新闻