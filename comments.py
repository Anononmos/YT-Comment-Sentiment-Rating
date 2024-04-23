import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env

load_dotenv()
KEY = os.environ['API_KEY']
service = os.environ['SERVICE']
version = os.environ['VERSION']

YT = build(serviceName=service, version=version, developerKey=KEY)


# TODO: Build comment object 
#       id, text pairs
#       comment, replies pairs

def navigate(request, callback, initial, reduce):
    response = request.execute()
    nextPage = response.get('nextPageToken', None)

    if nextPage is None:
        callback(response)

    ...

def get_comments(video_id):
    comments = {}
    threads = {}

    method = YT.commentThreads()
    request = method.list(
        part='snippet, replies', 
        video_id=video_id
    )

    response = request.execute()
    results = response.get('items', [])
    
    while True:

        for result in results:
            ...
        
        if nextPage is None: 
            break

        request = method.list(
            part='snippet, replies', 
            video_id=video_id, 
            pageToken=nextPage
        )

        response = request.execute()
        nextPage = response.get('nextPageToken', None)

    return comments, threads


def main():
    ...

if __name__ == "__main__":
    main()