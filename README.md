#Python Data Scraper
##Version 1.0

Set up:
runs with python 2.7
modules/ dependencies
1. phantomJs
2. selenium
3. requests
4. bs4
5. multiprocessing

PhantomJs is a headless browser used to power the browser automation involved in this script.  If you do not have it downloaded, first download the node package manager and node js from here, https://www.npmjs.com/.  once you have npm installed you can simply type 
“npm install phantomjs-prebuilt”, into your terminal (no quotes). This will download phantom and provide you with a directory path (*** take note of this path, the script needs it for the phantomJs webdriver***).  I have attached an image called insertPath.png, this is the location where you need to copy your phantomJs path (delete my path, within the quotes and copy yours).  After you have pasted you are up and running with a phantomJs web driver.

For the Python modules:
use pip to add bs4, requests, selenium, and multiprocessing

Description:
This script scrapes all urls in columnC from the following google document, https://docs.google.com/spreadsheets/d/1YJWH5up2sinNY7YubqJ_VbmqAR_Lj5xYmbd_ChqPjdY/edit#gid=0,and proceeds to capture all application listing data.  It only works for the current month.  It scrapes all pages containing listings for each url.

Run Time:
the first two urls and all subpages took (17-18 min) to fully scrape.  Some urls load way faster than others.  Some urls have way more data than others.  For instance the first url can be fully scraped in about 30s.  The remaining 16.5 min is for page 2!  I’m approximating the full running time to be anywhere from 3-5 hours.  