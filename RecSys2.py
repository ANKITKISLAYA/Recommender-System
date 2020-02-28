# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:31:07 2020

@author: Ankit Kislaya
"""

# program is for generating top n recommendations from stored cosine similarity matrix and filtering item's on warehouse id where customer belongs

import pandas as pd
from pymongo import MongoClient 
from collections import defaultdict
from operator import itemgetter 


class RecSys2:
    
    def rec(self,itemid,number,wid):
        
        citem = int(itemid)        # This is the itemid against whom recommendations are to be generated
        number = int(number)       # Number of recommendations to be generated
        wid = int(wid)             # the warehouse id in which the customer belongs 
        l=[]
        l1=[]
        
        # connect to mongodb collection (RecSysItem) where cosine similarity matrix and collection (ItemWarehouse) where 
        # items present in each warehouse are stored.
        conn = MongoClient('192.168.1.101', 27017)
        mydb = conn.ML
        mydb1 = conn.ankit_database
        collection = mydb.RecSysItem
        collection1 = mydb1.ItemWarehouse
        
        # storing the items based on warehouseid passed 
        dfw = pd.DataFrame(list(collection1.find({ 'WarehouseId' :wid })))
        lw = dfw.iloc[0,0]
         
        
        # Below is reading similarity row for itemid 1 to generate recommendations  for new item which is not present in our similarity matrix  
        df1 = pd.DataFrame(list(collection.find( { 'itemid' :1 })))
        df2 = df1.drop(['_id' , 'itemid'], axis = 1)
        df3 = df2.sort_values(0, axis=1, ascending=False, inplace=False, kind='quicksort', na_position='last') # sort itemid's (i.e column names) based on score values in row and store in df3
        l1 = list(df3.columns.values)   # take column values (i.e sorted item id's based on score ) store it in list 
        l1 = [int(i) for i in l1]
        
        
        
        
        if (citem in l1):  # if itemid passed is in our stored similarity matrix then proceed
            
            # get the row of citem and create dictionary of itemid's and it's scores
            df = pd.DataFrame(list(collection.find( { 'itemid' : citem })))
            df12 = df.drop(['_id' , 'itemid'], axis = 1)
            df13 = df12.sort_values(0, axis=1, ascending=False, inplace=False, kind='quicksort', na_position='last')
            l12 = list(df13.columns.values)
            l12 = [int(i) for i in l12]
            
            # sort the dictionary and generate top n recommendations
            pos = 0
            for itemID in l12:
                if ((itemID != citem) & (itemID in lw)):
                    l.append(itemID)
                    pos += 1
                    if (pos > number-1):
                        break
                l = [int(i) for i in l]  
            return tuple(l)
        
        else:   # for new item generating top n popular (based on scores of itemid 1 which is already stored) as recommendations
            for i in l1:
                if (i in lw):
                    l.append(i)
            
                if (len(l) > number):
                    break
            return tuple(l)





