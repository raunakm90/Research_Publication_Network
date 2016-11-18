
# coding: utf-8

# # Connections of Top Authors and their network

# In[13]:

from __future__ import division
from __future__ import print_function
# The %... is an iPython thing, and is not part of the Python language.
# In this case we're just telling the plotting library to draw things on
# the notebook, instead of on a separate window.
get_ipython().magic(u'matplotlib inline')
import os
os.getcwd()
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd
import time
import csv
from collections import Counter
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.notebook_repr_html', True)
import seaborn as sns
sns.set_style("whitegrid")


import random
from PIL import Image
from os import path
from nltk.corpus import stopwords
from scipy.misc import imread
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from wordcloud import WordCloud, STOPWORDS

import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error

import plotly
import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
plotly.tools.set_credentials_file(username='raunakm90', api_key='qh9wd16d6g')

import plot_network
import plotly.plotly as py
from plotly.graph_objs import *
#sns.set_context("poster")

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# ## Import data from SQL database

# In[2]:

import mysql_setup
query_list,field_names = mysql_setup.query_with_fetchmany("SELECT * FROM Author")
Author = mysql_setup.make_frame(query_list,field_names)


# In[3]:

query_list,field_names = mysql_setup.query_with_fetchmany("SELECT * FROM Publishing_Detail")
Publishing_Detail = mysql_setup.make_frame(query_list,field_names)


# ## Extract top authors and their corresponding publications

# In[4]:

ind = Author.Author_Cited_By.sort_values(ascending = False).index
# Select top 4 indices
ind = ind[0:4]
top_Authors = Author[Author.index.isin(ind)]
a_dict = top_Authors.set_index('Author_Id')['Author_Name'].to_dict()
top_Authors


# In[5]:

#Key_Value pair of author id and author name
a_dict


# In[6]:

#Get the publications of the required authors
a_id = a_dict.keys()
DB_NAME = 'NLP_Project'
in_p=', '.join(list(map(lambda x: '%s', a_id)))
sql = ("SELECT * FROM publishing_Detail WHERE Author_Id in (%s)")
sql = sql % in_p
query_list = list()
cnx = mysql.connector.connect(user='root',password = "raunak")
cursor = cnx.cursor()
cnx.database = DB_NAME
cursor.execute(sql,a_id)

for row in iter(cursor):
        query_list.append(row)
        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description]
        field_names
        
cursor.close()
cnx.close()
Author_Pubs = mysql_setup.make_frame(query_list,field_names)
Author_Pubs.head()


# In[7]:

# Publication of the first author
pubs = Author_Pubs[Author_Pubs['Author_Id']==a_id[0]]


# ## Create author networks

# Collect all co-authors for a given author's publication and count how many times they have co-authored a paper. This way create a adjacency matrix for all connections between the author and his co-authors as well as amongst the co-authors. This will show how the co-authors are connected as well.

# For each graph, hover over the nodes to get details related to that node. Yet to add edge strength (for some reason it seems to be way more complicated than imagined). The size and the colour of the node vary according to the number of connections or the degree of the node.

# In[8]:

# All the co-authors of a given author
x = pubs['Pub_Authors'].tolist()
x_authors = ",".join(unicode(i) for i in x if not i.isdigit())
x_authors = x_authors.lower()

#Create adjacency matrix of author connections
x_authors = set(x_authors.split(","))
adj_mat = pd.DataFrame(0, index=x_authors, columns=x_authors)
for authors in x:
    temp = authors.lower().split(",")
    if len(temp)>1:
        for i in range(0,len(temp)-1):
            j=0
            while j <= len(temp)-1:
                adj_mat[temp[i]][temp[j]] = adj_mat[temp[i]][temp[j]]+1
                j +=1
                
Gr=nx.from_numpy_matrix(adj_mat.values)

G = ((source, target, attr) for source, target, attr in 
                Gr.edges_iter(data=True) if attr['weight'] > 1)
new_network = nx.Graph()
new_network.add_edges_from(G)


position=nx.spring_layout(new_network)
labels = adj_mat.columns[new_network.nodes()]

traceE=plot_network.scatter_edges(new_network, position)
traceN=plot_network.scatter_nodes(new_network,position,labels = labels)

