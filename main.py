from pygooglenews import GoogleNews
import streamlit as st
import pandas as pd
import nltk
from newspaper import Article
import wget
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
data_name=f"{search_term}_results.csv"
data.to_csv(data_name,columns=["title","link","published"])
st.sidebar.markdown(f"""<form method="get" action="dataa.csv">
   <button type="submit">Download data</button>
</form>""",unsafe_allow_html=True)
for row in range(0, count):
    url=data['link'].iloc[row]
    article=Article(url)
    article.download()
    article.parse()
    article.nlp()
    st.markdown("""<h2 ><a style="color:#8000C4;font-weight:bold;font-family: montserrat;" href={} target=_blank>{}</a><p style="color:red;font-weight:bold;font-family: montserrat;margin-top:10px;">{}</p><img style='display: block;width: 50%;' src="{}"></h2>"""
    .format(data['link'].iloc[row],data['title'].iloc[row],data['published'].iloc[row],article.top_image),unsafe_allow_html=True)
    slot1=st.empty()
    slot2=st.empty()
    if(slot1.checkbox("Extract Summary",key=row)):
        slot2.markdown("""<h3 style="font-family: montserrat;">{}</h3>""".format(article.summary),unsafe_allow_html=True)



