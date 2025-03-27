import html.parser
import os
import html
import re as regex
from emoji import emoji_count
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables from .env

load_dotenv()
KEY = os.environ['API_KEY']
service = os.environ['SERVICE']
version = os.environ['VERSION']

YT = build(serviceName=service, version=version, developerKey=KEY)

# TODO: Add error handling for API call failure

def get_vidId(url):
    if 'https://www.youtube.com' not in url or 'watch?v=' not in url:
        return None
    
    return url[-11:]


def get_comments(video_id):
    topcomments = {}    # reply id with its top comment id
    comments = {}       # comment id with its text display
    threads = {}        # topcomment id and reply ids

    method = YT.commentThreads()
    request = method.list(
        part='snippet, replies', 
        videoId=video_id, 
        textFormat='html'
    )

    try:
        response = request.execute()
    except HttpError as e:
        raise e

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

                for reply_id, reply in zip(reply_ids, replies):
                    if is_relevant(video_id, reply):
                        comments[reply_id] = format_comment(reply)
                        topcomments[reply_id] = id
        
        if nextPage is None: 
            break

        request = method.list(
            part='snippet, replies', 
            videoId=video_id,
            textFormat='html', 
            pageToken=nextPage
        )

        try:
            response = request.execute()
        except HttpError as e:
            raise e

        results = response.get('items', [])
        nextPage = response.get('nextPageToken', None)

        if results == []:
            break

    return comments, topcomments, threads


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
    # Filter out hyperlinks

    front = regex.compile('<a.*?>')
    end = regex.compile('</a>')

    # Filter out user handles

    user_handle = regex.compile('@@\S*')

    comment = regex.sub(front, '', comment)
    comment = regex.sub(end, '', comment)
    comment = html.unescape(comment)
    
    comment = regex.sub('<br>', '', comment)
    comment = regex.sub(user_handle, '', comment)
    
    return comment


def main():
    comments, _, _ = get_comments('pzxC5Ad3Ars')

    print(comments)

if __name__ == "__main__":
    main()