# =========================================================================================
# Initialization
# =========================================================================================
import stanza
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

stanza.download('fr')

from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
nltk.download('words')
from nltk.corpus import words
correct_words = words.words()

#Constructing Pipeline to get all text processsing tools
nlp_pipeline = stanza.Pipeline('fr')

#load keys word
AGREGATION_LIST = []
with open('app/nlp_ai/src/aggregation_keyword.txt') as file:
    for word in file:
        AGREGATION_LIST.append(word.strip())

# =========================================================================================
# Function
# =========================================================================================
def get_input_text():
    plain_text = str(input('Input : '))
    return plain_text

def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append(list())
    return list_of_objects

def preview(doc):
    for i, sent in enumerate(doc.sentences):
        print("[Sentence {}]".format(i+1))
        for word in sent.words:
            print("{:12s}\t{:12s}\t{:6s}\t{:d}\t{:12s}".format(\
              word.text, word.lemma, word.pos, word.head, word.deprel))

def text_parser(doc):
    tab_result = []
    for i, sent in enumerate(doc.sentences):
        sentence_size = len([i for i in sent.words])
        data = init_list_of_objects(sentence_size)
        
        for j, word in enumerate(sent.words):
            data[j].append(word.text)
            data[j].append(word.lemma)
            data[j].append(word.pos)
            data[j].append(word.deprel)
            data[j].append(word.head)
        tab_result.append({"Sentence {}".format(i+1):data})
        
    print("-"*55)
    preview(doc)
    print("-"*55)
    return tab_result

def plainTextParser(text):
    escape = re.compile(re.escape('a chaque'), re.IGNORECASE)
    text2 = escape.sub('un', text)
    escape = re.compile(re.escape('.'), re.IGNORECASE)
    text2 = escape.sub(' . ', text2)
    escape = re.compile(re.escape('au plus une'), re.IGNORECASE)
    text2 = escape.sub('un *', text2)
    escape = re.compile(re.escape('au moins une'), re.IGNORECASE)
    text2 = escape.sub('un -', text2)
    escape = re.compile(re.escape('au plus un'), re.IGNORECASE)
    text2 = escape.sub('un *', text2)
    escape = re.compile(re.escape('au moins un'), re.IGNORECASE)
    text2 = escape.sub('un -', text2)
    escape = re.compile(re.escape('un ou deux'), re.IGNORECASE)
    text2 = escape.sub('un --', text2)
    escape = re.compile(re.escape('1'), re.IGNORECASE)
    text2 = escape.sub('un', text2)
    escape = re.compile(re.escape('beaucoup'), re.IGNORECASE)
    text2 = escape.sub('plusieurs', text2)
    return nlp_pipeline(text2)

def getRootNodeInSentence(sentence):
    for word in sentence.words:
        """
        Updated on 23 August: Comment pos control help us to identify non verbal root 
        sentence and consider them as generalization management rules.
        """
        if word.head == 0:# and word.pos == "VERB":
            return word
    return None

def wordLinkedNodeSelector(sentence: stanza.Document.sentences, root_id, nodeChildType, article=None) -> list:
    children = []
    for word in sentence.words:
        if word.head == root_id:
            if word.pos == nodeChildType:
                if article == 'DET':
                    det = wordLinkedNodeSelector(sentence, word.id, article)
                    punct = wordLinkedNodeSelector(sentence, word.id, 'PUNCT')
                    if len(punct) != 0:
                        det[0].lemma=(det[0].lemma+punct[0].lemma)
                    children.append({'word': word, 'det': det})
                else:
                    children.append(word)
            elif ((word.pos == 'VERB' and word.deprel == "xcomp") or (word.pos != 'VERB')) and (article != None):
                children += wordLinkedNodeSelector(sentence, word.id, nodeChildType, article)
    return children

