import csv
import requests
import json
from time import sleep
import re

patternInfo = re.compile(r'(itemId|value|limit|members) [\' \']*= (\w*)')
patternPrices = re.compile(r'([\d]+):([\d]+)(:([\d]+))?')
baseURLItemNames="https://oldschool.runescape.wiki/api.php?action=query&list=categorymembers&cmtitle=Category:Tradeable_items&format=json"
baseURLPrices="https://oldschool.runescape.wiki/api.php?action=parse&prop=wikitext&format=json&page=Module:Exchange/"

Indices=None
indicesSet=False

custom_agent = {
    'User-Agent': 'pick_a_username',
    'From': 'provide_an_email_address'
}

parametersItemNames = {
    'action': 'query',
    'list': 'categorymembers',
    'format': 'json',
    'cmtitle': 'Category:Tradeable_items',
    'cmlimit' : 20
}


parametersItemGeneral = {
    'action': 'parse',
    'prop': 'wikitext',
    'format': 'json'
}

def test_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def populateItemInfo(mainList, mylist, mystr):
    i = 2
    for m in re.finditer(patternInfo, mystr):
        if m.group(1)=='itemId':
            if test_int(m.group(2)):
                mylist[0] = int(m.group(2))
            else:
                return
        else:
            if m.group(1)=='members':
                mylist[4] = str(m.group(2))
            else:
                if test_int(m.group(2)):
                    mylist[i] = int(m.group(2))
                else:
                    return
            i+=1
    mylist[5] = mylist[2]*0.6
    mylist[6] = mylist[2]*0.4
    mainList.append(mylist)

def populateItemPrices(prices, volume, itemID, mystr):
    labelsOne = ['itemId']
    labelsTwo = ['itemId']
    if indicesSet:
        itemPrices = [-1] * len(prices[0])
        itemPrices[0] = itemID
        itemVolumes = [-1] * len(prices[0])
        itemVolumes[0] = itemID
    else:
        itemPrices = [itemID]
        itemVolumes = [itemID]
    splitted = None
    for m in re.finditer(patternPrices, mystr):
        if test_int(m.group(1)):
            epoch = int(m.group(1))
            if not indicesSet:
                labelsOne.append(epoch)
                labelsTwo.append(epoch)
            if m.group(3)!=None:
                if test_int(m.group(4)):
                    if not indicesSet:
                        itemVolumes.append(int(m.group(4)))
                    else:
                        if epoch in Indices:
                            itemVolumes[Indices[epoch]] = int(m.group(4))
                else:
                    return
            if m.group(3)==None:
                if not indicesSet:
                    itemVolumes.append(-1)
            if test_int(m.group(2)):
                if not indicesSet:
                    itemPrices.append(int(m.group(2)))
                else:
                    if epoch in Indices:
                        itemPrices[Indices[epoch]] = int(m.group(2))
            else:
                return
        else:
            return
    if not indicesSet:
        prices.append(labelsOne)
        volume.append(labelsTwo)
    prices.append(itemPrices)
    volume.append(itemVolumes)

def writeToCSV(fp, mydata):
    with open(fp, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(mydata)

if __name__ == "__main__":
    tableOne = [['itemId','itemName','Value','Limit','Members','hiAlch','lowAlch']]
    tableTwo = []
    tableThree = []
    itemExists = True
    data = None
    nextpage = ""
    count=0
    while itemExists:
        sleep(1)
        if len(tableOne)!=1:
            parametersItemNames['cmcontinue'] = nextpage
        data = requests.get('https://oldschool.runescape.wiki/api.php', headers=custom_agent, params=parametersItemNames).json()
        if 'continue' in data:
            nextpage = data['continue']['cmcontinue']
        item = ""
        print "processed: "+str(count)+"\n"
        for x in data['query']['categorymembers']:
            if count==1:
                Indices = dict(map(lambda t: (t[1], t[0]), enumerate(tableTwo[0])))
                indicesSet = True
            sleep(1)
            infoList = [0]*7
            item = x['title']
            infoList[1] = str(item)
            parametersItemGeneral['page'] = 'Module:Exchange/' + str(item)
            print str(item)
            dataOne = requests.get('https://oldschool.runescape.wiki/api.php', headers=custom_agent, params=parametersItemGeneral).json()
            if not ('error' in dataOne):
                populateItemInfo(tableOne, infoList, dataOne['parse']['wikitext']['*'])
                sleep(1)
                parametersItemGeneral['page'] = 'Module:Exchange/' + str(item) + '/Data'
                dataTwo = requests.get('https://oldschool.runescape.wiki/api.php', headers=custom_agent, params=parametersItemGeneral).json()
                if not ('error' in dataTwo):
                    populateItemPrices(tableTwo, tableThree, infoList[0], dataTwo['parse']['wikitext']['*'])
            count+=1
        if not ('continue' in data):
            itemExists = False
    writeToCSV('path_to_save_item_info', tableOne)
    writeToCSV('path_to_save_item_prices_info', tableTwo)
    writeToCSV('path_to_save_item_volume_info', tableThree)
