
import urllib
import json
from bs4 import BeautifulSoup
# http://www.cnblogs.com/zhoudayang/p/5474053.html
import requests
# 获取页数
def get_pages_counts():
    # url = '''http://data.eastmoney.com/DataCenter_V3/jgdy/xx.ashx?pagesize=50&page=%d''' % 1
    # url += "&js=var%20ngDoXCbV&param=&sortRule=-1&sortType=0&rt=48753724"
    url = '''http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=%d''' % 1
    url += "&pageSize=20&js=var%20MuaZqltj={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517270127528"
    wp = urllib.request.urlopen(url)
    # data = wp.read().decode('gbk')
    data = wp.read().decode('utf-8')
    data = data.replace('rank:', '\"rank\":').replace('pages:', '\"pages\":').replace('total:', '\"total\":')
    start_pos = data.index('=')
    json_data = data[start_pos + 1:]
    dict = json.loads(json_data)
    pages =dict['pages']
    # import urllib
    # jzc_html = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=1" \
    #            "&pageSize=20&js=var%20SGFWioRt={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517274040425"
    # request = urllib.request.Request(jzc_html)
    # response = urllib.request.urlopen(request)
    # body = json.loads(response.read())
    return pages
pagenumber = get_pages_counts()

def get_pages_count2():
    url = '''http://data.eastmoney.com/DataCenter_V3/jgdy/xx.ashx?pagesize=50&page=%d''' % 1
    url += "&js=var%20ngDoXCbV&param=&sortRule=-1&sortType=0&rt=48753724"
    wp = urllib.request.urlopen(url)
    print(wp)
    data = wp.read().decode('gbk')
    start_pos = data.index('=')
    json_data = data[start_pos + 1:]
    dict = json.loads(json_data)
    pages =dict['pages']
    return pages


# 获取链接列表
def get_url_lists(start,end):
    url_list=[]
    while(start<=end):
        url = '''http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=%d''' %start
        url += "&pageSize=20&js=var%20MuaZqltj={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517270127528"
        url_list.append(url)
        start+=1
    return url_list

url_list = get_url_lists(0,pagenumber)

def get_tickers(url_list):
    tickers={}
    for index in range(len(url_list)):
        url0 = urllib.request.urlopen(url_list[index])
        test_message = url0.read().decode('utf-8')
        start_pos = test_message.index('=')
        json_data = test_message[start_pos + 1:]
        json_data = json_data.replace('rank:', '\"rank\":').replace('pages:', '\"pages\":').replace('total:', '\"total\":')
        dict = json.loads(json_data)
        list = dict['rank']
        for index_list in range(len(list)):
            stock_info = list[index_list].split(',')
            tickers[stock_info[1]]=stock_info[2]

    return tickers


def get_tickers_ex(url_list):
    tickers={}
    for index in range(len(url_list)):
        url0 = urllib.request.urlopen(url_list[index])
        test_message = url0.read().decode('utf-8')
        start_pos = test_message.index('=')
        json_data = test_message[start_pos + 1:]
        json_data = json_data.replace('rank:', '\"rank\":').replace('pages:', '\"pages\":').replace('total:', '\"total\":')
        dict = json.loads(json_data)
        list = dict['rank']
        for index_list in range(len(list)):
            stock_info = list[index_list].split(',')
            if(stock_info[1][0]) == '6':
                tickers[stock_info[1] + '.SS'] = stock_info[2]
            if (stock_info[1][0]) == '3':
                tickers[stock_info[1] + '.SZ'] = stock_info[2]
            if (stock_info[1][0]) == '0':
                tickers[stock_info[1] + '.SZ'] = stock_info[2]

    return tickers

cn_tickers = get_tickers_ex(url_list)
def printTickers(cn_tickers):
    tempstr = cn_tickers.split('\r\n')
    filename = "'cn_tickers.csv"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    for _tempstr in tempstr:
        f.write(_tempstr)
        f.write('\n')
    f.close()

import time
import json
import datetime
from tushare.stock import cons as ct
import os


try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