def searchEngine(root, sent) -> list:
    if root != None:
        #var
        result = []
        verbalSentence = {'verb': root, 'subject': None, 'other': [], 'action': []}

        #logic1
        linkedNoun = wordLinkedNodeSelector(sent, root.id, 'NOUN', 'DET')
        for noun in linkedNoun:
            subNoun = wordLinkedNodeSelector(sent, noun['word'].id, 'NOUN', 'DET')
            for i, n in enumerate(subNoun):
                linkedByConjunction = wordLinkedNodeSelector(sent, n['word'].id, 'CCONJ')
                if len(linkedByConjunction) != 0 and 'nsubj' in noun['word'].deprel:
                    subNoun[i]['relation'] = "cconj"
                else:
                    subNoun[i]['relation'] = None
            
            if 'nsubj' in noun['word'].deprel:
                verbalSentence['subject'] = {'main': noun, 'linked': subNoun}
            else:
                verbalSentence['other'].append({'main': noun, 'linked': subNoun})

        #logic2
        linkedVerb = wordLinkedNodeSelector(sent, root.id, 'VERB')  
        for verb in linkedVerb:
            if verb.deprel == 'xcomp':
                verbalSentence['verb'] = verb
            if verbalSentence['subject'] == None and verbalSentence['verb'].deprel != 'xcomp':
                verbalSentence['action'].append(verb)
            else:
                temp = searchEngine(verb, sent)  
                for data in temp:
                    if data['subject'] == None:
                        verbalSentence['action'] += [data['verb']]
                        verbalSentence['action'] += data['action']
                    else:
                        result += [data]
        
        #return
        return [verbalSentence] + result
    return []

def atomicSentenceMaker(doc: stanza.Document, verbose: bool = False) -> list:
    result = []
    for sent in doc.sentences:
        root = getRootNodeInSentence(sent)
        structuredSentence = searchEngine(root, sent)
        result.append(structuredSentence)
        
        #debug
        if verbose == True:
            print(structuredSentence)
    
    #return
    return result

def umlObjectClassifier(svo : list, verbose: bool = False) -> list:
    #funct
    def getNewStruct():
        return {'d1': None, 's1': None, 'v': None, 'd2': None, 's2': None, 'ss1': [], 'ss2': [], 'obj': [], 'sens': 'toRight'}
    
    #data
    result = []
    template = []
    SIMPLE_PASS_SENTENCE = False
    
    #logic1
    for structObj in svo:
        for obj in structObj:
            template = []
            if obj['subject'] != None:
                t = getNewStruct()
                if obj['verb'].upos == 'NOUN':
                    t['v'] = 'sorte'
                else:
                    t['v'] = obj['verb'].lemma
                t_subj = obj['subject']['main']['word']
                if obj['verb'].upos == 'NOUN' and obj['other'] == []:
                    t_otherList = [{'main': {'word': obj['verb'], 'det': []}, 'linked': []}]
                elif obj['verb'].upos == 'NOUN' and len(obj['other']) > 0 and obj['other'][0]['main']['word'].deprel == 'conj':
                    t_otherList = obj['other']+[{'main': {'word': obj['verb'], 'det': []}, 'linked': []}]
                else:
                    t_otherList = obj['other']
                    
                for element in obj['action']:
                    t['obj'].append(element.lemma)

                SIMPLE_PASS_SENTENCE = True if 'pass' in t_subj.deprel else False
                
                t['s1'] = t_subj.lemma
                t['d1'] = obj['subject']['main']['det'][0].lemma if len(obj['subject']['main']['det'])>0 else 'default'
                for element in obj['subject']['linked']:
                    if element['relation'] == None:
                        t['ss1'].append(element['word'].lemma)
                    else:
                        t2 = t.copy()
                        t2['s1'] = element['word'].lemma
                        t2['d1'] = element['det'][0].lemma if len(element['det'])>0 else 'default'
                        template.append(t2)
                template.append(t)

                for firstPart in template:
                    for element in t_otherList:
                        t3 = firstPart.copy()
                        t3['s2'] = element['main']['word'].lemma
                        t3['d2'] = element['main']['det'][0].lemma if len(element['main']['det'])>0 else 'default'
                        if SIMPLE_PASS_SENTENCE:
                            _t3 = t3.copy()
                            _t3['sens'] = 'toLeft'
