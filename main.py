import json

import langchain
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
import os
import requests
import flask
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/questions", methods=["POST"])
def create_questions():
    easy_question = request.form.get("easy_question")
    hard_question = request.form.get("hard_question")
    question_type = request.form.get("type")
    subject = request.form.get("subject")
    format = ""
    temp = ""
    print(request.get_data())
    try:
        req = request.get_data()
        json_object = json.loads(req)
        if easy_question == None:
            easy_question = json_object["easy_question"]
        if hard_question == None:
            hard_question = json_object["hard_question"]
        if question_type == None:
            question_type = json_object["type"]
        if subject == None:
            subject = json_object["subject"]
    except:
        z = 1
    if question_type == "mcq":
        format = "\n ----\n Question: generated question\n ----\n Choices: 1) choice_1 2) choice_2 3)choice_3 4) choice_4\n ----\n."
    elif question_type == "fitb":
        format = "\n ----\n Rule: Generated questions must start with 'what is'. You should not return the answer."
        temp = "Given an easy question and a hard question, generate a set of '{subject}' questions whose difficulties are from easy to hard on the same topics. Return questions while following this rule:'{format}'\nEasy question:'{easy_question}'\nHard question: '{hard_question}'"
    else:
        format = "\n---\n Statement: generated statement. True/False? \n ----\n"
        temp = "Given an easy question and a hard question, generate a set of true/false '{subject}' statements whose difficulties are from easy to hard on the same topics. Return the statements in this format:'{format}'\nEasy question:'{easy_question}'\nHard question: '{hard_question}'"
    llm = OpenAI(temperature=0.9, api_key = "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")
    prompt = PromptTemplate(
        input_variables=["easy_question","hard_question", "format", "subject"],
        template="Given an easy question and a hard question, generate a set of '{subject}' questions whose difficulties are on the same scale. Return the questions in this format:'{format}'\nEasy question:'{easy_question}'\nHard question: '{hard_question}'",
    )
    if question_type != "mcq":
        prompt.template = temp

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(easy_question=easy_question, hard_question=hard_question, format=format, subject=subject)
    print(response)
# Run the chain only specifying the input variable.
    response = jsonify({
            "response": response,
        })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)