import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())
hf_token = os.environ.get('HUGGING_FACE_TOKEN')

torch.cuda.empty_cache()

model_hf = 'microsoft/Phi-3.5-mini-instruct'

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_compute_dtype=torch.bfloat16
)


model = AutoModelForCausalLM.from_pretrained(model_hf, quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained(model_hf)


pipe = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.1,
    max_new_tokens=100,
    do_sample=True,
    repetition_penalty=1.1
)

llm = HuggingFacePipeline(pipeline=pipe)


async def app_prompt():

    template_initial = """
        <|system|>
        You are a helpful medical assistant.
        {str}
        Give a friendly greeting, explain that you will need to ask some questions to determine the disease.
        <|end|>
        <|assistant|>
    """

    prompt_initial = PromptTemplate.from_template(template_initial)

    chain_initial = prompt_initial | llm

    template = """
        <|system|>
        You are a helpful virtual assistant. Your goal is to ask a question. 
        {context}.
        Ask one question for the people about the context, use few and simple words.
        <|end|>
        <|assistant|>
    """

    prompt = PromptTemplate.from_template(template)

    chain = prompt | llm

    return chain_initial, chain


async def result_disease(columns, responses, df):
        
        result_data = {k: v for k, v in zip(columns, responses)}


        filtered_df = df[
            (df['Fever'] == result_data['Fever']) &
            (df['Cough'] == result_data['Cough']) &
            (df['Fatigue'] == result_data['Fatigue']) &
            (df['Difficulty Breathing'] == result_data['Difficulty Breathing']) &
            (df['Age'] == int(result_data['Age'])) &
            (df['Gender'] == result_data['Gender']) &
            (df['Blood Pressure'] == result_data['Blood Pressure']) &
            (df['Cholesterol Level'] == result_data['Cholesterol Level'])
        ]

        disease = filtered_df['Disease'].values[0] if not filtered_df.empty else 'No match found'

        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500))


        result_wikipedia = wikipedia.invoke(disease)


        template_disease = """
            <|system|>
            You are a helpful virtual assistant. Your goal is explain the disease. 
            {context}.
            Explain in a gentle way what the patient's illness is based on the context, Use a maximum of five lines.
            <|end|>
            <|assistant|>
        """

        prompt_disease = PromptTemplate.from_template(template_disease)

        chain = prompt_disease | llm

        explain_disease = chain.invoke({'context': result_wikipedia})

        result_explain = explain_disease.split('\n')[8]

        return result_explain, disease


disease_data = None

async def set_disease(disease_value):
      global disease_data
      disease_data = disease_value

async def get_disease():
      return disease_data