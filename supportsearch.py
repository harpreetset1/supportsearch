'''
Created on Jul 24, 2017

@author: harpreetsethi
'''
from flask import Flask, request
import ProcessQnA

app = Flask(__name__)

@app.route("/search", methods=['POST'])
def search():
    #print(request.get_json())
    doc=request.get_json()['query'] #'CCH Axcess Workstream due date?'
    return ProcessQnA.search_concepts(doc)