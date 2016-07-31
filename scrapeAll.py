
"""
dependencies:
npm
phantom.js
selenium
"""

import csv
import requests
import selenium
import sys
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import time


# driver methods
# get elements from the phantom's html
def getElement(parent,key,value):
    element = False
    try:
        element = {
            'id'   :  lambda x: parent.find_elements_by_id(x),
            'class':  lambda y: parent.find_elements_by_class_name(y),
            'css'  :  lambda z: parent.find_elements_by_css_selector(z),
            'name' :  lambda a: parent.find_element_by_name(a)
        }[key](value)
    except selenium.common.exceptions.NoSuchElementException:
        print "Could not find element."

    return element

# page navigation methods
# a function to extract the desired data from the urls
def dataCap(driver,url):
    string = ""
    # parent element (li.searchresult)
    bullets = getElement(driver,'css','li.searchresult')
    for li in bullets:
        a        = ''
        href     = ''
        des      = ''
        metaInfo = ''
        try:
            # url (a) get href 0
            a    = getElement(li,'css','a')[0]
            href = str(a.get_attribute("href"))
            # description 1
            des = str(a.text)
        except:
            try:
                if getElement(driver,'css','h2')[0].text == 'Error':
                    print "I found a server error"
                else:
                    print "unknown try error"
            except:
                print "unknown except error"
        try:
            # all other elements from here down are in (p.metaInfo)
            metaInfo = str(getElement(li,'css','p.metaInfo')[0].text)
        except:
            print "I am error"
            pass

        data = metaInfo + " | " + des + " | " + href
        string = string + data + "-^-"
    return string

# a function that clicks 'date decided' and submits this result
def decideAndSearch(driver):
    try:
        radio = getElement(driver,'id','dateDecided')[0]
        radio.click()
        form = getElement(driver,'css','#monthlyListForm')[0]
        submit = getElement(form,'css','input.button')[0]
        submit.click()
    except:
        print 'radio click error'

# a function that captures the number of pages
def pageNum(driver):
    try:
        container = getElement(driver,'id','searchResultsContainer')[0]
        return len(getElement(container,'css','a.page'))/2 + 1
    except:
        return 0


# recursive methods
# function that creates new phantom browser instances and calls neccesarry page navigation methods to retrieve data
def drive_Spider(url,output):
    storage = str(url) + "-^-"

    name = mp.current_process().name
    driver = webdriver.PhantomJS(executable_path='<INSERT_PHANTOM_JS_PATH>')

    print name, 'Starting'

    driver.get(url)
    decideAndSearch(driver)

    pagen = pageNum(driver)
    for i in range(1, pagen+1):
        try:
            url = url.replace('search.do?action=monthlyList','pagedSearchResults.do?action=page&searchCriteria.page='+str(2))
            driver.get(url.replace('monthlyListResults.do?action=firstPage','pagedSearchResults.do?action=page&searchCriteria.page='+str(2)))
            data = dataCap(driver,url.replace('monthlyListResults.do?action=firstPage','pagedSearchResults.do?action=page&searchCriteria.page='+str(2)))
            storage = storage + data
        except:
            print "I had to continue, page failed to load."
            continue

    print storage
    driver.quit()
    output.put(storage)

    print name, 'leaving'

# capture url's to be scraped from the google docs sheet
def request_Doc():
    data = requests.get("ENTER_G_SHEET")
    #"https://docs.google.com/spreadsheets/d/1YJWH5up2sinNY7YubqJ_VbmqAR_Lj5xYmbd_ChqPjdY/edit#gid=0
    soup = BeautifulSoup(data.text, "html.parser")
    return [i.contents[0] for i in soup.select('td.s3 > div.softmerge-inner')]

# parse data strings captured from phantom into a more usable data structure
def parser(string):
    return [i.split("|") for i in string.split("-^-")]

def prettifyText(string):
    string = string.replace('Ref. No:','')
    string = string.replace('Status:','')
    string = string.replace('Validated:','')
    string = string.replace('Received:','')
    return string.strip()

# function used to write data to the csv file
def write2Csv(data):
    # dictionary provides a reference to the city corresponding to each url
    dictionary = {
        'http://paplan.lbbd.gov.uk/online-applications/search.do?action=monthlyList': [0,'Barking and Dagenham'],
        'https://publicaccess.barnet.gov.uk/online-applications/search.do?action=monthlyList': [1,'Barnet'],
        'http://pa.bexley.gov.uk/online-applications/search.do?action=monthlyList':[2,'Bexley'],
        'https://pa.brent.gov.uk/online-applications/search.do?action=monthlyList':[3,'Brent'],
        'https://searchapplications.bromley.gov.uk/onlineapplications/search.do?action=monthlyList':[4,'Bromley'],
        'http://publicaccess2.croydon.gov.uk/online-applications/search.do?action=monthlyList':[5,'Croydon'],
        'https://pam.ealing.gov.uk/online-applications/search.do?action=monthlyList':[6,'Ealing'],
        'http://planningandbuildingcontrol.enfield.gov.uk/online-applications/search.do?action=monthlyList':[7,'Enfield'],
        'https://planning.royalgreenwich.gov.uk/online-applications/search.do?action=monthlyList':[8,'Greenwich'],
        'http://public-access.lbhf.gov.uk/online-applications/search.do?action=monthlyList':[9,'Hammersmith and Fulham'],
        'http://planning.lambeth.gov.uk/online-applications/search.do?action=monthlyList':[10,'Lambeth'],
        'http://planning.lewisham.gov.uk/online-applications/search.do?action=monthlyList':[11,'Lewisham'],
        'https://pa.newham.gov.uk/online-applications/search.do?action=monthlyList':[12,'Newham'],
        'http://planbuild.southwark.gov.uk:8190/online-applications/search.do?action=monthlyList':[13,'Southwark'],
        'https://development.towerhamlets.gov.uk/online-applications/search.do?action=monthlyList':[14,'Tower Hamlets'],
        'http://idoxpa.westminster.gov.uk/online-applications/search.do?action=monthlyList':[15,'Westminster'],
        'http://www.planning2.cityoflondon.gov.uk/online-applications/search.do?action=monthlyList':[16,'City of London']
    }
    key = [data[0]]

    out_file = open("sa.csv", "wb")
    writer = csv.writer(out_file)
    for arr in data:
        for row in range(len(arr)):
            if row == 0:
                try:
                    writer.writerow([dictionary[arr[row][0]][1]])
                except:
                    print "There was an error"
            elif row == 1:
                writer.writerow(['Reference Number','Recieved','Validated','Status','Description','Url'])
                writer.writerow(map(prettifyText,arr[row]))
            else:
                writer.writerow(map(prettifyText,arr[row]))
    out_file.close()
    return

def main():

    start = time() # reference time, used to calculate script running time
    output = mp.Queue() # data structure storing sub process results

    if len(sys.argv) > 1:
        urls = request_Doc()[0:int(sys.argv[1])] # urls scraped from google docs
    else:
        urls = request_Doc()
        
    processes = [mp.Process(target=drive_Spider, args=(url, output)) for url in urls] # list of web scraping proccesses

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()
        p.terminate()

    # list of formatted output from queue, write this data to the csv file
    product = [parser(output.get()) for i in range(len(processes))]
    write2Csv(product)

    # print the reults and running time
    print product
    print "\n",float(time()-start)/60,"\n"

if __name__ == "__main__":
    main()
