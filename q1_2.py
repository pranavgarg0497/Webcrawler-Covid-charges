from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them

maxNumUrl = 500; #set the maximum number of urls to visit

res = {}
counter = 0
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl and counter < 20:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        # print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    if 'charges' in str(webpage).lower():
        print('Word matched for url=' + curr_url)
        res[curr_url] = 'charges'
        counter += 1
        
        
    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        
        if 'https://www.sec.gov/news/press-release' in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

print(res)