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

# page = requests.get('http://www.calottery.com/play/draw-games/powerball')
# page = requests.get('http://www.calottery.com/play/draw-games/superlotto-plus')
# page = requests.get('http://www.calottery.com/play/draw-games/mega-millions')

#'http://www.calottery.com/sitecore/content/Miscellaneous/download-numbers/?GameName=powerball&Order=Yes'
#pb = map(int, wn[:6])
#mega = map(int, wn[6:12])
#sup = map(int, wn[12:18])

t = datetime.today().strftime("%Y-%m-%d")

print( "Today is",  datetime.today().strftime("%A, %d %b %Y"))

print( t,"p",pb)
print( t,"m",mega)
print( t,"s",sup)

# write to the database...

# get prize amounts
def get_prize(draw = 'powerball'):
	if draw == 'powerball':
		game = draw
		txt = "p" # "Pball"
	if draw == 'mega':
		game = 'mega-millions'
		txt = "m" # 'Mega'
	if draw == 'super':
		game = 'superlotto-plus'
		txt = "s" # "Super"
	page = requests.get('http://www.calottery.com/play/draw-games/' + game)
	tree = html.fromstring(page.content)
	prize = tree.xpath('//div[@class="heroContentBox drawGameHero"]/h2/text()')
	return "Next " + txt + ": " + str(prize[0]).split(" ")[0][1:] + "M"

print(get_prize('powerball'))
print( get_prize('mega'))
print( get_prize('super'))
input("Press any key...")