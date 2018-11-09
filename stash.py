import requests
import json
from datetime import datetime as dt

#277475225-288016844-271398447-311302841-293723179
print(dt.utcnow())
new_change = False
current_change = None
try:
    with open("next-change.id", "r") as nci:
        current_change = nci.read()
        print(current_change)
except FileNotFoundError:
    current_change = None
with open("log.txt", "w") as out, open("next-change.id", "r+") as nci:
    if not current_change:
        data = requests.get('http://api.pathofexile.com/public-stash-tabs')
    else:
        data = requests.get('http://api.pathofexile.com/public-stash-tabs?id=' + current_change)

    info = data.json()
    nc = info.get('next_change_id')
    nci.write(info.get("next_change_id"))
    print(info.get("next_change_id"))
    valid = requests.get('http://api.pathofexile.com/public-stash-tabs?id='+nc)
    while valid:
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
            print(tab_info)
            flag = False
        if tab.get('public') == True and tab.get('stashType') == "PremiumStash" and tab.get('league') != "Standard" or tab.get('league') != "Hardcore":
            for item in tab.get('items'):
                if not item.get('league') == "Standard" and not item.get('league') == "Hardcore" and 'maps' in item.get('category'):
                    items.append(item)
                #items.append(item)
            if(items != []):
                tab_info['items'] = items
                log += json.dumps(tab_info)
    out.write(log)

