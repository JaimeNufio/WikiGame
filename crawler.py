from bs4 import BeautifulSoup 
from lxml import html
import requests
import re

base = 'https://en.wikipedia.org/'
start = '/wiki/coconut'#'wiki/Lythronax'
target = '/wiki/Adolf_Hitler'

scope = '/wiki/'
path = []
known = []
exploreLayer = []
childrenOfExploreLayer = []
explored = []
DFS = 0
requestsCount = 0

def gotThere(location,parent):
    global DFS
    #print("Checking |%s| against |%s|" %(location,target))
    if (location == target):
        DFS+=1
        print("Found %s on DFS level %d [Parent: %s]" %(target,DFS,parent))
        exit(0)

def safety():
    global requestsCount
    #print("Requests %d" %(requestsCount))
    if (requestsCount > 9999999999):
        print("request exit")
        exit(0)

def collectChildrenOfExploreLayer(): #

    global known,exploreLayer,childrenOfExploreLayer,requestsCount,DFS

    print("DFS Layer %s" %(DFS))

    for location in exploreLayer:

        path.append(location)

        #print("Exploring: "+base+location)
        #print("\tRequesting: %s" %(base+location))

        page = requests.get(base+location)
        requestsCount += 1
        #
        #safety()
        title = ""

        if (not page is None):
            soup = BeautifulSoup(page.text,'html.parser')
            if (not soup.find(id='firstHeading') is None):
                title = soup.find(id='firstHeading').text
            else:
                print("Invalid Page: %s" %(location))
                continue
        else:
            print("Null Page: %s" %(location))
            continue

        cnt = 0
        for link in soup.findAll('a',attrs={'href':re.compile("^/wiki.*")}):

            if (not childSeen(link.get('href'))):
                if (preProcess(link.get('href'))):
                    known.append(link.get('href'))
                    continue

                #print("New Child: %s" %(link.get('href')))
                childrenOfExploreLayer.append(link.get('href'))
                known.append(link.get('href'))
                gotThere(link.get('href'),location)
                cnt+=1
            else:
                continue
                #print("\t\tFound duplicate %s, ignoring." %(link.get('href')))
        #
        # print("\tFound %d Child Nodes of \"%s\" at DFS Layer: %s" %(cnt,title,DFS))
        explored.append(link.get('href'))
        
    print("DFS Layer "+str(DFS)+" complete.")
    DFS += 1
    print("\tOf %d nodes, we found %d children." %(len(exploreLayer),len(childrenOfExploreLayer)))
    exploreLayer = childrenOfExploreLayer
    childrenOfExploreLayer = []

def childSeen(location):
    global known, explored
    return (location in known) or (location in explored)


def preProcess(location):
    location = location.lower()
    if (re.search(".*wikimedia.*|.*wikt.*|.*wikibooks.*|.*wikiquote.*|.*wikisource.*|.*wikiversity.*|.*file:.*|.*wikipedia.*|.*help:.*",location)):
        return True
    return False


exploreLayer.append(start)
while(True):
    collectChildrenOfExploreLayer()
    print("Explore Layer targets:")
    #print(exploreLayer[:5])