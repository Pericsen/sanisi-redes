import requests
import json
import pandas as pd

with open('credentials_instagram.json') as f:
    config = json.load(f)

ACCESS_TOKEN = config["access_token"]
USER_ID = config["ig_user_id"]

def get_recent_posts(limit=100):
    url = f"https://graph.instagram.com/v22.0/{USER_ID}/media"
    
    params = {
        "fields": "id,caption,timestamp",
        "limit": limit,
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params)
    return res.json().get("data", [])

def get_comments(media_id):
    comments = []

    url = f"https://graph.instagram.com/v22.0/{media_id}/comments"

    params = {
        "fields": "id, username, like_count, text, timestamp",
        "access_token": ACCESS_TOKEN
    }

    while url:
        res = requests.get(url, params=params)
        data = res.json().get("data", [])
        comments.extend(data)
        url = res.json().get("paging", {}).get("next")
        params = {}

    return comments

def comments_to_csv(comments_dict, filename="comments.csv"):
    flat_data = []

    for post_id, comment_list in comments_dict.items():
        for comment in comment_list:
            flat_data.append({
                "post_id": post_id,
                "comment_id": comment.get("id"),
                "username": comment.get("username"),
                "comment_text": comment.get("text"),
                "like_count": comment.get("like_count"),
                "timestamp": comment.get("timestamp")
            })

    df = pd.DataFrame(flat_data)
    df.to_csv(filename, index=False)

def main():
    posts = get_recent_posts(limit=100)
    all_comments = {}

    for post in posts:
        media_id = post["id"]
        print(f"Descargando comentarios de {media_id}")
        comments = get_comments(media_id)
        all_comments[media_id] = comments

    comments_to_csv(all_comments)
    print("Comentarios guardados en comments.csv")

if __name__ == '__main__':
    main()


