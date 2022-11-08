import json
import requests
import time

# User Inputs:

usertoken = input("Glossary owner's token: ")
community_uuid = input("API5 Community UUID: ")
community_id = input("API4 Community ID: ")
fromglossary = input("Name of old glossary to be replaced: ")
toglossary = input("Name of new glossary replacing: ")

# Housekeeping.

cookie = {"Cookie":"tms_prod_community={0}; tms_auth_token={1}".format(community_id, usertoken)}
calls = 0    # for tracking how many APIs have run

# Grab all the glossaries.

glossarylist = json.loads(requests.get("https://myaccount.lingotek.com/api/glossary?limit=1000", headers={"Authorization":"Bearer {0}".format(usertoken)}).text)
calls += 1

while True:
    oldmaster = ""
    newmaster = ""
    for i in glossarylist["entities"]:
        if i["properties"]["title"] == fromglossary:
            oldmaster = i["properties"]["id"]
        if i["properties"]["title"] == toglossary:
            newmaster = i["properties"]["id"]
    if len(newmaster) > 0 and len(oldmaster) > 0:
        break
    else:
        input("Missing old/new pair. Please ensure both glossaries exist. Press enter to try again, or restart script to re-enter names.")

# Grab all the projects. Currently just grabs a limit 1000, but can be increased if need be. Running limit 10000 actually works, but seems like overdoing it.

projectlist = json.loads(requests.get("https://myaccount.lingotek.com/api/project?limit=1000&community_id={0}".format(community_uuid), headers={"Authorization":"Bearer {0}".format(usertoken)}).text)
calls += 1
time.sleep(1)    # rate limiting to one per second

# inactiveprojects list excludes many known inactive projects from the list of projects to modify, without needing to check the project with a slower api.
# This makes this a little bit faster if you want to exclude projects and have a LOT to check through, but I won't include it as an input().

inactiveprojects = []
activeprojects = []

for i in projectlist["entities"]:
    if i["properties"]["id"] not in inactiveprojects:
        activeprojects.append(i["properties"]["id"])
        print(i["properties"]["title"])
        
print("Checking {0} projects for old glossary.".format(len(activeprojects)))

# These are the API4 requests made within the TMS itself when you add or remove a glossary from a project.
# Fortunately, API4 accepts API5 UUIDs which makes this easier.

for i in activeprojects:
    projectGlossaries = json.loads(requests.post("https://myaccount.lingotek.com/lingopoint/api/4/getProjectGlossaries", headers = cookie, data={"projectId":"{0}".format(i)}).text)
    calls += 1
    time.sleep(1)    # rate limiting to one per second
    for j in projectGlossaries["glossaries"]:
        if j["name"] == fromglossary:    # If present, add and then remove old.
            requests.post("https://myaccount.lingotek.com/lingopoint/api/4/AddProjectDictionary", headers = cookie, data = {"project_id":i,"dictionary":newmaster})
            calls += 1
            time.sleep(1)    # rate limiting to one per second
            requests.post("https://myaccount.lingotek.com/lingopoint/api/4/RemoveProjectDictionary", headers = cookie, data = {"project_id":i,"dictionary":oldmaster})
            calls += 1
            time.sleep(1)    # rate limiting to one per second

input("Done. {0}".format(str(calls)))
