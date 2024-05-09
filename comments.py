import html.parser
import os
import html
import re as regex
from emoji import emoji_count
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env

load_dotenv()
KEY = os.environ['API_KEY']
service = os.environ['SERVICE']
version = os.environ['VERSION']

YT = build(serviceName=service, version=version, developerKey=KEY)

# TODO: Filter out initial b and HTML encoding

def get_comments(video_id):
    comments = {}
    threads = {}

    method = YT.commentThreads()
    request = method.list(
        part='snippet, replies', 
        videoId=video_id, 
        textFormat='html'
    )

    response = request.execute()
    results = response.get('items', [])
    nextPage = response.get('nextPageToken', None)
    
    while True:

        for result in results:
            comment = result['snippet']['topLevelComment']['snippet']['textDisplay']
            id = result['snippet']['topLevelComment']['id']
            reply_count = result['snippet']['totalReplyCount']

            if is_relevant(video_id, comment):
                comments[id] = format_comment(comment)

            if reply_count > 0:
                reply_ids = [reply['id'] for reply in result['replies']['comments']]
                replies = [reply['snippet']['textDisplay'] for reply in result['replies']['comments']]

                threads[id] = reply_ids

                for id, reply in zip(reply_ids, replies):
                    if is_relevant(video_id, reply):
                        comments[id] = format_comment(reply)
        
        if nextPage is None: 
            break

        request = method.list(
            part='snippet, replies', 
            videoId=video_id,
            textFormat='html', 
            pageToken=nextPage
        )

        response = request.execute()
        results = response.get('items', [])
        nextPage = response.get('nextPageToken', None)

    return comments, threads


def is_relevant(video_id, comment):
    threshold = 0.65
    
    s = comment.strip()

    emojis = emoji_count(s)
    characters = len( regex.sub(r'\s', '', s) )

    # Remove hyperlinks

    if '</a>' in s and video_id not in s:
        return False

    if all(not char.isalnum() for char in s):
        return False
    
    if emojis / characters > threshold:
        return False
    
    return True


def format_comment(comment):   
    front = regex.compile('<a.*?>')
    end = regex.compile('</a>')

    comment = regex.sub(front, '', comment)
    comment = regex.sub(end, '', comment)
    comment = html.unescape(comment)
    
    return comment


def main():
    comments, threads = get_comments('lZMtgcOgfEk')

    for key, value in comments.items():
        print(f'{key}: {value}\n')

if __name__ == "__main__":
    main()