
from lxml import html
import requests
import time


# def get_file(which_file):
#     data_dir = '.\\data\\'    
#     url = 'http://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=' + which_file +'&Order=Yes'
#     resp = requests.get(url)
#     with open(data_dir + which_file + '.txt', 'wb') as pbf:
#         pbf.write(resp.content)


def get_file(which_game, ordered='No', fname='newdata'):
    data_dir = '.\\data\\'    
    url = 'http://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=' + which_game +'&Order=' + ordered
    resp = requests.get(url)
    with open(data_dir + fname + '.txt', 'wb') as pbf:
        pbf.write(resp.content)


def parse_file(which_file):
    data_dir = '.\\data\\'    
    with open(data_dir + which_file + '.txt', 'rt', encoding='UTF-8') as raw_file:
        lines = raw_file.readlines()
    return lines


def parse_line(line):
    ln_len = len(line[:5].strip())
    ln = int(line[:5])
    dts = line[ln_len+5:ln_len+22]
    dt =  time.strptime(dts, '%a. %b %d, %Y') # Sat. Nov 11, 2017
    num_txt = line[ln_len+32:].split(' ')
    nums = []
    for n in num_txt:
        if '' == n or '\n' == n:
            next
        else:
            nums.append(int(n))
    return [str(str(dt.tm_mon) + '/' + str(dt.tm_mday) + '/' + str(dt.tm_year)), 'game-' + str(ln)] + nums


def mkcsv(fname):
    data_dir = '.\\data\\'
    hdr_size = -5
#    get_file(game, 'Yes', fname)
    lines = list(reversed(parse_file(fname)))
    with open(data_dir + fname + '.csv', 'wt') as csvfile:
        for line in lines[:hdr_size]:
            csvfile.write(",".join(list(map(str, parse_line(line)))))
            csvfile.write("\n")


# fnames = ['powerball', 'mega-millions', 'superlotto-plus']
# for name in fnames:
#     mkcsv(name)
fn = {'powerball':'pball', 'mega-millions':'mega', 'superlotto-plus':'sball'}
for game,fname in fn.items():
    get_file(game,'Yes',fname)
    mkcsv(fname)