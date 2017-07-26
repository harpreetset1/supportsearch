'''
Created on Jul 6, 2017

@author: harpreetsethi
'''
from gensim import corpora, models, similarities
#from py_utils import extract_keywords
import os.path, json, nltk
from stop_words import get_stop_words

def get_concept(word_list):
    stoplist = get_stop_words('en')
    stemmer = nltk.stem.PorterStemmer()
    words=set()
    for word in word_list:
        if (len(word)>2 and word not in stoplist):
            words.add(stemmer.stem(word))
    #print('word_list',words)
    return words

def search_concepts(doc):
    if(os.path.exists('./support_1.0.pkl')):
        print('support model exists')
        with open('./q_and_a_text2.txt','r', encoding="utf-8") as f:
            lines = f.readlines()

            model = models.LsiModel.load('./support_1.0.pkl')
            dictionary = corpora.Dictionary.load_from_text('./support_1.0.dict')
            corpus = corpora.MmCorpus('./support_1.0.mm')
    else:
        print('support model doesnt exist')
        return {}
       
    input_data=list()
    input_data.extend(get_concept(doc.lower().split()))
    #input_data.extend(extract_keywords.get_keywords(doc.lower()))
    vec_bow = dictionary.doc2bow(input_data)
    
    vec_model = model[vec_bow]
    index = similarities.MatrixSimilarity(model[corpus])
    sims = index[vec_model] 
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    idx=0
    results = []
    for x in sims:
        if (idx<10):
            res={}
            #print('%s : %s' % (x[1],lines[x[0]]))
            res['score']=str(x[1])
            res['text']=(lines[x[0]])
            idx+=1
            results.append(res)
        else:
            break
    print(results)
    return json.dumps(results)

