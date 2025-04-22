import requests
import json

with open('credentials_instagram.json') as f:
    config = json.load(f)

ACCESS_TOKEN = config["access_token"]
USER_ID = config["ig_user_id"]

def get_post_ids():
    url = f"https://graph.instagram.com/v22.0/{USER_ID}/media?access_token={ACCESS_TOKEN}"

    res = requests.get(url)
    print(res.json())

def get_post_comments():
    url = f"https://graph.instagram.com/v22.0/18047361881582351/comments?fields=id,text,timestamp&access_token={ACCESS_TOKEN}"

    res = requests.get(url)
    print(res.json())

def main():
    #get_post_ids()
    get_post_comments()

if __name__ == '__main__':
    main()


