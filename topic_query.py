# -*- coding: utf-8 -*-
"""
Created on Sat May 21 14:01:04 2016

@author: Raunak Mundada
"""

from BeautifulSoup import  BeautifulSoup as bs4
import requests
import time
import re
import mysql_setup


'''
class queryResult():
    def __init__(self,qr):
        author = []
        pub_journal = []
        year = []
        url = []
        urlText = []
        pub_details = []
        abstract = []
        cite = []

        for div in qr:
            temp = bs4(str(div.findAll("div",{"class":"gs_ri"})))
            url.append( temp.find('a')['href']) # get the url
            urlText.append(temp.find('a').text) # get the title of the url
            pub_details.append (bs4(str(div.findAll("div", {"class":"gs_a"}))).text) # get publishing details
            abstract.append(bs4(str(div.findAll("div", {"class":"gs_rs"}))).text) #get abstract of publication
            cite.append(bs4(str(div.findAll("div",{"class":"gs_fl"}))).find('a').text) #get number of citations
            
        for pub in pub_details:
            temp = pub.split('-')
            author.append(temp[0])
            year.append(temp[1])
            try:
                pub_journal.append(temp[2])
            except:
                pub_journal.append('NA')
                
        self.url = url
        self.urlText = urlText
        self.abstract = abstract
        self.cite = re.sub("[A-Z,a-z]","",str(cite))
        self.author = author
        self.pub_journal = pub_journal
        self.year = year
    
    def __str__(self):
        print "Class created"
''' 
class queryResult():
    def __init__(self,qr):
        self.bib = dict()

        for div in qr:
            temp = bs4(str(div.findAll("div",{"class":"gs_ri"})))
            self.bib['url'] = ( temp.find('a')['href']) # get the url
            self.bib['title'] = (temp.find('a').text) # get the title of the url
            self.bib['Publisher'] = (bs4(str(div.findAll("div", {"class":"gs_a"}))).text) # get publishing details
            self.bib['abstract'] = (bs4(str(div.findAll("div", {"class":"gs_rs"}))).text) #get abstract of publication
            self.bib['citedby'] = (bs4(str(div.findAll("div",{"class":"gs_fl"}))).find('a').text) #get number of citations
            
        for pub in pub_details:
            temp = pub.split('-')
            author.append(temp[0])
            year.append(temp[1])
            try:
                pub_journal.append(temp[2])
            except:
                pub_journal.append('NA')
                
        self.url = url
        self.urlText = urlText
        self.abstract = abstract
        self.cite = re.sub("[A-Z,a-z]","",str(cite))
        self.author = author
        self.pub_journal = pub_journal
        self.year = year
    
    def __str__(self):
        print "Class created"
def addQuotes(s):
    return '"{}"'.format(s)
    
def searchResults(topic, n = None):
    queryRes = []
    query = addQuotes(topic)
    
    if n is None:
        n = 10
    for i in range(0,n): 
        # url to scrape 
        url_scrape = 'https://scholar.google.com/scholar?start=%d0'%i+'&q=%s'%query+'&hl=en&as_sdt=0,44'
        
        #add delay between requests
        time.sleep(0)
        # get the html data
        html = requests.get(url=url_scrape)
        # Convert html text to beautiful soup object
        soup = bs4(html.text)
        '''
        f = open('TopicQuery_HTML.txt','wb')
        f.write(str(soup))
        f.close()
        '''

        # Get the query results from html page
        q_table = soup.findAll ("div", {"class" : "gs_r"})
        q = queryResult(q_table)
        


queryRes = searchResults('machine learning',n=1)

           
    
        