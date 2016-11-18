# -*- coding: utf-8 -*-
"""
Created on Sun May 29 15:02:27 2016

@author: Raunak Mundada
"""

import sys
import scholarly_edit
import mysql_setup
import multiprocessing
from multiprocessing import Pool #for parallel processing
import time
import pandas as pd
import random

if __name__ == '__main__':
	journal_name = 'phy_probabilitystatistics'
	i = 1
	count = 0
	article_list = list()
	journal_list = list()
	# Generator object at _search_journal_soup
	query = scholarly_edit.search_topJournal(journal_name)
	for item in query:

		if not count == i:
			#print item
			q = item.fill() # Extract articles in the journal
			journal_list.append([q.pub['journal_id'],q.pub['title'],q.pub['h5_index'],
				q.pub['h5_median'],q.pub['url']])

			for article in q.articles:
				time.sleep(5+random.uniform(0, 5))
				pubList = article.fill().pubList
				print (pubList)
				#a = pubList[0].fill()
				#print (a)
				'''
				for i in range(0,len(pubList)):
					a = pubList[i].fill()
					print (a)
					
					if a.bib['ENTRYTYPE'] == 'article':
						article_list.append([article.pub['journal_id'],a.bib['title'],a.bib['author'],
							a.bib['journal'],a.bib['publisher'],a.bib['abstract'],a.bib['volume'],a.bib['year'],a.citedby,
							a.bib['url']])
					'''
				#article_list.append(a)
	#print (article_list,journal_list)


