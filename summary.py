from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


def real_text_preprocessing(text):
    return sent_tokenize(text)

def title_preprocessing(title):
    # LOWERCASE + TOKENIZE TO SENTENCES + REMOVE PUNCTUATION + REMOVE NUMBER
    title = title.lower()
    title = re.sub(r'[^\w\s]','',title) #Remove punctuation
    title = re.sub(r'\w*\d\w*','',title) #Remove number

    # STOPWORDS REMOVAL
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    title = stopword.remove(title)

    #STEMMING
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    title = stemmer.stem(title)

    #TOKENIZE TO WORDS
    words = word_tokenize(title)

    #REMOVE DUPLICATE WORDS
    words = set(words)

    return words

def text_preprocessing(text):
    # LOWERCASE + TOKENIZE TO SENTENCES + REMOVE PUNCTUATION + REMOVE NUMBER
    text = text.lower()
    sentences = sent_tokenize(text)
    temp = []
    for sentence in sentences:
        sentence = re.sub(r'[^\w\s]','',sentence) #Remove punctuation
        sentence = re.sub(r'\w*\d\w*','',sentence) #Remove number
        if sentence != None:
            temp.append(sentence)
        else:
            temp.append(".")
    sentences = temp

    # STOPWORDS REMOVAL
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    temp = []
    for sentence in sentences:
        sentence = stopword.remove(sentence)
        temp.append(sentence)
    sentences = temp

    #STEMMING
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    temp = []
    for sentence in sentences:
        sentence = stemmer.stem(sentence)
        temp.append(sentence)
    sentences = temp

    #TOKENIZE TO WORDS
    words = [word_tokenize(word) for word in sentences]

    #REMOVE DUPLICATE WORDS
    words = [set(word) for word in words]

    return words

def jaccard_similarity(title, text):
    # CALCULATE JACCARD SIMILARITY
    temp = []
    for t in text:
        if(t == set()):
            temp.append(0)
            continue
        j = float(len(title.intersection(t))) / len(title.union(t))
        temp.append(j)
    return enumerate(temp)

def similarity_ranking(similarity):
    return sorted(similarity,key=lambda s:s[1],reverse=True)

def result(ranking, real_text, count):
    temp = []
    for i in range(int(count)):
        for j, rank in enumerate(ranking):
            if i == j:
                temp.append(real_text[rank[0]])
                break
    result = ' '.join([str(t) for t in temp])
    return result

def main(title, text, count):
    real_text = real_text_preprocessing(text)
    title = title_preprocessing(title)
    text = text_preprocessing(text)
    similarity = jaccard_similarity(title, text)
    ranking = similarity_ranking(similarity)
    summary = result(ranking, real_text, count)
    return summary
