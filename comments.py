import os
import html
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

            comments[id] = html.unescape(comment)

            if reply_count > 0:
                reply_ids = [reply['id'] for reply in result['replies']['comments']]
                replies = [reply['snippet']['textDisplay'] for reply in result['replies']['comments']]

                threads[id] = reply_ids

                for id, reply in zip(reply_ids, replies):
                    comments[id] = html.unescape(reply)
        
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


def main():
    comments, threads = get_comments('NnmekTRwYjU')

    print(comments)

    ...

if __name__ == "__main__":
    main()