#!/usr/bin/python

# Download US Fed Rate and perform sensitivity analysis
# Author: ttoleung@gmail.com
#

from datetime import datetime
import urllib2
import MySQLdb as mdb
import sys

def rate_url():
	i = datetime.now()
	url = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%20' + str(i.month) + '%20and%20year(NEW_DATE)%20eq%20' + str(i.year)
	return url

def get_www_content(url):
	response = urllib2.urlopen(url)
	html = response.read()
	return html

def extract_value(line,offset):
	start_index = line.index('>')
	end_index = line.index('</')
	return line[start_index+1:end_index-offset]

def get_sql(html):
	state = 0
	marker = 0
	key_rate = [0,0,0,0,0,0,0,0,0,0,0]
	sql_list = []
	for l in list(iter(html.splitlines())):
		line = l.strip()
		if state != 0:
			key_rate[marker] = extract_value(line,0)
			if marker == 10:
				sql = "INSERT INTO rates (rate_date, y1m, y3m, y6m, y1y, y2y, y3y, y5y, y7y, y10y, y20y, y30y) VALUES " \
					+ "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
					(key_date, key_rate[0], key_rate[1], key_rate[2], key_rate[3], key_rate[4], key_rate[5], key_rate[6], key_rate[7], key_rate[8], key_rate[9], key_rate[10])
				sql_list.append(sql)
				state = 0
			marker = marker + 1
		elif 'NEW_DATE' in line:
			key_date = extract_value(line,9)
			state = 1
			marker = 0
	return sql_list

def sql_insert(sql_list):
	con = mdb.connect('localhost', 'eclipse', 'eclipse', 'monsuke');
	cur = con.cursor()
	for sql in sql_list:
		try:
			cur.execute(sql)
			print 'Inserted for ' + sql[97:107]
		except mdb.IntegrityError:
			con.rollback()
			print 'key date already existed for ' + sql[97:107]
	con.close()

html = get_www_content(rate_url())
sql_list = get_sql(html)
sql_insert(sql_list)
