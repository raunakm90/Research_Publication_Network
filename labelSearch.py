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


def extractPublish(a_obj):
    Pub_list = []
    journal_list = []
    # Assign NA to non-existent columns
    
    for i in a_obj.publications:
        # Assign NA to non-existent columns
        pub = i.fill()
        temp = 'NULL'
        if pub.bib.has_key("volume") == False:
            pub.bib['volume'] = temp
        if pub.bib.has_key("publisher") == False:
            pub.bib['publisher'] = temp
        if pub.bib.has_key("author") == False:
            pub.bib['author'] = temp
        if pub.bib.has_key("url") == False:
            pub.bib['url'] = temp
        if pub.bib.has_key['journal'] == False:
          pub.bib['journal'] = temp
            
        if pub.bib.has_key("abstract") == True:
            if not isinstance(pub.bib['abstract'],unicode):
                #print type(pub.bib['abstract'])
                pub.bib['abstract2'] = pub.bib['abstract'].text
            elif isinstance(pub.bib['abstract'],unicode):
                pub.bib['abstract2'] = pub.bib['abstract']
        else:
            pub.bib['abstract2'] = temp
            
            
        if pub.bib.has_key("title") == False:
            pub.bib['title'] = temp
        if pub.bib.has_key("year") == False:
            pub.bib['year'] = -99
        if hasattr(pub,'citedby') == False:
            setattr(pub,'citedby',-99)

        if pub.bib.has_key['journal'] == True:
          journalTitle = pub.bib['journal']
          search_query = scholarly_edit.search_journal(journalTitle)
          journal_item = next(search_query)
          journal_list.append([journal_item.pub['journal_id'],journal_item.pub['title'],journal_item.pub['h5_index'],
            journal_item.pub['h5_median'],journal_item.pub['url']])

        Pub_list.append([pub.id_citations.partition(':')[2],pub.bib['title'], pub.bib['author'],
                       pub.bib['publisher'],pub.bib['journal'],pub.bib['abstract2'], pub.bib['volume'], pub.bib['year'], 
                        pub.citedby ,pub.bib['url'],pub.id_citations.partition(':')[0],journal_list.pub['journal_id']])
    return Pub_list,journal_list

# Extract authors based on label search on google scholar
if __name__ == '__main__':
  i = 1 # Number of authors/search results to access
  count = 0
  search_query = scholarly_edit.search_keyword('operations_research')
  start_time = time.time()
  for item in search_query:
      if not count == i:
          print item
          author_list = []
          mysql_setup.mysqlConn() # set up mysql connections, database and tables
          author = item.fill()
          #print author
          Pub_Details = extractPublish(author)
          #print ("Publishing list extracted")
          author_list.append([str(author.id),str(author.name),str(author.affiliation), str(author.email),
                                    str(",".join(author.interests)),author.citedby,author.hIndex,author.i_10_index,
                                    author.hIndex_recent,author.i_10_index_recent])
          #print (pub_list)
          #mysql_setup.updateTables(author_list,pub_list)
          count +=1
          
  print("--- %s seconds ---" % (time.time() - start_time))
      
