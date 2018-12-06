import requests
from lxml import html
import json
from datetime import datetime as dt
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

#277475225-288016844-271398447-311302841-293723179
print(dt.utcnow())

class Item:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
    def getName(self):
        return self.name
    def getPrice(self):
        return self.price
    def getDescription(self):
        return self.description


def collect_api():
    new_change = False
    current_change = None
    try:
        with open("next-change.id", "r") as nci:
            current_change = nci.read()
            print(current_change)
    except FileNotFoundError:
        current_change = None
    with open("log.txt", "w") as out, open("next-change.id", "r+") as nci:
        
        """
        opt = webdriver.ChromeOptions()
        opt.add_argument('--disable-extentions')
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
        opt.add_argument('--no-sandbox')

        #driver = webdriver.Chrome(chrome_options=opt)
        driver = webdriver.Firefox()
        driver.get("https://poe.ninja/stats")
        print(driver.getCurrentUrl())
        print(driver.page_source)
        poe_ninja_stats = requests.get("https://poe.ninja/stats")
        change_id = driver.find_element(By.XPATH, '//a[contains(@href,"https://api.pathofexile.com/public-stash-tabs")]').text
        #[contains(@href, "https://pathofexile.com/api/public-stash-tabs")]
        print(change_id)
        """
        current_change = nci.read()
        if not current_change:
            data = requests.get('http://api.pathofexile.com/public-stash-tabs')
        else:
            data = requests.get('http://api.pathofexile.com/public-stash-tabs?id=' + current_change)

        info = data.json()
        nc = info.get('next_change_id')
        nci.seek(0)
        nci.truncate()
        nci.write(info.get("next_change_id"))


        #Pauses to constantly update, could pull from updated source instead

        valid = requests.get('http://api.pathofexile.com/public-stash-tabs?id='+nc)
        iters = 0
        count = 0
        while valid and count < iters:
            count+=1
            nc = valid.json().get('next_change_id')
            print(nc)
            valid = requests.get('http://api.pathofexile.com/public-stash-tabs?id='+nc)
            nci.seek(0)
            nci.truncate()
            nci.write(nc)

        log = ""
        stashes = info.get("stashes")
        flag = True
        for tab in stashes:
            items = []
            tab_info = {'accountName': tab.get('accountName'), 'lastCharacterName': tab.get('lastCharacterName'), 'id':tab.get('id'), 'stash':tab.get('stash'), 'league':tab.get('league')}
            if flag:
                flag = True
            if tab.get('public') == True and tab.get('stashType') == "PremiumStash" and tab.get('league') != "Standard" or tab.get('league') != "Hardcore":
                for item in tab.get('items'):
                    if not item.get('league') == "Standard" and not item.get('league') == "Hardcore" and 'maps' in item.get('category'):
                        items.append(item)
                    #items.append(item)
                if(items != []):
                    tab_info['items'] = items
                    log += json.dumps(tab_info)
        item_list = []
        for st in stashes:
            if st.get('public') and tab.get('stashType') == "PremiumStash":
                items = process_stash(st, ["maps"])
                item_list.extend(items)
        item_dumper(item_list, 10)
        out.write(log)

def process_stash(stash, types):
    owner = stash.get("lastCharacterName")
    stash_name = stash.get("stash")
    stash_price = None
    if "~price" in stash_name:
        stash_price = stash_name[7:]
    league = stash.get("league")
    if league == "Hardcore":
        return []
    item_list = []
    for item in stash.get("items"):
        useful_item = False
        for category in types:
            if category in item.get('category'):
                useful_item = True
                print("?")
                break

        if useful_item:
            desc = ""
            price = ""
            name = ""

            if 'note' in item and "~price" in item.get('note'):
                price_note = item.get('note')
                quant = re.findall('[0-9]+', price_note)
                currency = re.findall('[a-z]+', price_note[7:])
                price = quant[0] + " " + currency[0]

            if 'identified' not in item or item.get('identified') == False:
                desc += "Unidentified "
            if 'corrupted' in item:
                desc += "Corrupted "
                
            if "maps" in item.get('category'):
                if "properties" in item:
                    tier = item.get('properties')[0].get('values')[0]
                    desc += "Tier " + str(tier) + " "
                map_type = item.get("typeLine")
                words = re.findall('[A-Z][^A-Z]*', map_type)
                for word in words:
                    name += word + " "
                desc += name

            item = Item(name, price, desc)
            item_list.append(item)

    return item_list

def item_dumper(item_list, items_to_print):
    for i in range(items_to_print):
        if i < len(item_list):
            item = item_list[i]
            print(item.getName(), " at ", item.getPrice(), ". ", item.getDescription())

collect_api()
            


            