def get_hist_data(code=None, start=None, end=None,
                  ktype='D', retry_count=3,
                  pause=0.001):
    """
        获取个股历史交易记录
    Parameters
    ------
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率
    """
    symbol = ct._code_to_symbol(code)
    url = ''
    if ktype.upper() in ct.K_LABELS:
        url = ct.DAY_PRICE_URL % (ct.P_TYPE['http'], ct.DOMAINS['ifeng'],
                                  ct.K_TYPE[ktype.upper()], symbol)
    elif ktype in ct.K_MIN_LABELS:
        url = ct.DAY_PRICE_MIN_URL % (ct.P_TYPE['http'], ct.DOMAINS['ifeng'],
                                      symbol, ktype)
    else:
        raise TypeError('ktype input error.')

    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(url)
            lines = urlopen(request, timeout=10).read()
            if len(lines) < 15:  # no data
                return None
        except Exception as e:
            print(e)
        else:
            js = json.loads(lines.decode('utf-8') if ct.PY3 else lines)
            cols = []
            if (code in ct.INDEX_LABELS) & (ktype.upper() in ct.K_LABELS):
                cols = ct.INX_DAY_PRICE_COLUMNS
            else:
                cols = ct.DAY_PRICE_COLUMNS
            if len(js['record'][0]) == 14:
                cols = ct.INX_DAY_PRICE_COLUMNS
            df = pd.DataFrame(js['record'], columns=cols)
            if ktype.upper() in ['D', 'W', 'M']:
                df = df.applymap(lambda x: x.replace(u',', u''))
                df[df == ''] = 0
            for col in cols[1:]:
                df[col] = df[col].astype(float)
            if start is not None:
                df = df[df.date >= start]
            if end is not None:
                df = df[df.date <= end]
            if (code in ct.INDEX_LABELS) & (ktype in ct.K_MIN_LABELS):
                df = df.drop('turnover', axis=1)
            df = df.set_index('date')
            df = df.sort_index(ascending=False)
            return df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)

import time
import json
import datetime
import urllib
def get_hist_data_163(code=None,index_type=None, start=None, end=None,retry_count=3,
                  pause=0.001):
    if (index_type.upper() == 'SS'):
        index_id = '0' + code
    if (index_type.upper() == 'SZ'):
        index_id = '1' + code
    startstr = start.strftime('%Y%m%d')
    endstr = end.strftime('%Y%m%d')
    url = 'http://quotes.money.163.com/service/chddata.html?code='
    url += index_id
    url += '&start='
    url += startstr
    url += '&end='
    url += endstr
    url += '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            test_data = urllib.request.urlopen(url,timeout=10).read().decode("GB2312")
        except Exception as e:
            print(e)
        else:
            tempstr = test_data.split('\r\n')
            filename = "'temp.csv"
            # opening the file with w+ mode truncates the file
            f = open(filename, "w+")
            for _tempstr in tempstr:
                f.write(_tempstr)
                f.write('\n')
            f.close()
            df = pd.read_csv(filename, encoding="GB2312")
            df = df.set_index('日期')
            df = df.sort_index(ascending=False)
            return df


import os
import datetime as dt
import sys
sys.path.append('/easyquotation.easyquotation')
sys.path.append(r'C:\Users\home\AppData\Local\Programs\Python\Python36\Lib\site-packages\tushare\stock')
import pandas as pd
def download_stocks(tickers,folder,source):
    start = dt.datetime(1998, 1, 1)
    end = dt.datetime(2018, 4, 1)
    if not os.path.exists(folder):
        os.mkdir(folder)
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists(folder+'/{}.csv'.format(ticker)):

            while True:
                # try:
                #     web.DataReader(ticker, "google", dt.datetime(2015, 1, 1), dt.datetime(2018, 2, 1))
                # except IOError as err:
                #     print("I/O error: {0}".format(err))

                    # df = ts.get_h_data(ticker.split(".")[0], start='2015-01-01', end='2018-02-01')
                if(source == 'ifeng'):
                    df = get_hist_data(ticker.split(".")[0], start='1998-01-01', end='2018-04-01')
                elif(source == '163'):
                    df = get_hist_data_163(ticker.split(".")[0],ticker.split(".")[1], start, end)
                break
            pd.DataFrame(df).to_csv(folder + '/{}.csv'.format(ticker))
        else:

            print('Already have {}'.format(ticker))
    return 1
folder = 'cn_stock_163'
download_stocks(list(cn_tickers.keys()),folder,'163')



import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

