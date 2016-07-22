#retrieves the latest winners from the winning-numbers page
from __future__ import print_function

from lxml import html
import requests
from datetime import datetime
#
page = requests.get('http://www.calottery.com/win/winning-numbers')

tree = html.fromstring(page.content)


# get all the winning numbers in an array of strings
wn = tree.xpath('//ul[@class="winning_number"]//li//span/text()')

# split out and convert text to ints
#wn = map(int, wn)
pb =  wn[:6]
mega = wn[6:12]
sup = wn[12:18]

#pb = map(int, wn[:6])
#mega = map(int, wn[6:12])
#sup = map(int, wn[12:18])

t = datetime.today().strftime("%Y-%m-%d")

print( "Today is",  datetime.today().strftime("%A, %d %b %Y"))

print( t,"pb",pb)
print( t,"mega",mega)
print( t,"super",sup)

# write to the database...

# get prize amounts
def get_prize(draw = 'powerball'):
	if draw == 'powerball':
		game = draw
		txt = "Powerball"
	if draw == 'mega':
		game = 'mega-millions'
		txt = 'MegaMillions'
	if draw == 'super':
		game = 'superlotto-plus'
		txt = "Superlotto"
	page = requests.get('http://www.calottery.com/play/draw-games/' + game)
	tree = html.fromstring(page.content)
	prize = tree.xpath('//div[@class="heroContentBox drawGameHero"]/h2/text()')
	return "Next " + txt + " prize: " + str(prize[0])

print(get_prize('powerball'))
print( get_prize('mega'))
print( get_prize('super'))