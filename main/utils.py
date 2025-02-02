'''
Fetch the test questions and answers using open trivia database api for tests
'''

import requests

def fetch_categories():
    url = "https://opentdb.com/api_category.php"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["trivia_categories"]
    else:
        return []

def fetch_questions(category_id):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": 25,  # Number of questions
        "type": "multiple",  # Multiple-choice questions
        "category": category_id,  # Category ID
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        return []