#                             _t3['ss1'] = t3['ss2']
#                             _t3['ss2'] = t3['ss1']
#                             _t3['s1'] = t3['s2']
#                             _t3['d1'] = t3['d2']
#                             _t3['d2'] = t3['d1']
#                             _t3['s2'] = t3['s1']
                            result.append(_t3)
                        else:
                            result.append(t3)
                        for sub in element['linked']:
                            if sub['relation'] == None:
                                if SIMPLE_PASS_SENTENCE:
                                    result[-1]['ss2'].append(sub['word'].lemma)
                                else:
                                    result[-1]['ss2'].append(sub['word'].lemma)
                            else:                      
                                t3 = firstPart.copy()
                                t3['s2'] = sub['word'].lemma
                                t3['d2'] = sub['det'][0].lemma if len(sub['det'])>0 else 'default'
                                if SIMPLE_PASS_SENTENCE:
                                    _t3 = t3.copy()
                                    _t3['sens'] = 'toLeft'
#                                     _t3['ss1'] = t3['ss2']
#                                     _t3['ss2'] = t3['ss1']
#                                     _t3['s1'] = t3['s2']
#                                     _t3['d1'] = t3['d2']
#                                     _t3['d2'] = t3['d1']
#                                     _t3['s2'] = t3['s1']
                                    result.append(_t3)
                                else:
                                    result.append(t3)
                    
                    if not t_otherList:
                        result += template

                if result == []:
                    result = template

    #debug
    if verbose:
        for parseData in result:
            print(parseData)
            print('---------')
        
    #return
    return result

