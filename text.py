from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pdfplumber
import google.generativeai as genai
import nltk
from dotenv import load_dotenv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import string
import getpass
import os
import pandas as pd
import numpy as np



#pages embeddings
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

load_dotenv(dotenv_path='apikey.env')
api_key = os.getenv('GOOGLE_API_KEY')
if api_key is None:
    print("ERROR: The GOOGLE_API_KEY environment variable is not set.")
else:
    print("\n")

genai.configure(api_key=api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

query = input("Enter your query inside parentheses: ") #!!!!!replace input with text prompt



def data():
    if request.method == 'POST':
        content = request.json
        return jsonify({'response': 'Data received', 'yourData': content})
    else:
        data = {"message": "Hello from Flask!"}
        return jsonify(data)

def return_query():
    return query


def extract_text_from_pdf(pdf_path):
    """Extract text from each page of the specified PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


#pages embeddings
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)



def create_dataframe(sentences):
    # Embed each sentence and store in a dataframe
    data = {
        'sentence': sentences,
        'embedding': [embeddings.embed_query(sentence) for sentence in sentences]
    }
    return pd.DataFrame(data)

def find_best_passage(query_embed, dataframe):
    # Embed the query    
    # Calculate dot product of query embedding with all sentence embeddings in the dataframe
    dataframe['similarity'] = dataframe['embedding'].apply(lambda x: np.dot(query_embed, x))
    
    # Find the sentence with the highest similarity
    best_row = dataframe.loc[dataframe['similarity'].idxmax()]
    return best_row['sentence']


def main():
    query_embed = embeddings.embed_query(query)
    pdf_path = 'annualreport.pdf' #!!!!!!This needs to be changed to uploaded pdf
    document_text = extract_text_from_pdf(pdf_path)
    processed_text = preprocess_text(document_text)
    sentences = sent_tokenize(processed_text)
    df = create_dataframe(sentences)
    best_passage = find_best_passage(query_embed, df)
    return best_passage






