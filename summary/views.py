
from django.shortcuts import render
from requests import request
from .utils import  robin

import re




# Create your views here.
# Create your views here.



def tool(request):
    
    
    if request.method == 'POST':
        show_statistics = False
        text = request.POST.get("description").lower()
        keywords = request.POST.get("keywords")

        summary_length = request.POST.get("summary_length")  

        context = robin(keywords,text, summary_length)
    
        context['oldDescription'] = text

        '''statistic starts'''

        count = count_paragraphs_helper(text)
        lines = count_lines_helper(text)
        updated_lines = count_lines(text)
        char_count = character_count(text)
        char_count_one = count_char_one(text)
        word_count = count_words(text)
        pages = count_pages(text)
        
        show_statistics = True


        context.update({
            'count': count,
            'lines': lines,
            'pages': pages,
            'text': text,
            'updated_lines': updated_lines,
            'char_count': char_count,
            'char_count_one': char_count_one,
            'word_count': word_count,
            'show_statistics' : show_statistics,
            
        })


        '''statistic ends''' 

        top_keywords = summarize_text(text)

        context.update({
             
             
             'top_keywords': top_keywords,
        })
        return render(request,'index.html',context)
       
    return render(request, 'index.html')



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



import string
from django.shortcuts import render
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def summarize_text(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words and word not in punctuation]

    keyword_counts = Counter(filtered_words)  
    top_keywords = keyword_counts.most_common(10) 

    return top_keywords


'''

from rake_nltk import Rake


def get_top_keywords_with_rake(text, num_keywords=10):
    r = Rake()  # Initialize the RAKE extractor
    r.extract_keywords_from_text(text)  # Extract keywords from the text
    keyword_scores = r.get_word_degrees()  # Get keyword scores (single words)
    
    # Convert decimal scores to integers
    for word, score in keyword_scores.items():
        keyword_scores[word] = int(round(score))  # Convert and round the score to an integer
    
    # Filter out numeric keywords
    non_numeric_keywords = {word: score for word, score in keyword_scores.items() if not word.isnumeric()}
    
    # Sort the non-numeric keywords by score in descending order
    sorted_keywords = sorted(non_numeric_keywords.items(), key=lambda x: x[1], reverse=True)
    
    # Select the top N keywords
    top_keywords = sorted_keywords[:num_keywords]
    
    return top_keywords

'''



