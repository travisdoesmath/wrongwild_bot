import os
import praw

reddit = praw.Reddit(
    user_agent=os.getenv("USER_AGENT"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)

subreddit = reddit.subreddit("gonwild")

def authors_nsfw_percentage(author):
    if hasattr(author, 'is_suspended'):
            return 100
    nsfw_count = 0
    sfw_count = 0
    for submission in author.submissions.new():
        if submission.subreddit != 'gonwild' and submission.over_18:
            nsfw_count += 1
        else:
            sfw_count += 1
    return nsfw_count / (nsfw_count + sfw_count)

for submission in subreddit.stream.submissions():
    author = submission.author
    nsfw_percentage = authors_nsfw_percentage(author)
    # print(author, nsfw_percentage)
    if nsfw_percentage > 0.5:
        submission.report("User is likely a porn bot.")
        submission.reply("This post has been reported to the moderators and /u/SabreYT has been tagged.\n\nMore than half of the user's submissions are to (non-gonwild) NSFW subreddits or their account is suspended\n\n---\n\n^(I am a bot created by /u/travisdoesmath)")
