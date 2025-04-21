import os
import numpy as np
import json  # Ensure to import json to handle the JSON parsing

def cosine_similarity(vec1, vec2):
    # Compute the cosine similarity between two text vectors.
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    norm1 = np.linalg.norm(vec1)  # Length of vector1
    norm2 = np.linalg.norm(vec2)  # Length of vector2

    if norm1 == 0 or norm2 == 0:  # Don't divide by 0 in dot product computation
        return 0.0

    # Formula for cosine similarity is computing dot product of the vectors
    # then dividing by the dot product of their respective lengths
    return np.dot(vec1, vec2) / (norm1 * norm2)


def get_best_course_match(quiz_vector, course_list):
    # Returns the course with the highest cosine similarity to the quiz vector.
    '''
    In the each embedding in course_list, we are storing each course's 
    embedding as a JSON object, which is essentially a string. To compute cosine 
    similarity of each course embedding to the user's quiz embedding, we have to make 
    that string into a list of floats instead. Because we hold the quiz 
    vector as a list of floats, and never enter it into the database during 
    the matching process, we only need to parse the course embedding JSON
    '''
    best_score = -1
    best_course = None #will need throw an error if best_course is Null

    for course in course_list:
        if course.embedding:
            # Ensure embedding is parsed from JSON string to a list of floats
             # Parse JSON string to list
            course_embedding = json.loads(course.embedding) 
            # cosine sim. of each course to quiz vector
            score = cosine_similarity(quiz_vector, course_embedding) 
            print("%s and %s" % (score, best_score))
            if score > best_score:
                #iteratively compare for highest similarity score
                best_score = score 
                best_course = course

    return best_course
