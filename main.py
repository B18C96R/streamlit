# streamlit run <this file name>

# https://streamlit.io/gallery
# ここにテンプレは詰まっている

# https://docs.streamlit.io/library/api-reference
# APIリファレンスを見ればたいていのことは乗っている

# https://qiita.com/yoichi_t/items/065779ddf0a528289cbf
# アプリ無限増殖方法かも？



import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import time
from ast import Break
from mmap import ACCESS_COPY
from pprint import pprint
import heapq
import pandas as pd
import re
import tweepy






# definition function of get_api
def ClientInfomation():
    client = tweepy.Client(
        bearer_token = BEARER_TOKEN,
        consumer_key = API_KEY,
        consumer_secret = API_SECRET,
        access_token = ACCESS_TOKEN,
        access_token_secret = ACCESS_TOKEN_SECRET
    )

    return client


# def serch_tweet_fuction
def SearchTweetFunction(search, tweet_max):
    # get recently tweets
    tweets = API.search_recent_tweets(query=search, max_results=tweet_max)

    # Processing acquired data
    results = []
    tweets_data = tweets.data

    # get results
    if tweets_data != None:
        for tweet in tweets_data:
            dict_data = {}
            dict_data["tweet_id"] = tweet.id
            dict_data["text"] = tweet.text
            results.append(dict_data)
    else:
        # append nothing
        results.append('')

    return results





# favorite counting function
def Get_Liking_Usernum(dictlist):

    favnum_list = []
    tweet_id_list = []
    #i = 0

    for twidlt in dictlist:
        if twidlt == '':
            Break
        else:
            tmp = twidlt['tweet_id']
            tweet_id_list.append(tmp)

    for id_num in tweet_id_list:
        liking_users_list = API.get_liking_users(id=int(id_num)).data

        if liking_users_list is not None:
            favnum = len(liking_users_list)
            favnum_list.append(favnum)

        else:
            favnum_list.append(0)

    return favnum_list



# add the number of "いいね！"
def AppendFavnum(dictlist, fav_list):

    i = 0

    for num in fav_list:
        tmp_dict = dictlist[i]
        tmp_dict["fav_num"] = num
        i += 1

    return dictlist



# generate pandas Dataframe
def Gen_df(dictlist):

    list_list = []

    id_list = []
    text_list = []
    list_favnum = []

    for d in dictlist:
        tmp_id = d['tweet_id']
        tmp_text = d['text']
        tmp_fav = d['fav_num']

        id_list.append(tmp_id)
        text_list.append(tmp_text)
        list_favnum.append(tmp_fav)

    zip_list = zip(id_list, text_list, list_favnum)
    df = pd.DataFrame(zip_list, columns=['id','text','fav'])

    return df



def PutStarSleepFunc(integer):
    i = 0
    while i < integer:
        print("*")
        time.sleep(1)
        i += 1




def clean_text(text):
    replaced_text = '\n'.join(s.strip() for s in text.splitlines()[2:] if s != '')  # skip header by [2:]
    replaced_text = replaced_text.lower()
    replaced_text = re.sub(r'[【】]', ' ', replaced_text)       # 【】の除去
    replaced_text = re.sub(r'[（）()]', ' ', replaced_text)     # （）の除去
    replaced_text = re.sub(r'[［］\[\]]', ' ', replaced_text)   # ［］の除去
    replaced_text = re.sub(r'[@＠]\w+', '', replaced_text)  # メンションの除去
    replaced_text = re.sub(r'https?:\/\/.*?[\r\n ]', '', replaced_text)  # URLの除去
    replaced_text = re.sub(r'　', ' ', replaced_text)  # 全角空白の除去

    return replaced_text
















#-------------------------------------------------------------------
# API information
BEARER_TOKEN        = "AAAAAAAAAAAAAAAAAAAAANX7fAEAAAAAJTCW9dfzmgiGvHNG2HwYYuEbTZY%3D8AoTRRhTxmGe8px9HSG7boHmD9xl1d989zI1U78PR1t6Q96Yps"
API_KEY             = "taQt8tw3RJYtTGN95zO5LzhMx"
API_SECRET          = "IBRk8KGYFRqqsZqKLJD1JDPBfa0cJs0cmWq5xpsDOMAV6OQz9Z"
ACCESS_TOKEN        = "1551490706686242816-sbYm9SrHoqiYlmogaIw5MEDeD1SYMp"
ACCESS_TOKEN_SECRET = "aCdDTMBJNFkTugYq9YDTtkvk50ViV6Dxh4lhhhvjJpPzs"

