import csv
import json

csvFilePath = "testcsv.csv"
jsonFilePath = "testjson.json"

data = {}

with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        id = rows['Ingredient']
        data[id] = rows

#create json file and write data into it
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))

