import torch
import os,glob
import time
from transformers import T5Tokenizer, T5ForConditionalGeneration
from datetime import datetime
import io
import argparse

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(torch.cuda.is_available())
tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
model = T5ForConditionalGeneration.from_pretrained('castorini/doc2query-t5-base-msmarco')
model.to(device)



def transform(doc_text, return_num=3):
    input_ids = tokenizer.encode(doc_text, return_tensors='pt', truncation=True, max_length=512).to(device)
    outputs = model.generate(
        input_ids=input_ids,
        max_length=64,
        do_sample=True,
        top_k=10,
        num_return_sequences=return_num)
    return outputs


def main():
       
    parser = argparse.ArgumentParser(description='Cleaned file paths')
    parser.add_argument('filename')
    args = parser.parse_args()
    file_list = io.open(args.filename, "r", encoding="utf-8")
    filename = args.filename

    with open(filename,'r') as f:
        print(str(filename))
        f = open(filename,"r")
        start_time = datetime.now()
        file_contents = f.read()
        contents_split = file_contents.splitlines() 


        print("Transforming Text")
        x = 0
     
        exp_doc = ""
        terms = ""
        for txt in contents_split:
           start = time.time()
           title = txt.split(r"\n")
           terms = title[0] 
           outputs = transform(txt, 10)
           x += 1
           for i, line in enumerate(outputs):
              string = str(tokenizer.decode(outputs[i], skip_special_tokens=True))
              terms = terms + ":!@#$%^" + string 
           if (x %100 == 0):
              end = time.time()
              print(x,": ",end - start)
           exp_doc = exp_doc + terms + "\n"      

        text_file = open(str(filename) + '_transformer_expansion.txt', "w")
        text_file.write(exp_doc)
        text_file.close()

        print("Done with Program", datetime.now() - start_time)
    
main()
