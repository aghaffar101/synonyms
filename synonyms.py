'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math



def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    if vec1 == {}:
        return -1
    if vec2 == {}:
        return -1
    #make a list of the words in each dictionary
    words_vec1 = list(vec1.keys())
    words_vec2 = list(vec2.keys())
    # make a list of the common words
    common_words = []
    for key, value in vec1.items():
        if key in words_vec2:
            common_words.append(key)
    #calculate the numerator
    numerator = 0
    for word in common_words:
        numerator = numerator + (vec1[word] * vec2[word])

    mod_vec1 = 0
    for key, value in vec1.items():
        mod_vec1 = mod_vec1 + (value**2)
    mod_vec1 = math.sqrt(mod_vec1)
    mod_vec2 = 0
    for key, value in vec2.items():
        mod_vec2 = mod_vec2 + (value**2)
    mod_vec2 = math.sqrt(mod_vec2)


    denominator = mod_vec1 * mod_vec2

    res = float(numerator/denominator)

    return res



def build_semantic_descriptors(sentences):
    #need to create a dictionary for every word, which includes the other words
    #that appeared in that sentence. Must do this without having a complexity
    #of O(n^2) where n is the number of words in the file.
    semantic_d = {}
    for sentence in sentences:
        #get rid of duplicates
        word_set = set(sentence)
        l_words = list(word_set)
        for word in word_set:
            if word not in semantic_d.keys():
                semantic_d[word] = {}
            for i in range(len(l_words)):
                if l_words[i] == word:
                    continue
                semantic_d[word][l_words[i]] = semantic_d[word].get(l_words[i],0) + 1

    return semantic_d




#punctuation l is [",", "-", "--", ":", ";"]

def build_semantic_descriptors_from_files(filenames):
    punct = [",", "-", "--", ":", ";"]
    semantic_d = {}
    for file in filenames:
        fhandle = open(file, "r", encoding="utf-8")
        text = fhandle.read()
        text = text.lower()
        for p in punct:
            text = text.replace(p," ")
        text = text.replace("!", ".")
        text = text.replace("?", ".")
        sentences = text.split(".")
        sentence_list = []
        #print(sentences[1:20])
        for sentence in sentences:
            words = sentence.split()
            sentence_list.append(words)
        semantic_df = build_semantic_descriptors(sentence_list)

        for word, dict in semantic_df.items():
            if word not in semantic_d.keys():
                semantic_d[word] = dict
                #print(semantic_d)
                continue
            for sub_word,value in dict.items():
                semantic_d[word][sub_word] = semantic_d[word].get(sub_word,0) + value
                #print(semantic_d)
    return semantic_d




def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]
    vec1 = semantic_descriptors[word]
    best_index = 0
    best_score = 0
    for i in range(len(choices)):
        if choices[i] not in semantic_descriptors:
            continue
        vec2 = semantic_descriptors[choices[i]]
        similarity = similarity_fn(vec1, vec2)
        if similarity > best_score:
            best_score = similarity
            best_index = i

    return choices[best_index]




def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    fhandle = open(filename, "r", encoding="latin1")
    text = fhandle.read()
    lines = text.splitlines()
    list_words = []
    for line in lines:
        words = line.split()
        list_words.append(words)
    total_questions = len(list_words)
    correct_answers = 0
    for question in list_words:
        answer = question[1]
        choices = question[2:]
        word = question[0]
        est = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
        if est == answer:
            correct_answers += 1
    percentage = (float(correct_answers/total_questions)) * 100
    return percentage



# if __name__ == "__main__":
#     semantic_descriptors = build_semantic_descriptors_from_files(["warandpeace.txt", "sw.txt"])
#     res = run_similarity_test("test.txt", semantic_descriptors, cosine_similarity)
#     print(res)