API = ClientInfomation()

# then, twitter API settings all done!


# タイトルの追加は超簡単
# 実行時はコマンドプロンプトからLocalhostの指定ポートを開く
# st.title('Tweepy_App_Beta by CXGr.')
"""
# Tweepy_App_Beta by CXGr.
"""



# required information of serching
search_tmp1 = st.text_input('検索したい語句を入力して下さい（検索語句の工夫が重要です）↓')
'検索語句：',search_tmp1
search_tmp2 = " -RT".replace('\u3000', ' ')

# slider表示
tweet_tmp = st.slider(
    '何件のTweetを取得しますか？（10-100の間で指定,30件程度推奨）',
    0, 50, 20
    )
# tweet_tmp = st.text_input('何件のTweetを取得しますか？（10-100の間で指定,30件程度推奨）→')
tweet_max = int(tweet_tmp)

search = search_tmp1 + search_tmp2
#search    = "三菱自動車 -RT"  # search Words
search_sub = search.replace(" -RT", "")
#tweet_max = 10           # Number of tweets you want to retrieve
Top_num = 10 # define as a global variable
#-------------------------------------------------------------------






# 単に文字を書きたいときはこれ
'''
### Tweetを自動取得し、いいね！順にソートします
'''




# プログレスバーの表示

button2 = st.button('Tweet取得を開始！')
if button2:
    'TwitterAPIを読み込み中、、、、、'
    # これ以下を表示させないようにEmptyとしながら、プログレスバーを設置
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        latest_iteration.text(f'Iteration:{i+1}')
        bar.progress(i+1)
        time.sleep(0.02)

    # for を抜けたら、以下を表示する
    'Done.'


    # main_code
    #--------------------------------
    result_dictlist = SearchTweetFunction(search, tweet_max)

    if result_dictlist == ['']:
        # PutStarSleepFunc(3)
        st.write(f'{"="*15}There is NO corresponding Tweet. Please redo with other words.{"="*15}')

    else:
        favnum_list = Get_Liking_Usernum(result_dictlist)
        fix_dictlist = AppendFavnum(result_dictlist, favnum_list)

        st.write(f'取得した{tweet_max}件をいいね！数順にソート中 :sunglasses:')# OK without
        time.sleep(2)# OK without
        st.write(f"検索語句：{search_sub}")# OK without
        time.sleep(2)# OK without
        df = Gen_df(fix_dictlist)
        df_fix = df.sort_values('fav', ascending=False)

        #print('Run [df_fix] below ↓')# for Jupyter
        st.table(df_fix) # for command prompt
    #--------------------------------


st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text(" \n")



# エクスパンダー機能
'''
### FAQ
'''
expander0 = st.expander('Q: 「TooManyRequests: 429 Too Many Requests Too Many Requests」と出てしまうが？')
expander0.write('A: おかげさまで、沢山のアクセスを頂いているようです。APIロックが解除される、15分後に再度アクセスしてみて下さい。')
expander1 = st.expander('Q: なぜ取得数制限があるのですか？')
expander1.write('A: 本アプリはTwitterAPIを利用しており、Twitter社によるAPI取得制限に準ずるための基準を設けています。')
expander2 = st.expander('Q: アプリが上手く動かないのですが、なぜですか？')
expander2.write('A: こちらはベータ版につき何かと不具合もあるかもしれません。ぜひ詳細を管理者までご連絡下さい。')
expander3 = st.expander('Q: 私のTwitterで検索した結果と乖離がありますが、理由は何ですか？')
expander3.write('A: こちらはデモ的に取得したTwitterアカウントをベースにしているため、そのような挙動となっています。')
expander4 = st.expander('Q: 「There is NO corresponding Tweet. Please redo with other words.」と出てしまう。')
expander4.write('A: 検索語句をもう少しシンプルにして再度試してみて下さい。')
expander5 = st.expander('Q: DfのIndexはReIndexしないのですか？')
expander5.write('A: してもいいのですが、元々取得したDfをソートしてる感を出すために敢えてそのままにしています。')
