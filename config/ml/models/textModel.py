from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os

def getClassification(text):
    if type(text)!=str: return None
    classification = pipeline("text-classification", "SamLowe/roberta-base-go_emotions")
    result = classification(text)
    print("result : ", result)
    return result

def getGeneratedText(input_text):
    if type(input_text)!=str: return None
    access_token = os.environ.get("GEMMA_ACCESS_TOKEN")
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b", token=access_token)
    model = AutoModelForCausalLM.from_pretrained("google/gemma-7b", device_map="auto", token=access_token)
    input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
    outputs = model.generate(**input_ids)
    return (tokenizer.decode(outputs[0]))
