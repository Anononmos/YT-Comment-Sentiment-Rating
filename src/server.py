from commentsAPI import get_comments
from model import median_sentiment
from flask import Flask
from flask_cors import CORS, cross_origin
from googleapiclient.errors import HttpError
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# TODO: Add error handling for API call failure

@app.route('/<video_id>')
@cross_origin()
def get_sentiment(video_id):
    
    try: 
        comments_dict, _, _ = get_comments(video_id)

    except HttpError as err:
        response = json.loads(err.content)
        reason = response['error']['errors'][0]['reason']
        message = response['error']['errors'][0]['message']

        return { 
            'status': err.resp.status, 
            'reason': reason, 
            'message': message
        }
    
    if comments_dict == {}:
        return {
            'status': 404, 
            'reason': 'commentsUnavailable', 
            'message': f'Video {video_id} does not have comments posted.'
        }

    comments = list( comments_dict.values() )
    median_score = median_sentiment(comments)

    return {
        'neg': median_score[0], 
        'neu': median_score[1], 
        'pos': median_score[2]
    }


if __name__ == "__main__":
    app.run()