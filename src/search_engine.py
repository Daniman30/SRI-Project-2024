import os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def process_query(query, query_expand_bool, stop_words_bool, stemmer_bool):
    tokens = word_tokenize(query, "spanish")
    normal = [token.lower() for token in tokens]
    stop_words = set(stopwords.words('spanish'))
    stemmer = PorterStemmer()        
        
    if query_expand_bool:
        expanded_words = normal.copy()
        for word in normal:
            synsets = wordnet.synsets(word, None, "spa")
            for synset in synsets:
                expanded_words.extend(synset._lemma_names)
        if stop_words_bool:
            final = [word for word in expanded_words if word not in stop_words]
            if stemmer_bool:
                final.extend([stemmer.stem(token) for token in final])
            else:
                stemming = final
        else:
            if stemmer_bool:
                stemming = [stemmer.stem(token) for token in expanded_words]
            else:
                stemming = expanded_words
    else: 
        if stop_words_bool:
            final = [word for word in normal if word not in stop_words]
            if stemmer_bool:
                stemming = [stemmer.stem(token) for token in final]
            else:
                stemming = final
        else:
            if stemmer_bool:
                stemming = [stemmer.stem(token) for token in normal]
            else:
                stemming = normal
    
    return ' '.join(stemming)

# Function to read documents from a folder
def read_documents_from_folder():
    documents = []
    # Get the absolute path of the current folder
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the absolute path to the 'data' folder
    folder_path = os.path.join(current_dir, 'data')
    
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

def vectorial_model(texts, query, verbose, new_values):
    # Creating the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(lowercase=True, stop_words=None, max_df=1.0, min_df=1)
    
    # Transform texts into TF-IDF vectors
    vectors_tfidf_array = vectorizer.fit_transform(texts).toarray()
    
    # Getting the vectorizer vocabulary
    vocabulary = vectorizer.vocabulary_
    
    words_query = query.split(" ")
    
    i = 0
    # Modify TF-IDF values ​​of the query vector
    for word, new_value in zip(words_query, new_values):
        if word in vocabulary:
            index = vocabulary[word]
            # Each token is assigned the relevance determined in the frontend
            if verbose:
                vectors_tfidf_array[-1][index] = new_value
            else:
                new_values[i] = round(vectors_tfidf_array[-1][index], 2)
            i += 1
    
    # Calculate cosine similarity
    similarity = cosine_similarity(vectors_tfidf_array)
    
    return similarity, new_values

def search(query, verbose, values, query_expand_bool, stop_words_bool, stemmer_bool):
        
    # Process the query
    processed_query = process_query(query, query_expand_bool, stop_words_bool, stemmer_bool)
    
    # Read the documents
    documents = read_documents_from_folder()
    
    # Join the documents with the query in a single list
    texts = list(documents.values())
    texts.append(processed_query)
    
    # Calculate the TF-IDF of each document and the query
    matrix, final_values = vectorial_model(texts, query, verbose, values)
    
    # Map documents to their TF-IDF
    doc_tfidf = dict(zip(documents.keys(), matrix[-1][:-1]))
    
    # Filter documents with value greater than 0
    doc_tfidf_filtered = {k: v for k, v in doc_tfidf.items() if v > 0}
    
    if not doc_tfidf_filtered:
        doc_tfidf_filtered = {"No hay resultados relevantes": 1}
    
    # Sort the dictionary by values ​​from highest to lowest
    sorted_dictionary = dict(sorted(doc_tfidf_filtered.items(), key=lambda item: item[1], reverse=True))
    
    # Return the first 10 elements or all if there are less than 10
    top_10 = dict(list(sorted_dictionary.items())[:10])
    
    return top_10.keys(), final_values