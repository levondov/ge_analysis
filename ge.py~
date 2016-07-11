import json
import requests
from lxml import html
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import time
import datetime

# shark, barrow tab, 
ITEMS = [385,19629]

all_items = open('items.json')
all_items = json.load(all_items)

def ge_price(item_id):
    api_url = 'https://api.rsbuddy.com/grandExchange?a=guidePrice&i=' + str(item_id)
    page = requests.get(api_url)
    tree = html.fromstring(page.content)
    item_json = tree.xpath('//body//text()')[0].split(':')
    overall = item_json[1][:-9]
    buying = item_json[2][:-17]
    buying_Q = item_json[3][:-10]
    selling = item_json[4][:-18]
    selling_Q = item_json[5][:-1]
    return (overall,buying,buying_Q,selling,selling_Q)

def grab_data():
	# grab data and save to txt file
	for item in ITEMS:
		fname = 'item_' + str(item) + '.txt'
		try:
			a = open(fname, 'r')
			a.close()
			a = open(fname, 'a')
		except:
			a = open(fname, 'w')
		temp = ge_price(item)
		temp = str(temp[0]) + ',' + str(temp[1]) + ',' + str(temp[2]) + ',' + str(temp[3]) + ',' + str(temp[4] + ',' + str(time.time()) + '\n')
		a.write(temp)
		a.close()
	# try to plot data
	try:
		plot_data()
	except:
		print 'error graphing'
	
def plot_data():
	# plot data
	for item in ITEMS:
		# import and format data
		fname = 'item_' + str(item) + '.txt'
		data = np.genfromtxt(fname,dtype='float',delimiter=',')
		data_t = data[:,5]
		data_b = data[:,1]
		data_bq = data[:,2]
		data_s = data[:,3]
		data_sq = data[:,4]
		
		# grab name of item for graph title
		item_title = 'Item ID not found in database'
		for all_item in all_items:
			if all_item['id'] == item:
				item_title = all_item['name']
				
		# format time
		s = data_t/1000.0
		dts = map(datetime.datetime.fromtimestamp, s)
		fds = dates.date2num(dts)
		hfnt = dates.DateFormatter('%m/%d %H:%M:%S')
		
		# plot data
		f, ax = plt.subplots(2, sharex=True, figsize=(10,6))
		ax[0].grid(True)
		ax[0].set_title(item_title)
		ax[0].plot(fds,data_b,marker='o')
		ax[0].plot(fds,data_s,marker='o')
		ax[0].legend(('buy','sell'),loc=6)
		ax[0].set_ylabel('gp')
		ax[0].xaxis.set_major_formatter(hfnt)
		ax[1].grid(True)
		ax[1].plot(fds,data_bq,marker='o')
		ax[1].plot(fds,data_sq,marker='o')
		ax[1].legend(('buy','sell'),loc=6)	
		ax[1].set_xlabel('time')
		ax[1].set_ylabel('amount')
		ax[1].xaxis.set_major_formatter(hfnt)
		f.autofmt_xdate()
		plt.savefig('item_' + str(item) + '.png')
    
# make html file to display graphs in webpage
f = open('html_graph.txt','w')
for item in ITEMS:
	temp = "<img src=\"item_" + str(item) + ".png\">" + "<br>"
	f.write(temp)
f.close()

while True:
	grab_data()
	time.sleep(5)
    