def download_stock(tickers,folder):
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime(2018, 2, 1)
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists(folder+'/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "google", start, end)
            df.to_csv(folder+'/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
    return 1
folder = 'cn_stock'
download_stock(list(cn_tickers.keys()),folder)


from bs4 import BeautifulSoup #导入包
import urllib3
def get_hist_data_invest(code=None,dtype=None,
                  ktype='D', retry_count=3,
                  pause=0.001):
    http = urllib3.PoolManager()
    symbol = ct._code_to_symbol(code)
    url = ''
    if dtype == 'top10':
        url = '''http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CirculateStockHolder/stockid/''' % symbol
        url += ".phtml"
    elif dtype == 'Fund':
        url = '''http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_FundStockHolder/stockid/''' % symbol
        url += ".phtml"
    else:
        raise TypeError('dtype input error.')

    for _ in range(retry_count):
        time.sleep(pause)
        try:
            response = http.request('GET', url)
            soup = BeautifulSoup(response.data.decode('gbk'))
            tables = soup.findAll('table')
            # tab = tables[3]
            for tab in tables:
                for tr in tab.findAll('tr'):
                    for td in tr.findAll('td'):
                        print(td.getText())
            request = Request(url)
            lines = urlopen(request, timeout=10).read()
            if len(lines) < 15:  # no data
                return None
        except Exception as e:
            print(e)
        else:
            js = json.loads(lines.decode('utf-8') if ct.PY3 else lines)
            cols = []
            if (code in ct.INDEX_LABELS) & (ktype.upper() in ct.K_LABELS):
                cols = ct.INX_DAY_PRICE_COLUMNS
            else:
                cols = ct.DAY_PRICE_COLUMNS
            if len(js['record'][0]) == 14:
                cols = ct.INX_DAY_PRICE_COLUMNS
            df = pd.DataFrame(js['record'], columns=cols)
            if ktype.upper() in ['D', 'W', 'M']:
                df = df.applymap(lambda x: x.replace(u',', u''))
                df[df == ''] = 0
            for col in cols[1:]:
                df[col] = df[col].astype(float)
            if start is not None:
                df = df[df.date >= start]
            if end is not None:
                df = df[df.date <= end]
            if (code in ct.INDEX_LABELS) & (ktype in ct.K_MIN_LABELS):
                df = df.drop('turnover', axis=1)
            df = df.set_index('date')
            df = df.sort_index(ascending=False)
            return df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)



def download_stocks_investData(tickers,folder):
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime(2018, 2, 1)
    if not os.path.exists(folder):
        os.mkdir(folder)
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        while True:
            # try:
            #     web.DataReader(ticker, "google", dt.datetime(2015, 1, 1), dt.datetime(2018, 2, 1))
            # except IOError as err:
            #     print("I/O error: {0}".format(err))
            try:
                # df = ts.get_h_data(ticker.split(".")[0], start='2015-01-01', end='2018-02-01')
                df = get_hist_data_invest(ticker.split(".")[0],dtype = 'top10')
                break
            except IOError as err:
                print("I/O error: {0}".format(err))
            except ValueError:
                print("Oops!   Try again...")
            # df = ts.get_h_data(ticker.split(".")[0], start='2015-01-01', end='2018-02-01')
            pd.DataFrame(df).to_csv(folder+'/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
    return 1
folderinvestData = 'cn_stock_investData'
download_stocks_investData(list(cn_tickers.keys()),folderinvestData)

# 根据指定股票编号，下载此股票的数据，这里使用腾信接口
def load_quote_data(self, quote, start_date, end_date, is_retry, counter):
    # print("开始下载指定股票的数据..." + "\n")

    start = timeit.default_timer()
    # 直接从腾讯的js接口中读取
    if (quote is not None and quote['Symbol'] is not None):
        try:
            url = 'http://data.gtimg.cn/flashdata/hushen/latest/daily/' + quote['Symbol'] + '.js'  # 腾讯的日k线数据
            r = requests.get(url)  # 向指定网址请求，下载股票数据
            alldaytemp = r.text.split("\\n\\")[2:]  # 根据返回的字符串进行处理提取出股票数据的数组形式
            quote_data = []
            for day in alldaytemp:
                if (len(day) < 10):  # 去掉一些不对的数据，这里去除方法比较笼统.
                    continue
                oneday = day.strip().split(' ')  # 获取日K线的数据。strip为了去除首部的\n，' '来分割数组，分割出来的数据分别是日期、开盘、收盘、最高、最低、成交量
                onedayquote = {}
                onedayquote['Date'] = "20" + oneday[0]  # 腾讯股票数据中时间没有20170513中的20，所以这里加上，方便后面比较
                onedayquote['Open'] = oneday[1]  # 开盘
                onedayquote['Close'] = oneday[2]  # 收盘
                onedayquote['High'] = oneday[3]  # 最高
                onedayquote['Low'] = oneday[4]  # 最低
                onedayquote['Volume'] = oneday[5]  # 成交量
                quote_data.append(onedayquote)
            quote['Data'] = quote_data  # 当前股票每天的数据
            # print(quote_data)
            if (not is_retry):
                counter.append(1)

        except:
            print("Error: 加载指定股票的数据失败... " + quote['Symbol'] + "/" + quote['Name'] + "\n")
            if (not is_retry):
                time.sleep(2)
                self.load_quote_data(quote, start_date, end_date, True, counter)  ##这里重试，以免是因为网络问题而导致的下载失败

        print("下载指定股票 " + quote['Symbol'] + "/" + quote['Name'] + " 完成..." + "\n")
        ## print("time cost: " + str(round(timeit.default_timer() - start)) + "s." + "\n")
        ## print("total count: " + str(len(counter)) + "\n")
    return quote



# 获取链接列表
def get_url_list(start,end):
    url_list=[]
    while(start<=end):
        url = '''http://data.eastmoney.com/DataCenter_V3/jgdy/xx.ashx?pagesize=50&page=%d''' %start
        url += "&js=var%20ngDoXCbV&param=&sortRule=-1&sortType=0&rt=48753724"
        url_list.append(url)
        start+=1
    return url_list

# 此处需要设置charset,否则中文会乱码
engine =create_engine('mysql+mysqldb://user:passwd@ip:port/db_name?charset=utf8')
Base =declarative_base()

class jigoudiaoyan(Base):
    __tablename__ = "jigoudiaoyan"
    # 自增的主键
    id =Column(Integer,primary_key=True)
    # 调研日期
    StartDate = Column(Date,nullable=True)
    # 股票名称
    SName =Column(VARCHAR(255),nullable=True)
    # 结束日期 一般为空
    EndDate=Column(Date,nullable=True)
    # 接待方式
    Description =Column(VARCHAR(255),nullable=True)
    # 公司全称
    CompanyName =Column(VARCHAR(255),nullable=True)
    # 结构名称
    OrgName=Column(VARCHAR(255),nullable=True)
    # 公司代码
    CompanyCode=Column(VARCHAR(255),nullable=True)
    # 接待人员
    Licostaff=Column(VARCHAR(800),nullable=True)
    # 一般为空 意义不清
    OrgSum=Column(VARCHAR(255),nullable=True)
    # 涨跌幅
    ChangePercent=Column(Float,nullable=True)
    # 公告日期
    NoticeDate=Column(Date,nullable=True)
    # 接待地点
    Place=Column(VARCHAR(255),nullable=True)
    # 股票代码
    SCode=Column(VARCHAR(255),nullable=True)
    # 结构代码
    OrgCode=Column(VARCHAR(255),nullable=True)
    # 调研人员
    Personnel=Column(VARCHAR(255),nullable=True)
    # 最新价
    Close=Column(Float,nullable=True)
    #机构类型
    OrgtypeName=Column(VARCHAR(255),nullable=True)
    # 机构类型代码
    Orgtype=Column(VARCHAR(255),nullable=True)
    # 主要内容,一般为空 意义不清
    Maincontent=Column(VARCHAR(255),nullable=True)
Session =sessionmaker(bind=engine)
session =Session()
# 创建表
Base.metadata.create_all(engine)
# 获取链接列表


#记录并保存数据
def save_json_data(user_agent_list):
    pages =get_pages_count()
    len_user_agent=len(user_agent_list)
    url_list =get_url_list(1,pages)
    count=0
    for url in url_list:
        request = urllib2.Request(url)
        request.add_header('Referer','http://data.eastmoney.com/jgdy/')
        # 随机从user_agent池中取user
        pos =random.randint(0,len_user_agent-1)
        request.add_header('User-Agent', user_agent_list[pos])
        reader = urllib2.urlopen(request)
        data=reader.read()
         # 自动判断编码方式并进行解码
        encoding = chardet.detect(data)['encoding']
        # 忽略不能解码的字段
        data = data.decode(encoding,'ignore')
        start_pos = data.index('=')
        json_data = data[start_pos + 1:]
        dict = json.loads(json_data)
        list_data = dict['data']
        count+=1
        for item in list_data:
            one = jigoudiaoyan()
            StartDate =item['StartDate'].encode("utf8")
            if(StartDate ==""):
                StartDate = None
            else:
                StartDate = datetime.datetime.strptime(StartDate,"%Y-%m-%d").date()
            SName=item['SName'].encode("utf8")
            if(SName ==""):
                SName =None
            EndDate = item["EndDate"].encode("utf8")
            if(EndDate==""):
                EndDate=None
            else:
                EndDate=datetime.datetime.strptime(EndDate,"%Y-%m-%d").date()
            Description=item['Description'].encode("utf8")
            if(Description ==""):
                Description= None
            CompanyName=item['CompanyName'].encode("utf8")
            if(CompanyName==""):
                CompanyName=None
            OrgName=item['OrgName'].encode("utf8")
            if(OrgName ==""):
                OrgName=None
            CompanyCode=item['CompanyCode'].encode("utf8")
            if(CompanyCode==""):
                CompanyCode=None
            Licostaff=item['Licostaff'].encode("utf8")
            if(Licostaff ==""):
                Licostaff=None
            OrgSum = item['OrgSum'].encode("utf8")
            if(OrgSum ==""):
                OrgSum=None
            ChangePercent=item['ChangePercent'].encode("utf8")
            if(ChangePercent ==""):
                ChangePercent=None
            else:
                ChangePercent=float(ChangePercent)
            NoticeDate=item['NoticeDate'].encode("utf8")
            if(NoticeDate==""):
                NoticeDate=None
            else:
                NoticeDate=datetime.datetime.strptime(NoticeDate,"%Y-%m-%d").date()
            Place=item['Place'].encode("utf8")
            if(Place==""):
                Place=None
            SCode=item["SCode"].encode("utf8")
            if(SCode==""):
                SCode=None
            OrgCode=item['OrgCode'].encode("utf8")
            if(OrgCode==""):
                OrgCode=None
            Personnel=item['Personnel'].encode('utf8')
            if(Personnel==""):
                Personnel=None
            Close=item['Close'].encode("utf8")
            if(Close==""):
                Close=None
            else:
                Close =float(Close)
            OrgtypeName =item['OrgtypeName'].encode("utf8")
            if(OrgtypeName==""):
                OrgtypeName=None
            Orgtype=item['Orgtype'].encode("utf8")
            if(Orgtype==""):
                Orgtype=None
            Maincontent=item['Maincontent'].encode("utf8")
            if(Maincontent==""):
                Maincontent=None
            one.StartDate=StartDate
            one.SName=SName
            one.EndDate=EndDate
            one.Description=Description
            one.CompanyName=CompanyName
            one.OrgName=OrgName
            one.CompanyCode=CompanyCode
            one.Licostaff=Licostaff
            one.OrgSum=OrgSum
            one.ChangePercent=ChangePercent
            one.NoticeDate=NoticeDate
            one.Place=Place
            one.SCode=SCode
            one.OrgCode=OrgCode
            one.Personnel=Personnel
            one.Close=Close
            one.OrgtypeName=OrgtypeName
            one.Orgtype=Orgtype
            one.Maincontent=Maincontent
            session.add(one)
            session.commit()
        print 'percent:' ,count*1.0/pages,"complete!,now ",count
        # delay 1s
        time.sleep(1)

        # user_agent 池
        user_agent_list = []
        user_agent_list.append(
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 ")
        user_agent_list.append(
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50")
        user_agent_list.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")
        user_agent_list.append("Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11")
        user_agent_list.append(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 ")
        user_agent_list.append(
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")

        encoding = chardet.detect(data)['encoding']
        # 忽略不能解码的字段
        data = data.decode(encoding, 'ignore')

        # 获取当前的时间戳
        def get_timstamp():
            timestamp = int(int(time.time()) / 30)
            return str(timestamp)
