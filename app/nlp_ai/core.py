# =========================================================================================
# Initialization
# =========================================================================================
import stanza
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
fr_stopwords = set(stopwords.words('french'))
stanza.download('fr')

#Constructing Pipeline to get all text processsing tools
nlp_pipeline = stanza.Pipeline('fr')

# =========================================================================================
# Function
# =========================================================================================
def plainTextParser(text):
    return nlp_pipeline(text)

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
    return tab_result

def getRootNodeInSentence(sentence):
    for word in sentence.words:
        if word.head == 0 and word.pos == "VERB":
            return word
    return None

def wordLinkedNodeSelector(sentence: stanza.Document.sentences, root_id, nodeChildType, article=None) -> list:
    children = []
    for word in sentence.words:
        if word.head == root_id:
            if word.pos == nodeChildType:
                if article == 'DET':
                    children.append({'word': word, 'det': wordLinkedNodeSelector(sentence, word.id, article)})
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
            if verbalSentence['subject'] == None:
                verbalSentence['action'].append(verb)
            else:
                temp = searchEngine(verb, sent)
                if temp[0]['subject'] == None:
                    verbalSentence['action'] += temp[0]['action']
                else:
                    result += temp

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
            print('================>\n\n')

    #return
    return result

def umlObjectClassifier(svo : list, verbose: bool = False) -> list:
    #funct
    def getNewStruct():
        return {'d1': None, 's1': None, 'v': None, 'd2': None, 's2': None, 'ss1': [], 'ss2': [], 'obj': []}

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
                t['v'] = obj['verb'].lemma
                t_subj = obj['subject']['main']['word']
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
                    for element in obj['other']:
                        t3 = firstPart.copy()
                        t3['s2'] = element['main']['word'].lemma
                        t3['d2'] = element['main']['det'][0].lemma if len(element['main']['det'])>0 else 'default'
                        if SIMPLE_PASS_SENTENCE:
                            _t3 = t3.copy()
                            _t3['s1'] = t3['s2']
                            _t3['d1'] = t3['d2']
                            _t3['d2'] = t3['d1']
                            _t3['s2'] = t3['s1']
                            _t3['ss1'] = t3['ss2']
                            _t3['ss2'] = t3['ss1']
                            result.append(_t3)
                        else:
                            result.append(t3)
                        for sub in element['linked']:
                            if sub['relation'] == None:
                                if SIMPLE_PASS_SENTENCE:
                                    result[-1]['ss1'].append(sub['word'].lemma)
                                else:
                                    result[-1]['ss2'].append(sub['word'].lemma)
                            else:
                                t3 = firstPart.copy()
                                t3['s2'] = sub['word'].lemma
                                t3['d2'] = sub['det'][0].lemma if len(sub['det'])>0 else 'default'
                                if SIMPLE_PASS_SENTENCE:
                                    _t3 = t3.copy()
                                    _t3['s1'] = t3['s2']
                                    _t3['d1'] = t3['d2']
                                    _t3['d2'] = t3['d1']
                                    _t3['s2'] = t3['s1']
                                    _t3['ss1'] = t3['ss2']
                                    _t3['ss2'] = t3['ss1']
                                    result.append(_t3)
                                else:
                                    result.append(t3)

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

        print(len(svoList))

        for sentObj in svoList:
            potential_class.append(sentObj['s1'])
            if sentObj['s2'] != None:
                potential_attribute.append(sentObj['s2'])
                potential_attribute += sentObj['ss2']
            class_with_desc[sentObj['s1']] = {'name': sentObj['s1'], 'attributes': [], 'methods': [], 'x': 0, 'y': 0, 'width': 0, 'height': 0}

        potential_attribute = list( dict.fromkeys(potential_attribute))

        for _class in potential_class:
            if _class in potential_attribute:
                potential_attribute.remove(_class)

        for sentObj in svoList:
            if sentObj['s2'] in potential_attribute:
                class_with_desc[sentObj['s1']]['attributes'].append(sentObj['s2'])
                class_with_desc[sentObj['s1']]['attributes'] += sentObj['ss2']
            if sentObj['obj']:
                class_with_desc[sentObj['s1']]['methods'] += ([sentObj['v']]+sentObj['obj'])

        for k in class_with_desc.keys():
            result.append(class_with_desc[k])

        if verbose:
            #debug
            for _class in result:
                print(_class)

        return result

    def getRelationType(verb: str) -> str:
        return 'ASSOCIATION'

    def getMultiplicity(verb: str) -> str:
        cardinality_reper ={'chaque': '1,1', 'un et un seul':'1,1', 'un':'1,1', 'des':'0,*', 'plusieurs':'0,*', 'au moins':'1,*'}
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
                temp = {'t1': sentence['s1'], 't2': sentence['s2'], 'type': getRelationType(sentence['v']), 'c1': getMultiplicity(sentence['d1']), 'c2': getMultiplicity(sentence['d2']), 'direction': 'b', 'label': sentence['v']}
                potentialRelation.append(temp)

        if verbose:
            #debug
            for relation in potentialRelation:
                print(relation)

        return potentialRelation

    #main
    table = classExtractor(svoList, verbose=False)
    relation = relationExtractor(svoList, table, verbose=True)

    #return
    return {'allNodes': table, 'relation': relation}
