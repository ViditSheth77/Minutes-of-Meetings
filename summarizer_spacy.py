import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import pymongo
from pymongo import MongoClient
import re
from newspaper import Article

#text = """"In an attempt to build an AI-ready workforce, Microsoft announced Intelligent Cloud Hub which has been launched to empower the next generation of students with AI-ready skills. Envisioned as a three-year collaborative program, Intelligent Cloud Hub will support around 100 institutions with AI infrastructure, course content and curriculum, developer support, development tools and give students access to cloud and AI services. As part of the program, the Redmond giant which wants to expand its reach and is planning to build a strong developer ecosystem in India with the program will set up the core AI infrastructure and IoT Hub for the selected campuses. The company will provide AI development tools and Azure AI services such as Microsoft Cognitive Services, Bot Services and Azure Machine Learning.According to Manish Prakash, Country General Manager-PS, Health and Education, Microsoft India, said, With AI being the defining technology of our time, it is transforming lives and industry and the jobs of tomorrow will require a different skillset. This will require more collaborations and training and working with AI. That’s why it has become more critical than ever for educational institutions to integrate new cloud and AI technologies. The program is an attempt to ramp up the institutional set-up and build capabilities among the educators to educate the workforce of tomorrow. The program aims to build up the cognitive skills and in-depth understanding of developing intelligent cloud connected solutions for applications across industry. Earlier in April this year, the company announced Microsoft Professional Program In AI as a learning track open to the public. The program was developed to provide job ready skills to programmers who wanted to hone their skills in AI and data science with a series of online courses which featured hands-on labs and expert instructors as well. This program also included developer-focused AI school that provided a bunch of assets to help build AI skills."""
text = input("Enter the text or url to sumarize:")

def check_input_type(text):
    url_pattern = re.compile(r'^(http|https)://[^\s/$.?#].[^\s]*$')
    return re.match(url_pattern, text) is not None

if check_input_type(text):
    article = Article(text)
    article.download()
    article.parse()
    article.nlp()
    text = article.text
    #print(article.text)



def textSummarizer(text, percentage):
    
    # load the model into spaCy
    nlp = spacy.load('en_core_web_sm')
    
    # pass the text into the nlp function
    doc= nlp(text)
    
    # The score of each word is kept in a frequency table
    tokens=[token.text for token in doc]
    freq_of_word=dict()
    
    # Text cleaning and vectorization 
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in freq_of_word.keys():
                    freq_of_word[word.text] = 1
                else:
                    freq_of_word[word.text] += 1
                    
    # Maximum frequency of word
    max_freq=max(freq_of_word.values())
    
    # Normalization of word frequency
    for word in freq_of_word.keys():
        freq_of_word[word]=freq_of_word[word]/max_freq
        
    # In this part, each sentence is weighed based on how often it contains the token.
    sent_tokens= [sent for sent in doc.sents]
    sent_scores = dict()
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in freq_of_word.keys():
                if sent not in sent_scores.keys():                            
                    sent_scores[sent]=freq_of_word[word.text.lower()]
                else:
                    sent_scores[sent]+=freq_of_word[word.text.lower()]
    
    
    len_tokens=int(len(sent_tokens)*percentage)
    
    # Summary for the sentences with maximum score. Here, each sentence in the list is of spacy.span type
    summary = nlargest(n = len_tokens, iterable = sent_scores,key=sent_scores.get)
    
    # Prepare for final summary
    final_summary=[word.text for word in summary]
    
    # Convert to a string
    summary=" ".join(final_summary)
    
    # Return final summary
    return summary

final_summary = textSummarizer(text, 0.2)

"""print("original text: ", text)
print("--------------------------------------------------------------------------------------------------------------------------")
print("final summary: ", final_summary)"""

##################################CONNECTION TO DATABASE################################################################

# Establish a connection to your MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["MeetBoard"]  # Replace with your database name
collection = db["Data"]  # Replace with your collection name

# Your Python code that generates output
output_data = {
    "original text": text,
    "summary": final_summary
}

# Insert the output into MongoDB
inserted_data = collection.insert_one(output_data)
print("Output inserted. The object id is:", inserted_data.inserted_id)