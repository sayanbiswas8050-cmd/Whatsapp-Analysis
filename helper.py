from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.corpus import stopwords
import pandas as pd
from collections import Counter
import emoji as em
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def fetch_stats(selected_user,df):
    if selected_user != "overall":
        df=df[df["user"] == selected_user] # specific  user checking step
    # 1. fetch number of messages 
    num_messages = df.shape[0]

    # 2.fetch num of words
    words =[]
    for messages in df["messages"]:
        words.extend(messages.split())
    num_words = len(words)

    # 3. num of media messages
    num_media_msg =df[df["messages"] == "<Media omitted>"].shape[0]

    # 4.num of links
    import re 
    links = []
    for messages in df["messages"]:
        links.extend(re.findall(r'http[s]?://',messages))
        num_links = len(links)
    return num_messages,num_words,num_media_msg,num_links

# most active users
def most_busy_users(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]

    temp = df[df["user"] != "group_notification"]
    df = temp[temp["messages"] != "<Media omitted>"]
    x = df["user"].value_counts().head()
    name = x.index
    count = x.values

    df = round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns ={"count":"percent"})
    return name,count,df

# WordCloud
def create_wordcolud(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["messages"] != "<Media omitted>"]
        
    wc = WordCloud(width = 500,height = 500,min_font_size = 10,stopwords=STOPWORDS,background_color = "white")
    df_wc = wc.generate(temp["messages"].str.cat(sep = " "))
    return df_wc

# Most Common words
def most_common_word(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["messages"] != "<Media omitted>"]
    stop_words = set(stopwords.words('english'))
    words = []
    for message in temp['messages']:
        for word in message.lower().split(): # Convert to lowercase
            if word not in stop_words and word.isalpha(): # remove stop_words and isalpha() remove punctuation (!@#$%&()/+-)
                words.append(word)
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

# emoji analysis
def emoji_search(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]
    
    emojis = []
    for message in df ["messages"]:
        emojis.extend([word for word in message if em.emoji_list(word)])

    return_df = pd.DataFrame(Counter(emojis).most_common(10))
    return return_df

def monthly_timeline(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]

    timeline = df.groupby(["year","month_num","month"]).count()["messages"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))
    timeline["time"] = time
    return timeline

# daliy timeline
def daily_timeline(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]

    daliy_timeline = df.groupby(["date"]).count()["messages"].reset_index()
    return daliy_timeline

# active days
def week_activity_map(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]
    return df["day_name"].value_counts()

# active months
def monthly_activity_map(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]
    return df["month"].value_counts()

# activity heatmap
def activity_heatmap(selected_user,df):
    if selected_user != "overall":
        df = df[df["user"]== selected_user]
    return df.pivot_table(index="day_name",columns ="period_time",values="messages",aggfunc = "count").fillna(0)

# def text_sentiment(selected_user,df):
#     if selected_user != "overall":
#         df[df["user"]== selected_user]
    
#         temp = df[df["user"] != "group_notification"]
#         return temp