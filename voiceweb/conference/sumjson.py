import os
import glob
import json

def sum_json_file():
    list=[]
    for filename in glob.glob("voicetext*.json"):
     with open(filename, encoding="UTF-8-sig") as json_file:
        json_data = json.load(json_file)
        for j in json_data["data"] :
         list.append({'name':json_data["name"], "time":j["indata"]["time"],
                      "text":j["indata"]["text"]})
    list = sorted(list, key=lambda k: k["time"])
    print(list)
sum_json_file()