import requests
import json
import pandas as pd

with open('credentials_instagram.json') as f:
    config = json.load(f)

ACCESS_TOKEN = config["pages_access_token"]
PAGE_ID = config["page_id"]
API_VERSION  = 'v22.0'
BASE_URL     = f'https://graph.facebook.com/{API_VERSION}'

def paginate(url, params):
    items = []
    while url:
        resp = requests.get(url, params=params).json()
        items.extend(resp.get('data', []))
        url = resp.get('paging', {}).get('next')
        params = {}  # sólo el primer request lleva params
    return items

def get_page_posts(limit=2):
    """
    Devuelve lista de posts con contador de shares, comments y reactions.
    """
    url = f'{BASE_URL}/{PAGE_ID}/posts'
    params = {
        'fields': ','.join([
            'id',
            'message',
            'created_time',
            'shares.summary(true)',
            'comments.summary(true).limit(0)',
            'reactions.summary(true).limit(0)'
        ]),
        'limit': limit,
        'access_token': ACCESS_TOKEN
    }
    return paginate(url, params)

def get_comments_for_post(post_id, limit=2):
    """
    Devuelve lista de comentarios con autor, texto, timestamp y like_count.
    """
    url = f'{BASE_URL}/{post_id}/comments'
    params = {
        'fields': 'id,from,message,created_time,like_count',
        'limit': limit,
        'access_token': ACCESS_TOKEN
    }
    return paginate(url, params)

def build_comments_df(post_limit=2, comment_limit=2):
    posts = get_page_posts(limit=post_limit)
    rows = []
    for p in posts:
        meta = {
            'post_id':               p['id'],
            'post_message':          p.get('message',''),
            'post_time':             p['created_time'],
            'post_shares':           p.get('shares',{}).get('summary',{}).get('total_count',0),
            'post_comments_count':   p.get('comments',{}).get('summary',{}).get('total_count',0),
            'post_reactions_count':  p.get('reactions',{}).get('summary',{}).get('total_count',0)
        }
        comments = get_comments_for_post(p['id'], limit=comment_limit)
        for c in comments:
            rows.append({
                **meta,
                'comment_id':    c['id'],
                'comment_from':  c.get('from',{}).get('name',''),
                'comment_psid':  c.get('from',{}).get('id',''),
                'comment_text':  c.get('message',''),
                'comment_time':  c['created_time'],
                'comment_likes': c.get('like_count',0)
            })
    return pd.DataFrame(rows)

if __name__ == '__main__':
    # Construir y guardar CSV
    df_fb = build_comments_df(post_limit=2, comment_limit=2)
    print(f"Total comentarios obtenidos: {len(df_fb)}")
    df_fb.to_csv('fb_page_comments.csv', index=False)
    