from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

model = SentimentIntensityAnalyzer()

def comment_sentiments(comment):
    scores = model.polarity_scores(comment)

    pos = scores['pos']
    neu = scores['neu']
    neg = scores['neg']

    return [neg, neu, pos]


def median_sentiment(comments):
    n = len(comments)

    ratings = np.zeros([3, n])

    for i, comment in enumerate(comments):
        sentiment = comment_sentiments(comment)
        ratings[:, i] = sentiment

    # Median along columns

    median = np.median(ratings, axis=1)
    score = median / sum(median)

    return score


def main():
    ...


if __name__ == "__main__":
    main()