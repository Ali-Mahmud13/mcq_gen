import os
import json 
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback

load_dotenv() # Load environment variables from .env file

key= os.getenv("OPENAI_API_KEY") # Get OpenAI API key from environment variables

llm=ChatOpenAI(api_key=key, temperature=0.7, model_name="gpt-3.5-turbo")

TEMPLATE= """text: {text}
You are an expert MCQ generator. Given the above text, it is your job to create a quiz of {number} multiple \
choice questions for {subject} students in a {tone} tone.

Make sure the questions are not repeated and that all questions are factually based on the input text.

Respond strictly in JSON format as shown below — no extra explanations, headings, or markdown.

### FORMAT EXAMPLE:
{{
  "1": {{
    "mcq": "What is the capital of France?",
    "options": {{
      "a": "Berlin",
      "b": "Madrid",
      "c": "Paris",
      "d": "Rome"
    }},
    "correct": "c"
  }},
  ...
}}
"""


quiz_generation_prompt = PromptTemplate(
    input_variables=['text','number','subject','tone'],
    template= TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt= quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2="""You are an expert english grammarian and writer. Given a Multiple choice quiz for {subject} students. \
     You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use around 50 words for complexity \
     if the quiz is not at per the cognitive and analytical abilties of the students,\
     update the quiz questions, which need to be changed and change the tone such that it perfectly fits the student's abilties.
     Quiz MCQs:
     {quiz}

     Check from an expert english writer of the above quiz:
          """
quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],    
    verbose=True)
