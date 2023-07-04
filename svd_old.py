from nltk.tokenize import sent_tokenize
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

def real_text_preprocessing(text):
    return sent_tokenize(text)

def text_preprocessing(text):
    print("\n\n=======================================")
    print("TEXT PREPROCESSING")
    print("=======================================")

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
    print(f"\nLOWERCASE + TOKENIZE TO SENTENCES + REMOVE PUNCTUATION + REMOVE NUMBER\n>>",sentences)

    # STOPWORDS REMOVAL
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    temp = []
    for sentence in sentences:
        sentence = stopword.remove(sentence)
        temp.append(sentence)
    sentences = temp
    print(f"\nSTOPWORDS REMOVAL\n>>",sentences)

    #STEMMING
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    temp = []
    for sentence in sentences:
        sentence = stemmer.stem(sentence)
        temp.append(sentence)
    sentences = temp
    print(f"\nSTEMMING\n>>",sentences)

    return sentences


def svd(text):
    print("\n\n=======================================")
    print("TF-IDF")
    print("=======================================")
    vectorizer = TfidfVectorizer()
    text_matrix = vectorizer.fit_transform(text)
    print(f"\nMATRIX TF IDF TEXT\n>>",text_matrix.toarray())

    svd = TruncatedSVD(n_components=2)  # Jumlah komponen
    text_matrix = svd.fit_transform(text_matrix)

    print(f"\nSVD MATRIX\n>>",text_matrix)
    return text_matrix

def result(text_matrix, real_text, count):
    print("\n\n=======================================")
    print("RANKING SCORE")
    print("=======================================")
    sentence_scores = [(i, score) for i, score in enumerate(text_matrix[:, 0])]
    sentence_scores = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    top_sentences = sentence_scores[0:int(count)]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])
    print(f">>",top_sentences)

    print("\n\n=======================================")
    print("RESULT")
    print("=======================================")

    result = ' '.join([real_text[i] for i, score in top_sentences])
    
    print(f">>",result,"\n\n\n")
    return result

def main(title, text, count):
    real_text = real_text_preprocessing(text)
    text = text_preprocessing(text)
    similarity_matrix = svd(text)
    summary = result(similarity_matrix, real_text, count)
    return summary
