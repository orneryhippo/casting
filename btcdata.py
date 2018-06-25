import requests
from lxml import html
from time import strptime
from datetime import datetime as dtm
from datetime import timedelta as td

def mk_url(coin, start, end):
    url = "https://coinmarketcap.com/currencies/" + coin + "/historical-data/?start="+ start + "&end=" + end
    return url

def mk_dtstrs(dt):
    ds = str(dt.year)+str(dt.month)+str(dt.day)
    ys = str(dt.year-1)+str(dt.month)+str(dt.day)
    return ys,ds

# d is today, y is one year ago today
y,d = mk_dtstrs(dtm.today())

urlb = mk_url("bitcoin", y, d)
urle = mk_url("ethereum",y, d)
urll = mk_url("litecoin", y, d)
urlx = mk_url("ripple", y, d)

def get_table(u):
    result = requests.get(u)
    tree = html.fromstring(result.text)
    tbl = tree.xpath('//div[@class="table-responsive"]/table')
    tbody = tbl[0][1]
    return tbody

def to_date(sdate):
    return strptime(sdate, "%b %d, %Y")

def to_date_s(sdate):
    d = strptime(sdate, "%b %d, %Y")
    return str(d.tm_year) +"-"+ str(d.tm_mon) +"-"+ str(d.tm_mday)


def tbody_to_list(tbody):
    ohlc = [["Date","Open","High","Low","Close"]]
    for tr in tbody:
        ohlc.append([to_date_s(tr[0].text), float(tr[1].text),float(tr[2].text),float(tr[3].text),float(tr[4].text)])
    return ohlc

def list_to_csv(fname,ohlc):
    with open(fname,"w") as b:
        for line in ohlc:
            b.write(",".join(list(map(str,line)))+"\n")


list_to_csv("bitcoin.csv", tbody_to_list(get_table(urlb)))
list_to_csv("ripple.csv", tbody_to_list(get_table(urlx)))
list_to_csv("litecoin.csv", tbody_to_list(get_table(urll)))
list_to_csv("ethereum.csv", tbody_to_list(get_table(urle)))
