
# IMPORT STATEMENTS
from newspaper import Article
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
#nltk.download('punkt')
import streamlit as st
import time


# NLP
article = Article('https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963')
article.download()
article.parse()
article.nlp()
corpus = article.text
text = corpus
sentence_list = nltk.sent_tokenize(text)

# HEAD
st.title('Hey, this is CovidBot')
# st.image('sample.png', use_column_width=True)

# FUNCTIONS
def greetings(text):
    text = text.lower()
    bot_greetings = 'Hey There !'
    user_greetings = ['hi', 'hello', 'hey there', 'hola', 'hey']
    for word in text.split():
        if word in user_greetings:
            return bot_greetings

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]]>x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response = bot_response+' '+sentence_list[index[i]]
            response_flag=1
            j+=1
        if j>2:
            break
    if response_flag==0:
        bot_response= bot_response+' '+'Sorry I did not understand'
    sentence_list.remove(user_input)
    return bot_response


# CHATTING
line = 1
flag=1
while flag==1:
    line+=1
    x = st.text_input('Enter your text', key=str(line))
    if (x):
        if (x=='quit'):
            st.write('YOU: '+x)
            st.write('BOT: Thanks')
            break
        else:
            if greetings(x)!=None:
                    st.write('YOU: '+x)
                    st.write('BOT: '+greetings(x))
            else:
                    st.write('YOU: '+x)
                    st.write('BOT: '+bot_response(x))
        flag=1
    else:
        flag=0

