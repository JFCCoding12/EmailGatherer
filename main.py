import pandas as pd
import re
import requests
from itertools import product
from string import ascii_lowercase
import time
import sys


'''
Replace campus value with following codes

ALL (All umaine)
UM  (UMaine)
USM
UMA
UMF
UMFK 
UMM
UMPI
UMS
'''
def search(chars, filename):   
    url = 'https://peoplesearch.maine.edu/'
    data = {
    'campus': 'UM',  # <=== This is the code you change depending what campus you want to seach in
    'q': chars,
    'submit': 'Search for Faculty/Staff'
    }
    try:
        x = requests.post(url, data = data)
        html = x.text
    except:
        print(" "*100, end="\r")
        for i in range(20):
            print("Connection refused by the server.. Waiting",20-i,"seconds ", end='\r')
            time.sleep(1)
        print(" "*100, end="\r")
        print("Now let me continue...", end='\r')
        x = requests.post(url, data = data)
        html = x.text

    temp =  re.findall("Sorry, the search resulted in zero matches.", html)
    holder = ""
    if len(temp) == 0:
        try:
            dfs = pd.read_html(html)
        except:
            return
        df = dfs[0]
        for i in range(len(df.Email)):
            file1 = open(filename, "a+")
            with open(filename) as myfile:
                if df.Email[i] in myfile.read():
                    holder = "no"
                else:
                    file1.write(df.Email[i]+"\n") 
            file1.close() 

    else:
       holder = "no"

start_time = time.time()
keywords = [a+b+c for a,b,c in product(ascii_lowercase, repeat=3)]
total = len(keywords)
done = 0
filename = time.strftime("%Y_%m_%d-%H_%M_%S_%p.csv") 
f= open(filename,"w+")
f.write("email\n")
f.close()
print("="*10, "JFC Coding UMaine Email Scrapper - Version 1.0 - jfccoding.com", "="*10,"\n\n")
for i in keywords:
    print("Currently Searching with: ",i , " -- ",format(done,',d') ," out of ", format (total, ',d'), "--", round((done/total)*100, 2) ,"%" ,"finished", end="\r")
    search(i, filename)
    done = done + 1
print("                                                                                                                      ", end="\r")
print("Finished in ", time.time() - start_time, " seconds")
