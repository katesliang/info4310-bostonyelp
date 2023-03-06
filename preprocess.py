import csv, json
import requests
from os import environ
FILE_NAME = "yelp_boston.csv"

# Creates JSON file that maps each type to pokemon they are super effective attacking against
data = []
fields = ["Name", "Price"]

def preprocess(file_name):
    """
    Reads CSV with `file_name` and parses the data into the global `data` dictionary.
    """
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            business_id = row["url"].split("biz/")[1]
            url = "https://api.yelp.com/v3/businesses/" + business_id
            headers = {"accept": "application/json", "Authorization": "Bearer " + environ.get("API_KEY")}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                res_json = response.json()
                if "price" in res_json:
                    data.append({"Name": res_json["name"], "Price": res_json["price"]})
            else:
                print(response.text)
                
    
preprocess(FILE_NAME)

# Writing to data.json          
with open('prices.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields)
    writer.writeheader() 
    writer.writerows(data)