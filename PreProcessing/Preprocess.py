import pandas 
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy
from PreProcessing.Punctuation import add_punctuations
from Logs.Logsconfig import logger

# Download Pretrained model for Tokenization
nltk.download('punkt_tab')

# pretrained language model for processing text.
nlp = spacy.load('en_core_web_sm')

column_names = ['Positive_Review', 'Negative_Review']

# Handling null values 
def hanlde_null_values(data):
    try: 
        for column in data.select_dtypes(include=[np.number]).columns:
            data[column] = data[column].fillna(data[column].median())

        for column in data.select_dtypes(include=[object]).columns:
            data[column] = data[column].fillna('N/A')
        logger.info("Handled Null values")
        return data
    except Exception as e:
        logger.error("Error Occurred when Handling null values : " + str(e))
        return None

def remove_unwanted_columns(data):
    try:
        columns_to_remove = [
            'Review_Total_Negative_Word_Counts', 
            'Review_Total_Positive_Word_Counts', 
            'Reviewer_Score', 
            'days_since_review', 
            'lat', 
            'lng',
            'Additional_Number_of_Scoring'
        ]

        data = data.drop(columns=[col for col in columns_to_remove if col in data.columns], errors='ignore')
        logger.info("Removed unnecessary columns")
        
        return data
    except Exception as e:
        logger.error("Error Occurred when removing unwanted columns : " + str(e))
        return None


#  Lowercasing, removing all alphanumeric characters, remove stopwords and extra spaces
def normalize_data(text):
    try:
        text = text.lower()  
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  
        text = ' '.join(text.split()) 

        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        filtered_text = [word for word in words if word not in stop_words]
        text = " ".join(filtered_text)
        return text
    except Exception as e:
        logger.error("Error Occurred when normalizing data : " + str(e))
        return None

def normalize_object_columns(data):
    for column in data.select_dtypes(include=[object]).columns:
        data[column] = data[column].apply(lambda x: normalize_data(str(x)) if pandas.notnull(x) else '')
    logger.info("Normalized data")
    return data

# Tokenization
# def punctuate_Columns(data):
#     for column in column_names:
#         data[column] = data[column].apply(lambda x: add_punctuations(x) if pandas.notnull(x) else '')
#     return data

# # Apply punctuation for Address Column
# def punctuate_address(data):
#     data = data.apply(lambda x: add_punctuations(x) if pandas.notnull(x) else '')
#     return data

# def tokenize_Columns(data):
#     punctuate_data = punctuate_Columns(data)
#     for column in column_names:
#         data[column + '_Sentences'] = punctuate_data[column].apply(lambda x: sent_tokenize(str(x)) if pandas.notnull(x) else [])
#     data['Hotel_Address'] = punctuate_address(data['Hotel_Address'])
#     return data


# Extracting entities
def named_entity_recognition(text):
    try:
        doc = nlp(text)
        return [ent.text for ent in doc.ents]
    except Exception as e:
        logger.error("Error Occurred when Extracting entities : " + str(e))
        return None

def extract_named_entities(data):
    for column in column_names:
        data[column + '_NER'] = data[column].apply(lambda x: named_entity_recognition(x) if pandas.notnull(x) else '')
    return data

# def translate_to_english(text):
#     blob = TextBlob(text)
#     return blob.translate(to='en')

# def translate_columns(data):
#     for column in column_names:
#         data[column] = data[column].apply(lambda x: translate_to_english(x) if pandas.notnull(x) else '')
#     return data
