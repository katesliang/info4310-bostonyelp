import csv
import requests
from os import environ
FILE_NAME = "yelp_boston.csv"

# Creates JSON file that maps each type to pokemon they are super effective attacking against
data = []
fields = ["Name", "Price", "Review", "ReviewRating", "Photo"]

def preprocess(file_name):
    """
    Reads CSV with `file_name` and parses the data into the global `data` dictionary.
    """
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_row = {}
            business_id = row["url"].split("biz/")[1]
            url = "https://api.yelp.com/v3/businesses/" + business_id
            headers = {"accept": "application/json", "Authorization": "Bearer " + environ.get("API_KEY")}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                res_json = response.json()
                if "price" in res_json:
                    new_row["Name"] = res_json["name"]
                    new_row["Price"] = res_json["price"]
                if "photos" in res_json:
                    new_row["Photo"] = res_json["photos"][0]
            else:
                print(response.text)

            review_response = requests.get(url + "/reviews", headers=headers)
            if review_response.status_code == 200:
                res_json = review_response.json()
                print(res_json["reviews"][0])
                new_row["Review"] = res_json["reviews"][0]["text"]
                new_row["ReviewRating"] = res_json["reviews"][0]["rating"]
            else:
                print(review_response.text)

            data.append(new_row)
    
preprocess(FILE_NAME)

# Writing to data.json          
with open('prices.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields)
    writer.writeheader() 
    writer.writerows(data)