from django.shortcuts import render
import spacy
from nltk.corpus import stopwords


nlp = spacy.load('en_core_web_lg')
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize
stopWords = set(stopwords.words("english"))

def search(pat, txt, q):
        d = 256
        count = 0
        M = len(pat)
        N = len(txt)
        i = 0
        j = 0
        p = 0  # hash value for pattern
        t = 0  # hash value for txt
        h = 1
        # The value of h would be "pow(d, M-1)%q"
        for i in range(M - 1):
            h = (h * d) % q
        # Calculate the hash value of pattern and first window
        # of text
        for i in range(M):
            p = (d * p + ord(pat[i])) % q
            t = (d * t + ord(txt[i])) % q
        # Slide the pattern over text one by one
        for i in range(N - M + 1):
            # Check the hash values of current window of text and
            # pattern if the hash values match then only check
            # for characters one by one
            if p == t:
                # Check for characters one by one
                for j in range(M):
                    if txt[i + j] != pat[j]:
                        break
                    else:
                        j += 1
                # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
                if j == M:
                    count += 1
            # Calculate hash value for next window of text: Remove
            # leading digit, add trailing digit
            if i < N - M:
                t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
                # We might get negative values of t, converting it to
                # positive
                if t < 0:
                    t = t + q
        return count

def robin(keywords,text, summary_length):
    q = 101
    newdict = {}
    keywords = list(map(str, keywords.split(',')))
    for i in keywords:
        newdict[i] = 0

    for pat in keywords:
        try:
            newdict[pat] = search(pat.lower(), text.lower(), q)
        except:
            pass

    doc = nlp(text)
    text = []
    for i in doc.sents:
        i = str(i)
        message = i.split('\n.')
        text.append(message[0])
    relevant_sentences = []

    # for single keyword
    # l = sorted(newdict.items(), key=lambda kv:
    # (kv[1], kv[0]))[-1][0]

    for sentence in text:
        sentence = str(sentence)
        for keyword in keywords:
            if keyword.lower() in sentence.lower():
        #if l.lower() in sentence.lower():
                relevant_sentences.append(sentence.strip())

    document1 = "".join(relevant_sentences)

    words = word_tokenize(document1)
    # Creating a frequency table to keep the
    # score of each word
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    # Creating a dictionary to keep the score
    # of each sentence
    sentences = sent_tokenize(document1)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    # Average value of a sentence from the original text
    average = 1
    if len(sentenceValue) != 0:
        average = int(sumValues / len(sentenceValue))
    # Storing sentences into our summary.
    summary = ''
    if summary_length == 'one_third':
        target_length = len(sentences) // 3
    elif summary_length == 'two_thirds':
        target_length = 2 * (len(sentences) // 3)
    else:
        target_length = len(sentences)
    
    current_length = 0
    for sentence in sentences:
        if sentence in sentenceValue and current_length < target_length:
            summary += " " + sentence
            current_length += 1


    


    '''
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    
    '''
    lst = set()
    for i in newdict.items():
        lst.add(i[0])

    """summary Statistic part"""
    
    summary_count = count_paragraphs_helper(summary)
    summary_lines = count_lines_helper(summary)
    summary_updated_lines = count_lines(summary)
    summary_char_count = character_count(summary)
    summary_char_count_one = count_char_one(summary)
    summary_word_count = count_words(summary)
    summary_pages = count_pages(summary)


    params = {   'sum': sorted(newdict.items(), key=lambda kv:(kv[1], kv[0])), 
              
                 'Summary': summary, 
                 'Text':text[0], 
                 "Keywords": lst,

                    #summary Statistic part

                'summary_count': summary_count,
                'summary_lines': summary_lines,
                #'summary_updated_lines': summary_updated_lines,
                'summary_char_count': summary_char_count,
                'summary_char_count_one': summary_char_count_one,
                'summary_word_count': summary_word_count,
                'summary_pages': summary_pages
                 
                 
                 
                 
                 }
    return params
    


    """summary Statistic part"""
import re

def count_paragraphs_helper(text):
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return len(paragraphs)

def count_lines_helper(text):
    sentences = re.split(r'\.\s+', text)
    
    line_count = len(sentences)
    return line_count

def count_pages(text):
    
    lines_per_page = 50
    lines = count_lines_helper(text)
    pages = lines // lines_per_page
    if lines % lines_per_page != 0:
        pages += 1
    return pages

def character_count(text):
    c = 0
    for i in range(len(text)):
        if text[i] != " ":
            c += 1
    return c

def count_char_one(text):
    return len(text)

def count_words(text):
    words = text.split()
    return len(words)

def count_lines(text):
    lines = re.split(r'\.\s+', text)
    formatted_lines = '<br>'.join(lines)
    return formatted_lines



