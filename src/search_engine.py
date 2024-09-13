import os
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def process_query(query, query_expand_bool, stop_words_bool, stemmer_bool):
    """
    Processes a given query by tokenizing, normalizing, expanding, removing stop words, and stemming.

    Args:
        query (str): The input query string to be processed.
        query_expand_bool (bool): If True, expands the query with synonyms.
        stop_words_bool (bool): If True, removes stop words from the query.
        stemmer_bool (bool): If True, applies stemming to the query tokens.

    Returns:
        str: The processed query as a single string with tokens joined by spaces.

    Example:
        >>> process_query("sword", query_expand_bool=True, stop_words_bool=True, stemmer_bool=True)
        'spade sword blade brand steel'
    """
    tokens = word_tokenize(query, "spanish")
    normal = [token.lower() for token in tokens]
    stop_words = set(stopwords.words('spanish'))
    stemmer = PorterStemmer()   
    stemming = []

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
                stemming = final
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
    """
    Reads all text documents from the 'data' folder and returns their contents.

    This function retrieves the absolute path of the current folder, constructs the path to the 'data' folder,
    and reads all text files within it. The contents of each text file are stored in a dictionary with the
    filenames as keys.

    Returns:
        dict: A dictionary where the keys are filenames and the values are the contents of the text files.

    Example:
        >>> documents = read_documents_from_folder()
        >>> print(documents['example.txt'])
        'This is the content of example.txt'
    """
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
    """
    Creates a TF-IDF vectorizer, transforms texts into TF-IDF vectors, modifies the query vector based on new values,
    and calculates cosine similarity between the vectors.

    Args:
        texts (list of str): A list of text documents to be vectorized.
        query (str): The query string whose TF-IDF values will be modified.
        verbose (bool): If True, assigns new values to the query vector; otherwise, rounds the existing values.
        new_values (list of float): A list of new TF-IDF values to be assigned to the query vector.

    Returns:
        tuple: A tuple containing:
            - similarity (ndarray): The cosine similarity matrix of the TF-IDF vectors.
            - new_values (list of float): The modified or rounded TF-IDF values of the query vector.

    Example:
        >>> texts = ["This is a sample document.", "This document is another example."]
        >>> query = "sample document"
        >>> verbose = True
        >>> new_values = [0.5, 0.8]
        >>> similarity, new_values = vectorial_model(texts, query, verbose, new_values)
        >>> print(similarity)
        [[1.        0.70710678 0.84789507]
        [0.70710678 1.         0.54651017]
        [0.84789507 0.54651017 1.]]
    """
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
    """
    Searches for relevant documents based on a processed query using TF-IDF and cosine similarity.

    Args:
        query (str): The input query string to be processed and searched.
        verbose (bool): If True, assigns new values to the query vector; otherwise, rounds the existing values.
        values (list of float): A list of new TF-IDF values to be assigned to the query vector.
        query_expand_bool (bool): If True, expands the query with synonyms.
        stop_words_bool (bool): If True, removes stop words from the query.
        stemmer_bool (bool): If True, applies stemming to the query tokens.

    Returns:
        tuple: A tuple containing:
            - keys (dict_keys): The keys of the top 10 relevant documents.
            - final_values (list of float): The modified or rounded TF-IDF values of the query vector.

    Example:
        >>> query = "magic and clans"
        >>> verbose = True
        >>> values = [0.5, 0.8]
        >>> query_expand_bool = True
        >>> stop_words_bool = True
        >>> stemmer_bool = True
        >>> top_docs, final_values = search(query, verbose, values, query_expand_bool, stop_words_bool, stemmer_bool)
        >>> print(top_docs)
        dict_keys(['document1.txt', 'document2.txt', ...])
    """
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