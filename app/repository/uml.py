from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
# from ..nlp_ai import core as ai
# from ..nlp_ai import trace as trace
# from ..nlp_ai import xmlBuilder as xmlTools

def toClassDigramXML(request: schemas.UMLText):
    try:
        #get plain text
        text = request.text

        # syntaxic analysis
        doc = ai.plainTextParser(text)
        # semantic analysis
        svo = ai.atomicSentenceMaker(doc, verbose=False)
        # Classifier Layer1
        firstClassification = ai.umlObjectClassifier(svo, verbose=False)
        # Classifier Layer2
        diagramObject = ai.umlObjectExtractor(firstClassification)

        #xml formater
        xml = xmlTools.main(diagramObject) 

        #result
        result = schemas.ShowUMLSchema(xml=xml)
        return result
    except Exception as e:
        trace.save_log(request.text, e)
        raise HTTPException(status_code=500, detail='NLP Pipline code error')
        return "AN ERROR OCCUR"
   

def toClassDigramOBJ(request: schemas.UMLText):
    try:
        #get plain text
        text = request.text

        # syntaxic analysis
        doc = ai.plainTextParser(text)
        # semantic analysis
        svo = ai.atomicSentenceMaker(doc, verbose=False)
        # Classifier Layer1
        firstClassification = ai.umlObjectClassifier(svo, verbose=False)
        # Classifier Layer2
        diagramObject = ai.umlObjectExtractor(firstClassification)

        #result
        return diagramObject
    except Exception as e:
        trace.save_log(request.text, e)
        raise HTTPException(status_code=500, detail='NLP Pipline code error')
        return "AN ERROR OCCUR"

def sentenceSplit(request: schemas.UMLText):
    try:
        #get plain text
        text = request.text

        # syntaxic analysis
        doc = ai.plainTextParser(text)
        # semantic analysis
        svo = ai.atomicSentenceMaker(doc, verbose=False)
        # Classifier Layer1
        firstClassification = ai.umlObjectClassifier(svo, verbose=False)

        #result
        return firstClassification
    except Exception as e:
        trace.save_log(request.text, e)
        raise HTTPException(status_code=500, detail='NLP Pipline code error')
        return "AN ERROR OCCUR"

def stanzaPipeline(request: schemas.UMLText):
    try:
        #get plain text
        text = request.text

        # syntaxic analysis
        doc = ai.plainTextParser(text)

        #result
        return ai.text_parser(doc)
    except Exception as e:
        trace.save_log(request.text, e)
        raise HTTPException(status_code=500, detail='NLP Pipline code error')
        return "AN ERROR OCCUR"
