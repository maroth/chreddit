import os

try:
    username = os.environ['REDDIT_USERNAME']
except:
    username = ""

try:
    password = os.environ['REDDIT_PASSWORD']
except:
    password = ""

try:
    subreddit = os.environ['SUBREDDIT']
except:
    subreddit = ""
    
try:
    client_id = os.environ['REDDIT_CLIENT_ID']
except:
    client_id = ""

try:
    client_secret = os.environ['REDDIT_CLIENT_SECRET']
except:
    client_secret = ""

database_url \
    = os.environ.get('DATABASE_URL',
                     'postgresql://kusi:styles@localhost:5432/chreddit')

# table name for database to store submissions in
tablename = 'submission'

# max rows in database, oldest entries which
# are more than these are deleted on insert
max_rows = 100000

# reddit constant
max_length = 300

# append when description is too long to fit in max_length
suffix = '...'

# used for posting comments to denote
# articles with identical titles from other new soutltes
other_source_prefix = 'Artikel mit gleichem Titel: '

# separator between feed title and description in submission title
separator = u'\u2014'

# number of submissions to post each time the script
# is run (every ten minutes from heroku)
submissions_per_run = 5

# user agent to send to reddit API when submitting
user_agent = 'submission agent for /r/' + subreddit + ' (by transpostmeta)'
