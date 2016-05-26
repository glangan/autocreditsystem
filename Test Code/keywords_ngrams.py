from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

#extract keywords from n-grams
def keywords(file):
    unit_file = open(file).read()
    terms_file = open('Dictionary.txt', 'r')

    terms = terms_file.readlines()
    terms = [t.rstrip('\n') for t in terms]
    terms = [t.lower() for t in terms]

    words = word_tokenize(unit_file)
    words = [w.lower() for w in words]
    #convert all words to base form e.g. structures -> structures
    lmtzr = WordNetLemmatizer()
    words = [str(lmtzr.lemmatize(w)) for w in words]

    #create bigrams and trigrams from words
    words_bigram = [words[i:i+2] for i in xrange(len(words)-2)]
    words_trigram = [words[i:i+3] for i in xrange(len(words)-3)]

    #convert list of lists to list of strings
    words_bigram = [w[0] + ' ' + w[1] for w in words_bigram]
    words_trigram = [w[0] + ' ' + w[1] + ' ' + w[2] for w in words_trigram]

    #combine all lists
    words = words + words_bigram + words_trigram
    terms = [term.rstrip('\n') for term in terms]

    #find common terms
    common_terms = set(terms) & set(words)

    common_terms = list(common_terms)
    #remove smaller keywords from larger keywords
    for term in common_terms:
        if ' ' in term:
            for t in common_terms:
                if (t in term and t != term):
                    common_terms.remove(t)

    return common_terms
