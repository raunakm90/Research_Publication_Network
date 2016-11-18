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
    Pub_Detail = []
    # Assign NA to non-existent columns
    
    for pub in a_obj.publications:
        # Assign NA to non-existent columns
        if pub.source = 'citations':
          title = pub.bib['title']
          print title
          search_q = scholarly_edit.search_pubs_query(title)
          scholar_pub = next(search_q)
          if scholar_pub.bib['ENTRYTYPE'] == 'article':
            Pub_Detail.append([article.pub['journal_id'],a.bib['title'],a.bib['author'],
              a.bib['journal'],a.bib['publisher'],a.bib['abstract'],a.bib['volume'],a.bib['year'],a.citedby,
              a.bib['url']])
      
        Pub_Detail.append([pub.id_citations.partition(':')[2],pub.bib['title'], pub.bib['author'],
                       pub.bib['publisher'],pub.bib['abstract2'], pub.bib['volume'], pub.bib['year'], 
                        pub.citedby ,pub.bib['url'],pub.id_citations.partition(':')[0]])

    return Pub_Detail

# Convert SQL query into a pandas data frame
def make_frame(list_of_tuples, legend):
    framelist=[]
    for i, cname in enumerate(legend):
        framelist.append((cname,[e[i] for e in list_of_tuples]))
    return pd.DataFrame.from_items(framelist)


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
          pub_list = extractPublish(author)
          #print ("Publishing list extracted")
          author_list.append([str(author.id),str(author.name),str(author.affiliation), str(author.email),
                                    str(",".join(author.interests)),author.citedby,author.hIndex,author.i_10_index,
                                    author.hIndex_recent,author.i_10_index_recent])
          #print (pub_list)
          mysql_setup.updateTables(author_list,pub_list)
          count +=1
          
  print("--- %s seconds ---" % (time.time() - start_time))
      