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
    page_title="Newsearcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""<h1 style='text-align:center;color:#8000C4;font-family: montserrat;font-size:50px;margin-top:-70px;'>Newsearcher<span style='text-align:center;color:red;'>.</span></h1><h3 style='text-align:center;margin-top:-25px;'>Created by: <u><a href='https://in.linkedin.com/in/rohankokkula' target="_blank">Rohan Kokkula</u></a></h3>""",unsafe_allow_html=True)
search_term = st.sidebar.text_input('Search Term:', 'Streamlit')
search = gn.search(search_term,when='1')
data = pd.DataFrame.from_dict(search['entries'])
count=st.sidebar.number_input("No. of Articles to display:",min_value=5,max_value=20,step=1,value=5)
st.markdown("""<h1 style='font-family: montserrat;text-align:center;color:#8000C4;'>{} <span style='text-align:center;color:red;'>News Articles</span></h1>""".format(search_term),unsafe_allow_html=True)
csv = data[['published','title','link']].to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode() 

for row in range(0, count):
    try:
        url=data['link'].iloc[row]
        article=Article(url)
        article.download()
        article.parse()
        article.nlp()
        with st.beta_expander(f"{row+1}. {data['title'].iloc[row]}"):
            col1, col2 = st.beta_columns([1, 1])
            
            col1.markdown("""<img style='display: block;width: 100%;' src="{}"><p style="color:red;font-weight:bold">{}</p><a style="color:#8000C4;font-weight:bold;font-family: montserrat;" href={} target=_blank>{}</a>"""
            .format(article.top_image,data['published'].iloc[row],data['link'].iloc[row],"Article Link"),unsafe_allow_html=True)
            if(col2.checkbox("Read Summary",key=row)):
                col2.markdown("""<h3 style="font-family: montserrat;">{}</h3>""".format(article.summary),unsafe_allow_html=True)
            if(col2.checkbox("Listen Summary",key=row)):
                tts = gTTS(text=article.summary, lang='en', slow=False)
                tts.save('ttsaudio.mp3')
                col2.audio("ttsaudio.mp3")
    except:
        pass

st.sidebar.markdown(f'<a href="data:file/csv;base64,{b64}" download="{search_term} dataset.csv">Download {search_term} dataset</a>', unsafe_allow_html=True)