import re
import pandas as pd
import emoji  as em
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def preprocess(data):
    pattern =r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM)\s-\s"
    message = re.split(pattern,data)[1:]
    messages = [m.strip() for m in message if m.strip()] # Remove empty spaces
    data = data.replace("\u202f", " ")
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'datetime_str': dates, 'message': messages})

    # Clean and convert to real datetime objects
    df['datetime_str'] = df['datetime_str'].str.replace(" - ", "")  #regex=False
    df['datetime'] = pd.to_datetime(df['datetime_str'], format="%m/%d/%y, %I:%M %p") ## %I->hour %M->minute %P-> AM/PM
    df.drop(columns='datetime_str', inplace=True)

    users =[]
    messages = []
    for message in df["message"]:
        entry = re.split(r"([\w\W]+?):\s",message)
        
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("goup_notification")
            messages.append(entry[0])

    df["user"] = users
    df["messages"] = messages
    df.drop(columns=["message"],inplace=True)
    
    df["year"] = df["datetime"].dt.year
    df["month_num"] = df["datetime"].dt.month
    df["month"] = df["datetime"].dt.month_name()
    df["day"] = df["datetime"].dt.day
    df["date"] = df["datetime"].dt.date
    df["day_name"] = df["datetime"].dt.day_name()
    df["hour"] = df["datetime"].dt.hour
    df["minute"] = df["datetime"].dt.minute


    period_time = []
    for hour in df[["day_name","hour"]]["hour"]:
        if hour == 23:
            period_time.append(str(hour)+"-"+ str("00"))
        elif hour == 0:
            period_time.append(str("00")+"-"+ str(hour+1))
        else:
            period_time.append(str(hour)+"-"+ str(hour+1))
    
    df["period_time"] = period_time
    
    # sentiment 
    df["demojize_messages"]=df["messages"].apply(lambda x: em.demojize(str(x),language ="en"))# Convert emoji to its textual representation
    sia = SentimentIntensityAnalyzer()
    df["sentiment_score"] =df["demojize_messages"].apply(lambda x: sia.polarity_scores(str(x))["compound"])

    df["sentiment"] = pd.cut(df["sentiment_score"],
                             bins=[-1,-0.5,0.5,1],
                             labels =["Negative","Natural","Positive"])
    return df