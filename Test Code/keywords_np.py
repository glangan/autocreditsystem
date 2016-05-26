import nltk, re
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

#extract keywords based on POS tags
def keywords(file):
    file = open(file).read()

    words = nltk.word_tokenize(file)  #word tokenize

    #filter
    chunkGram = r"""
        NN: {<NN\w?|JJ>*<NN\w?>+}
        """
    chunkParser = nltk.RegexpParser(chunkGram)
    final = []
    pre_chunk = nltk.pos_tag(words)
    chunked = chunkParser.parse(pre_chunk)
    result = []
    for subtree in chunked.subtrees(filter = lambda t: t.label() != 'S'):
        result.append(subtree.leaves())
        for r in result:
            s = ""
            for x, y in r:
                s = s + " " + x
        final.append(s.strip())
    return final

#match with dictionary terms
def match_dict(filename):
    terms_file = open('Dictionary.txt', 'r')
    terms = terms_file.readlines()
    terms = [term.rstrip('\n') for term in terms]

    words = keywords(filename)
    words = [w.lower() for w in words]

    lmtzr = WordNetLemmatizer()
    words = [str(lmtzr.lemmatize(w)) for w in words]

    common_terms = set(terms) & set(words)

    common_terms = list(common_terms)

    for term in common_terms:
        if ' ' in term:
            for t in common_terms:
                if (t in term and t != term):
                    common_terms.remove(t)

    return common_terms
