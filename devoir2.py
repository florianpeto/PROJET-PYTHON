import base64
import csv
import datetime
import hashlib
import json
import os
import random
import requests
import secrets
import string
import urllib.parse
import uuid
from pathlib import Path

def generate_safe_password(length: int) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_not_safe_password(length: int) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def encode_url(url: str) -> str:
    return urllib.parse.quote(url, safe='')

def hash_md5(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()

def process_json_data(json_data: dict) -> dict:
    for product in json_data['products']:
        product['my_date'] = datetime.datetime.now().isoformat()
        product_json_str = json.dumps(product)
        product['my_json_data_in_base64'] = base64.b64encode(product_json_str.encode()).decode()
        product['my_encoded_thumbnail'] = encode_url(product['thumbnail'])
        product['uuid_version_4'] = str(uuid.uuid4())
        product['all_these_images_urls_hashes'] = hash_md5('!::!'.join(product['images']))
        product['very_safe_password'] = generate_safe_password(8)
        product['totally_not_safe_password'] = generate_not_safe_password(8)

    return json_data

def download_and_process_data(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()

    json_data = response.json()
    return process_json_data(json_data)

def write_to_csv(data: dict, file_path: Path) -> None:
    with open("Florian_Junior_PETO_MY_FILE.csv" , 'w', newline='\n') as csvfile:
        fieldnames = data['products'][0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for product in data['products']:
            writer.writerow(product)

def main():
    json_url = "https://dummyjson.com/products"

    json_data = download_and_process_data(json_url)

    file_name = f"Florian_Junior_PETO_MY_FILE.csv"  
    file_path = Path("devoir2")

    write_to_csv(json_data, file_path)

Florian_Junior = "Florian_Junior"
PETO = "PETO"
main()
