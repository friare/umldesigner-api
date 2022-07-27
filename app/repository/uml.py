from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from .. import models, schemas
from ..hashing import Hash
from ..nlp_ai import core as ai
from ..nlp_ai import xmlBuilder as xmlTools

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
    except:
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
    except:
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
    except:
        return "AN ERROR OCCUR"

def stanzaPipeline(request: schemas.UMLText):
    try:
        #get plain text
        text = request.text

        # syntaxic analysis
        doc = ai.plainTextParser(text)

        #result
        return ai.text_parser(doc)
    except:
        return "AN ERROR OCCUR"
