# Import the necessary modules
import os  # For working with the operating system
from numpy import vectorize  # Import the 'vectorize' function from the 'numpy' library
from sklearn.feature_extraction.text import TfidfVectorizer  # Import 'TfidfVectorizer' from 'sklearn' library
from sklearn.metrics.pairwise import cosine_similarity  # Import 'cosine_similarity' from 'sklearn' library

# Get a list of text files in the current directory
sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]

# Read the contents of each text file and store them in a list
sample_contents = [open(File).read() for File in sample_files]

# Define a lambda function 'vectorize' that converts text data into TF-IDF vectors
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()

# Define a lambda function 'similarity' that calculates the cosine similarity between two text document vectors
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

# Create TF-IDF vectors for the sample text contents
vectors = vectorize(sample_contents)

# Combine the sample file names with their respective TF-IDF vectors
s_vectors = list(zip(sample_files, vectors))

# Define a function 'check_plagiarism' to check for plagiarism
def check_plagiarism():
    results = set()  # Initialize an empty set to store plagiarism results
    global s_vectors  # Access the 's_vectors' variable defined earlier
    for sample_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()  # Create a copy of the 's_vectors' list
        current_index = new_vectors.index((sample_a, text_vector_a))  # Get the index of the current sample
        del new_vectors[current_index]  # Remove the current sample from the copy
        for sample_b, text_vector_b in new_vectors:
            # Calculate the cosine similarity between the TF-IDF vectors of two samples
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            # Sort the sample names to ensure consistent pairs
            sample_pair = sorted((sample_a, sample_b))
            # Store the result as a tuple (sample1, sample2, similarity_score)
            score = sample_pair[0], sample_pair[1], sim_score
            results.add(score)  # Add the result to the 'results' set
    return results  # Return the set of plagiarism results

# Iterate through the plagiarism results and print them
for data in check_plagiarism():
    print(data)
