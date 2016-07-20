import matplotlib
matplotlib.use('Agg')
import json
import requests
from lxml import html
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import time
import datetime

all_items = open('items.json')
all_items = json.load(all_items)

def item_list():
	return np.genfromtxt('ITEMS.txt',delimiter=',',dtype='int')

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
		
		# find index for points up to last 24 hours
		data_t = data[:,5]
		last_24 = time.time() - 3600*24
		index = 0
		for i,times in enumerate(data_t):
			if times >= last_24:
				index = i
				break
		data_t = data[index:,5]		
		data_b = data[index:,1]
		data_bq = data[index:,2]
		data_s = data[index:,3]
		data_sq = data[index:,4]
		
		# grab name of item for graph title
		item_title = 'Item ID not found in database'
		for all_item in all_items:
			if all_item['id'] == item:
				item_title = all_item['name']
				break
			else:
				item_title = "ID: " + str(item) + " name not found in database"
				
		# format time
		s = (data_t - 3600*8)
		dts = map(datetime.datetime.fromtimestamp, s)
		fds = dates.date2num(dts)
		hfnt = dates.DateFormatter('%m/%d %H:%M:%S')
		
		# plot data
		f, ax = plt.subplots(2, sharex=True, figsize=(10,6))
		ax[0].grid(True)
		ax[0].set_title(item_title)
		ax[0].plot(fds,data_b,marker='.')
		ax[0].plot(fds,data_s,marker='.')
		ax[0].legend(('buy','sell'),loc=6)
		ax[0].set_ylabel('gp')
		ax[0].xaxis.set_major_formatter(hfnt)
		ax[1].grid(True)
		ax[1].plot(fds,data_bq,marker='.')
		ax[1].plot(fds,data_sq,marker='.')
		ax[1].legend(('buy','sell'),loc=6)	
		ax[1].set_xlabel('time')
		ax[1].set_ylabel('amount')
		ax[1].xaxis.set_major_formatter(hfnt)
		f.autofmt_xdate()
		plt.savefig('item_' + str(item) + '.png')
		plt.close('all')

while True:
	# check txt file for new items and generate html file to display graphs in webpage
	f = open('html_graph.txt','w')
	ITEMS = item_list()
	for item in ITEMS:
		temp = "<img src=\"item_" + str(item) + ".png\">" + "<br>"
		f.write(temp)
	f.close()

	# grab item data and generate plots
	print 'updating graphs....'
	try:
		grab_data()
	except:
		print 'something went wrong'
	time.sleep(30)
    