fig = Figure(data=Data([traceE, traceN]),
             layout=Layout(
                title='<br>Network graph - Robert Tibshirani',
                titlefont=dict(size=18),
                showlegend=False, 
                width=1000,
                height=1000,
                margin=dict(b=20,l=5,r=5,t=40),
                hovermode='closest',
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

iplot(fig, filename='Robert Tibshirani')


# In[9]:

# Publication of the first author
pubs = Author_Pubs[Author_Pubs['Author_Id']==a_dict.keys()[1]]
pubs.head()

# All the co-authors of a given author
x = pubs['Pub_Authors'].tolist()
x_authors = ",".join(unicode(i) for i in x if not i.isdigit())
x_authors = x_authors.lower()

#Create adjacency matrix of author connections
x_authors = set(x_authors.split(","))
adj_mat = pd.DataFrame(0, index=x_authors, columns=x_authors)
for authors in x:
    temp = authors.lower().split(",")
    if len(temp)>1:
        for i in range(0,len(temp)-1):
            j=0
            while j <= len(temp)-1:
                adj_mat[temp[i]][temp[j]] = adj_mat[temp[i]][temp[j]]+1
                j +=1

Gr=nx.from_numpy_matrix(adj_mat.values)

G = ((source, target, attr) for source, target, attr in 
                Gr.edges_iter(data=True) if attr['weight'] > 1)
new_network = nx.Graph()
new_network.add_edges_from(G)


position=nx.spring_layout(new_network)
labels = adj_mat.columns[new_network.nodes()]
     
traceE=plot_network.scatter_edges(new_network, position)
traceN=plot_network.scatter_nodes(new_network,position,labels = labels)

fig = Figure(data=Data([traceE, traceN]),
             layout=Layout(
                title='<br>Network graph - '+str(a_dict.values()[1]),
                titlefont=dict(size=18),
                showlegend=False, 
                width=1000,
                height=750,
                margin=dict(b=20,l=5,r=5,t=40),
                hovermode='closest',
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

iplot(fig, filename=str(a_dict.values()[1]))


# In[10]:

# Publication of the first author
pubs = Author_Pubs[Author_Pubs['Author_Id']==a_dict.keys()[2]]
pubs.head()

# All the co-authors of a given author
x = pubs['Pub_Authors'].tolist()
x_authors = ",".join(unicode(i) for i in x if not i.isdigit())
x_authors = x_authors.lower()
temp = x_authors.split(",")
print (temp.count(str(a_dict.values()[2])))

#Create adjacency matrix of author connections
x_authors = set(x_authors.split(","))
adj_mat = pd.DataFrame(0, index=x_authors, columns=x_authors)
for authors in x:
    temp = authors.lower().split(",")
    if len(temp)>1:
        for i in range(0,len(temp)-1):
            j=0
            while j <= len(temp)-1:
                adj_mat[temp[i]][temp[j]] = adj_mat[temp[i]][temp[j]]+1
                j +=1

Gr=nx.from_numpy_matrix(adj_mat.values)

G = ((source, target, attr) for source, target, attr in 
                Gr.edges_iter(data=True) if attr['weight'] > 1)
new_network = nx.Graph()
new_network.add_edges_from(G)


position=nx.spring_layout(new_network)
labels = adj_mat.columns[new_network.nodes()]
     
traceE=plot_network.scatter_edges(new_network, position)
traceN=plot_network.scatter_nodes(new_network,position,labels = labels)

fig = Figure(data=Data([traceE, traceN]),
             layout=Layout(
                title='<br>Network graph - '+str(a_dict.values()[2]),
                titlefont=dict(size=18),
                showlegend=False, 
                width=1000,
                height=750,
                margin=dict(b=20,l=5,r=5,t=40),
                hovermode='closest',
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

iplot(fig, filename=str(a_dict.values()[2]))


# In[11]:

# Publication of the first author
pubs = Author_Pubs[Author_Pubs['Author_Id']==a_dict.keys()[3]]
pubs.head()

# All the co-authors of a given author
x = pubs['Pub_Authors'].tolist()
x_authors = ",".join(unicode(i) for i in x if not i.isdigit())
x_authors = x_authors.lower()
temp = x_authors.split(",")
print (temp.count(str(a_dict.values()[3])))

#Create adjacency matrix of author connections
x_authors = set(x_authors.split(","))
adj_mat = pd.DataFrame(0, index=x_authors, columns=x_authors)
for authors in x:
    temp = authors.lower().split(",")
    if len(temp)>1:
        for i in range(0,len(temp)-1):
            j=0
            while j <= len(temp)-1:
                adj_mat[temp[i]][temp[j]] = adj_mat[temp[i]][temp[j]]+1
                j +=1

Gr=nx.from_numpy_matrix(adj_mat.values)

G = ((source, target, attr) for source, target, attr in 
                Gr.edges_iter(data=True) if attr['weight'] > 1)
new_network = nx.Graph()
new_network.add_edges_from(G)


position=nx.spring_layout(new_network)
labels = adj_mat.columns[new_network.nodes()]
     
traceE=plot_network.scatter_edges(new_network, position)
traceN=plot_network.scatter_nodes(new_network,position,labels = labels)

fig = Figure(data=Data([traceE, traceN]),
             layout=Layout(
                title='<br>Network graph - '+str(a_dict.values()[3]),
                titlefont=dict(size=18),
                showlegend=False, 
                width=1000,
                height=750,
                margin=dict(b=20,l=5,r=5,t=40),
                hovermode='closest',
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

iplot(fig, filename=str(a_dict.values()[3]))


# ## Conclusion

# Ideally, these graphs should be like following: One center node of the main author (on whose basis we extract the publications) and connections from that node to the rest of the network or to his co-authors. Currently, because of difference in spellings and the way names are used, we dont see every node connected. We need partial matching of strings, which will bring in it's own errors. 
