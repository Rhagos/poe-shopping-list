import requests
import json
import time
with open("next-change.id", "r+") as nci:
    current_change = nci.read()
    data = requests.get('http://api.pathofexile.com/public-stash-tabs?id='+current_change)
    info = data.json()
    while info.get('next_change_id') != current_change:
        current_change = info.get('next_change_id')
        data = requests.get('http://api.pathofexile.com/public-stash-tabs?id='+current_change)
        info = data.json()
        nci.seek(0)
        nci.truncate()
        nci.write(current_change)
        time.sleep(0.5)
    print(current_change)
    nci.seek(0)
    nci.truncate()
    nci.write(current_change)
