import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #To convert bytes to strict text
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    # fetch unique users
    user_list = df["user"].unique().tolist()
    user_list.remove("goup_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user = st.sidebar.selectbox("show analysis user",user_list)

    if st.sidebar.button("show analysis"):

        num_messages,num_words,num_media_msg,num_links = helper.fetch_stats(selected_user,df)
        # stats area
        st.header("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Massages")
            st.title(num_media_msg)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # finding busiest user in a group(group level analysis)
        if selected_user == "overall":

            col1,col2 = st.columns(2)
            with col1:
                st.header("Most Busy Users")
                name,count,new_df = helper.most_busy_users(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(name,count,color ="red")
                plt.xticks(rotation = 45)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("Word Cloud")
        df_wc =helper.create_wordcolud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        word_count_df = helper.most_common_word(selected_user,df)
        fig,ax = plt.subplots()
        sns.barplot(x=word_count_df[1],y = word_count_df[0],orient='h',palette = "plasma")
        st.pyplot(fig)
        
        # emoji analysis
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        with col1:
            emoji = helper.emoji_search(selected_user,df)
            st.dataframe(emoji)
        with col2:
            fig,ax =plt.subplots()
            ax.pie(emoji[1],labels=emoji[0],autopct='%1.1f%%',shadow=True,startangle=90)
            st.pyplot(fig)

        # monthly timeline
        st.title("Monthly Tmeline")
        time_df = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(time_df["time"],time_df["messages"])
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        #daily timeline
        st.title("timeline")
        daily_time_df = helper.daily_timeline(selected_user,df)
        fig,ax= plt.subplots()
        ax.plot(daily_time_df["date"],daily_time_df["messages"],color = "green")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        # active days
        st.title("Activity Map")

        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax= plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="red")
            plt.xticks(rotation =45)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy month")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig,ax= plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation =45)
            st.pyplot(fig)

        # activity heatmap
        st.title("Activity Heatmap")
        time_heatmap =helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        sns.heatmap(time_heatmap)
        plt.xticks(rotation = "horizontal")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        # sentiment_score
        # st.title("text_semtiment_score")
        # temp = helper.text_sentiment(selected_user,df)
        # fig, ax = plt.subplots()
        # sns.barplot(data=df, x="user", y="sentiment",orient = "h",errorbar=None,palette="magma")
        # plt.title("Sentiment vs user", fontsize=14, fontweight="bold")
        # plt.xticks(rotation = "vertical")
        # st.pyplot(fig)