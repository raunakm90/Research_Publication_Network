# -*- coding: utf-8 -*-
"""
Created on Sat May 21 11:46:30 2016

@author: Raunak Mundada
"""


import sys
sys.path.insert(0,'D:\NLP_Project')
import scholarly_edit

def extractAuthorProfiles():
    # Define a list of authors
    author_list = ['Monnie McGee']
    #Author_Detail = {}
    Author_Detail = []
    Pub_Detail = []
    
    for i in author_list:
        apub_detail = []
        a_obj = next(scholarly_edit.search_author(i)).fill()
        
        #Author_Detail.update({id : (a_obj.name,a_obj.affiliation, a_obj.email,a_obj.interests,a_obj.citedby)})
        Author_Detail.append([str(a_obj.id),str(a_obj.name),str(a_obj.affiliation), str(a_obj.email),
                              str(",".join(a_obj.interests)),a_obj.citedby])
        
              
        apub_detail = extractPublish(a_obj)
        #apub_detail.extend([a_obj.id,a_obj.name])
        
        Pub_Detail.append(apub_detail)
        
        
    return Author_Detail,Pub_Detail
    
    
#a_obj.publications[0].get_citedby() - get the articles citing the given publication
def extractPublish(a_obj):
    Pub_Detail = []
    
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
            pub.bib['year'] = temp
        if hasattr(pub,'citedby') == False:
            setattr(pub,'citedby',-99)
                 
        #print pub
        #Pub_Detail.append([pub.id_citations.partition(':')[0],pub.bib['title'], pub.bib['author'],
         #                  pub.bib['publisher'],pub.bib['abstract2'], pub.bib['volume'], pub.bib['year'], 
          #                  pub.citedby ,pub.bib['url']])
        Pub_Detail.append([pub.id_citations.partition(':')[2],pub.bib['title'], pub.bib['author'],
                           pub.bib['publisher'],pub.bib['abstract2'], pub.bib['volume'], pub.bib['year'], 
                            pub.citedby ,pub.bib['url'],pub.id_citations.partition(':')[0]])
    return Pub_Detail
    
'''
Pub_Detail = []
x = extractAuthorProfiles()
'''
'''
for pub in all_pub:
    Pub_Detail.append([pub.bib['title'], pub.bib['author'], pub.bib['publisher'],
                   pub.bib['abstract'], pub.bib['volume'], pub.bib['year'], 
                   pub.citedby ,pub.bib['url']])
'''

