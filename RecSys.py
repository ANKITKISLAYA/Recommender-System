# -*- coding: utf-8 -*-
"""
Created on Tue Jan  15 11:30:37 2020

@author: Ankit Kislaya
"""


#program is for generating top n recommendations from stored cosine similarity matrix which will be called by myapp.py


import pandas as pd
from pymongo import MongoClient 
from collections import defaultdict
from operator import itemgetter 


class RecSys:
    
    def rec(self,itemid,number):
        
        citem = int(itemid)    # This is the itemid against whom recommendations are to be generated
        number = int(number)   # Number of recommendations to be generated 
        l=[]
        l1=[]
		
		# connect to mongodb collection (RecSysItem) where cosine similarity is stored 
		
        conn = MongoClient('192.168.1.101', 27017)
        mydb = conn.ankit_database
        collection = mydb.RecSysItem
        
		# Below is reading similarity row for itemid 1 to generate recommendations  for new item which is not present in our similarity matrix   
        df1 = pd.DataFrame(list(collection.find( { 'itemid' :1 })))
        df2 = df1.drop(['_id' , 'itemid'], axis = 1)
        df3 = df2.sort_values(0, axis=1, ascending=False, inplace=False, kind='quicksort', na_position='last') # sort itemid's (i.e column names) based on score values in row and store in df3
        l1 = list(df3.columns.values)  # take column values (i.e sorted item id's based on score ) store it in the list 
        l1 = [int(i) for i in l1]
        
        
        
        
        if (citem in l1): # if itemid passed is in our stored similarity matrix then proceed
		
			# get the row of citem and create dictionary of itemid's and it's scores
            df = pd.DataFrame(list(collection.find( { 'itemid' : citem })))  
            df1 = df.drop(['_id' , 'itemid'], axis = 1)
            lcolumn = list(df1.columns.values)
            lcolumn = [int(i) for i in lcolumn]
            lvalue = list(df1.iloc[0])
            mapped = zip(lcolumn , lvalue)
            lis = list(mapped)
            candidates = defaultdict(float)

            for itemid, score in lis:
                candidates[itemid] = score
				
            			
			# sort the dictionary and generate top n recommendations
            pos = 0
            for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
                if (itemID != citem ):
                    l.append(itemID)
                    pos += 1
                    if (pos > number-1):
                        break
            return tuple(l)
        
        else: # for new item generating top n popular (based on scores of itemid 1 already stored) as recommendations
            l = l1[:number]
            return tuple(l)