def umlObjectExtractor(svoList : list, verbose: bool = False) -> dict:
    #function
    def classExtractor(svoList: list, verbose: bool = False) -> list:
        class_with_desc = {}
        potential_class = []
        potential_attribute = []
        result = []
        svoListCopy = svoList.copy()
        
        #generalization sentences
        mirrorStruct = []
        for sentObj in svoListCopy:
            if sentObj['v'] == 'sorte':
                temp = sentObj.copy()
                temp['d1'] = sentObj['s2']
                temp['s1'] = sentObj['s2']
                temp['d2'] = sentObj['s1']
                temp['s2'] = sentObj['s1']
                temp['ss1'] = sentObj['ss2']
                temp['ss2'] = sentObj['ss1']
                mirrorStruct.append(temp)
        svoListCopy += mirrorStruct   
        
        for sentObj in svoListCopy:
            potential_class.append(sentObj['s1'])
            if sentObj['s2'] != None:
                potential_attribute.append(sentObj['s2'])
                potential_attribute += sentObj['ss2']            
            class_with_desc[sentObj['s1']] = {'name': sentObj['s1'], 'attributes': [], 'methods': [], 'x': 0, 'y': 0, 'width': 0, 'height': 0}
           
        potential_attribute = list(dict.fromkeys(potential_attribute))
        
        for _class in potential_class:
            if _class in potential_attribute:
                potential_attribute.remove(_class)
            
        for sentObj in svoListCopy:
            if sentObj['s2'] in potential_attribute:
                class_with_desc[sentObj['s1']]['attributes'].append(sentObj['s2'])
                class_with_desc[sentObj['s1']]['attributes'] += sentObj['ss2']
            if sentObj['obj']:
                class_with_desc[sentObj['s1']]['methods'] += list(set([sentObj['v']]+sentObj['obj']))
                class_with_desc[sentObj['s1']]['methods'] = list(set(class_with_desc[sentObj['s1']]['methods']))

        for k in class_with_desc.keys():
            result.append(class_with_desc[k])
            
        if verbose:
            #debug
            for _class in result:
                print(_class)

        return result
    
    def getRelationType(verb: str, sens: str = 'toRight', reflexive: bool = False) -> str:
        if reflexive:
            return 'RASSOCIATION'
        elif verb in AGREGATION_LIST:
            return 'AGGREGATION' if sens == 'toRight' else 'COMPOSITION'
        elif verb == 'sorte':
            return 'GENERALISATION'
        else:
            return 'ASSOCIATION'
    
    def getMultiplicity(verb: str) -> str:
        cardinality_reper ={'un-':'1,*', 'un*':'0,1', 'un--':'1,2', 'aucun': '0, 0', 'tout': '0.*', 'tous':'0.*', 'chaque': '1,1', 'un et un seul':'1,1', 'un':'1,1', 'des':'0,*', 'plusieurs':'0,*'}
        for search_val in cardinality_reper.keys():
            combined = "(" + ")|(".join(search_val) + ")"
            if search_val in verb:
                return cardinality_reper[search_val]
        return ""
    
    def relationExtractor(svoList: list, classDesc: list, verbose: bool = False) -> list:
        potentialRelation = []
        className = [elem['name'] for elem in classDesc]
        for sentence in svoList:
            if sentence['s1'] in className and sentence['s2'] in className:
                temp = {'t1': sentence['s1'], 't2': sentence['s2'], 'type': getRelationType(sentence['v'], sens=sentence['sens'], reflexive=(sentence['s1']==sentence['s2'])), 'c1': getMultiplicity(sentence['d1']), 'c2': getMultiplicity(sentence['d2']), 'direction': 'a' if (sentence['sens'] == 'toLeft') else 'b', 'label': sentence['v'], 't3': None, 'c3': ''}
                if temp['type'] == 'GENERALISATION':
                    temp['c1'], temp['c2'], temp['label'] = '', '', ''
                potentialRelation.append(temp)
            for ss2 in sentence['ss2']:
                if sentence['s1'] in className and ss2 in className:
                    temp = {'t1': sentence['s1'], 't2': ss2, 'type': getRelationType(sentence['v'], sens=sentence['sens'], reflexive=(sentence['s1']==sentence['s2'])), 'c1': getMultiplicity(sentence['d1']), 'c2': getMultiplicity(sentence['d2']), 'direction': 'a' if (sentence['sens'] == 'toLeft') else 'b', 'label': sentence['v'], 't3': None, 'c3': ''}
                    if temp['type'] == 'GENERALISATION':
                        temp['c1'], temp['c2'], temp['label'] = '', '', ''
                    potentialRelation.append(temp)

        if verbose:
            #debug
            for relation in potentialRelation:
                print(relation)

        return potentialRelation
    
    #main
    table = classExtractor(svoList, verbose=False)
    relation = relationExtractor(svoList, table, verbose=False)
    
    #filter duplicate
    relationFilter = []
    for rel in relation:
        find1 = False
        find2 = False
        for relChecked in relationFilter:
            if((relChecked['t1'] == rel['t1']) and (relChecked['t2'] == rel['t2'])):
                find1 = True
                break;
        if not find1:
            for i, relChecked in enumerate(relationFilter):
                if((relChecked['t1'] == rel['t2']) and (relChecked['t2'] == rel['t1'])):
                    find2 = True
                    break
            if not find2:
                relationFilter.append(rel)
                
    #find class association
    for i, relationMaster in enumerate(relationFilter):
        for j, relation in enumerate(relationFilter):
            if relationMaster['t1'] == relation['t1'] and relationMaster['label'] == relation['label'] and relationMaster['t2'] != relation['t2']:
                relationFilter[j]['t3'] = relationMaster['t2']
                relationFilter[j]['c3'] = relationMaster['c2']
                relationFilter[j]['type'] = 'NASSOCIATION'
                relationFilter.pop(i)
                break
                
    if verbose:
        #debug
        for relation in relationFilter:
            print(relation)
    
    #return
    return {'allNodes': table, 'relation': relationFilter}


def typosTracker(potential_incorrect_words: list = [], verbose: bool = False) -> list:
    temp = []
    for word in potential_incorrect_words:
        temp = [(jaccard_distance(set(ngrams(word, 2)), set(ngrams(w, 2))) ,w) for w in correct_words if w[0]==word[0]]
    if verbose:
        print(sorted(temp, key = lambda val:val[0])[0][1])
    return sorted(temp, key = lambda val:val[0])[0][1]
# checkpoint - 202208231158
