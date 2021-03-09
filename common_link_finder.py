import argparse
import re
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager
import csv
#parse the file and check for errors in url
def filehandle(path):
    urllist=[]
    file1 = open(path, 'r')
    for line in file1:
        #print(isValidURL(line.strip()))
        #print("Line{}: {}".format(count, line.strip()))
        if not isValidURL(line.strip()):
           print("wrong url: ",line.strip())
           print("pls check and rerun again")
           return False
        else:
            urllist.append(line.strip())
    file1.close()
    return urllist


    
def isValidURL(str):
    # Regex to check valid URL 
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty 
    # return false
    if (str == None):
        return False
 
    # Return if the string 
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False
#find the feqencncy of all tags
def findtags(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'lxml')
    #print(soup)
    #print("LINK TAGS:")
    d=dict()
    #tags=soup.find_all('a').contents[0]
    #print(tags)
    #print(tags.contents[0])
    #anchor_freq(str(tags))
    for link in soup.find_all('a'):
        if link.string:
            #print(link.string)
            #word=link.string.encode("utf-8")
            word=str(link.string)
            if word in d: 
                # Increment count of word by 1 
                d[word] = d[word] + 1
            else: 
                # Add the word to dictionary with count 1 
                d[word] = 1
    #print(d)
    csvfile(d,url)
#write data to csv file
def csvfile(d,url):
    writer=csv.writer(open("report.csv",'a',encoding="utf-8"),lineterminator='\n')
    for key, value in d.items():
        writer.writerow([url,key,value])
#create csv file with headers        
def createfile():
    fields = ['href', 'anchor_text', 'total_occurence']
    with open("report.csv", 'w',encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields,lineterminator='\n') 
        writer.writeheader() 


#main
if __name__ == "__main__":     
    parser=argparse.ArgumentParser()
    parser.add_argument("path", help="File path")
    parser.add_argument("n",help="number of process", type=int)
    args=parser.parse_args()
    path=args.path
    createfile()
    urllist=filehandle(path)
    if urllist:
        p=Pool(args.n)
        p.map(findtags,urllist)
        p.close()
        p.join()
