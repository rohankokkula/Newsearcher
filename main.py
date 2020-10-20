from pygooglenews import GoogleNews
import streamlit as st
import pandas as pd
import nltk
from newspaper import Article
from gtts import gTTS 
import base64
gn = GoogleNews()
nltk.download('punkt')
st.beta_set_page_config(
    page_title="Newsummarizer",
    layout="wide",
    page_icon="📄",
    initial_sidebar_state="expanded")

st.markdown("""<h1 style='text-align:center;color:#8000C4;font-family: montserrat;font-size:70px;margin-top:-70px;'>NEWSUMMARISER<span style='text-align:center;color:red;'>.</span></h1>""",unsafe_allow_html=True)
search_term = st.sidebar.text_input('Search Term:', 'Corona Virus mumbai')
search = gn.search(search_term,when='1')
data = pd.DataFrame.from_dict(search['entries'])
count=st.sidebar.number_input("No. of Articles to display:",min_value=5,max_value=20,step=1,value=5)
st.markdown("""<h1 style='font-family: montserrat;text-align:center;color:#8000C4;'>{} <span style='text-align:center;color:red;'>News Articles</span></h1>""".format(search_term),unsafe_allow_html=True)
csv = data[['published','title','link']].to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode() 
st.sidebar.markdown(f'<a href="data:file/csv;base64,{b64}" download="{search_term}.csv">Download {search_term} generated dataset</a>', unsafe_allow_html=True)
for row in range(0, count):
    try:
        url=data['link'].iloc[row]
        article=Article(url)
        article.download()
        article.parse()
        article.nlp()
        st.markdown("""<h2 style="color:red;font-weight:bold;font-family: montserrat;">{}. <a style="color:#8000C4;font-weight:bold;font-family: montserrat;" href={} target=_blank>{}</a><p style="color:red;font-weight:bold;font-family: montserrat;margin-top:10px;">{}</p><img style='display: block;width: 70%;margin-left: auto;margin-right: auto;' src="{}"></h2>"""
        .format(row+1,data['link'].iloc[row],data['title'].iloc[row],data['published'].iloc[row],article.top_image),unsafe_allow_html=True)
        slot1=st.empty()
        slot2=st.empty()
        slot3=st.empty()
        slot4=st.empty()
        if(slot1.checkbox("Read Summary",key=row)):
            slot3.markdown("""<h3 style="font-family: montserrat;">{}</h3>""".format(article.summary),unsafe_allow_html=True)
        if(slot2.checkbox("Listen Summary",key=row)):
            tts = gTTS(text=article.summary, lang='en', slow=False)
            tts.save('ttsaudio.mp3')
            slot4.audio("ttsaudio.mp3")
    except:
        pass


