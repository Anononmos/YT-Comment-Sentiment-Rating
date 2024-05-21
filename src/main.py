import model
import commentsAPI
import random

video = commentsAPI.get_vidId("https://www.youtube.com/watch?v=J5crXEaFOyw")
comments, topcomments, threads = commentsAPI.get_comments(video)

comments_list = list(comments.values())

score = model.median_sentiment(comments_list)
print(score)