#Determine cluster for each warc file
#Output list as pickle file

import pickle 
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse

def divide_chunks(l, n):  
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

path = "/scratch/jq741/work/data/cw09en1/"
folder = "en0011/"
parser = argparse.ArgumentParser(description="Docs")
parser.add_argument("WARC_File")
args = parser.parse_args()

f = open(path + folder + args.WARC_File, "r")

with open(path + "cluster_model.pkl", "rb")  as r:
    model = pickle.load(r)

doc_list = []
doc_title_list = []

for stop, line in enumerate(f):
    # if stop >= 10000:
    #     break
    sep = line.find("\\n")
    doc_txt = line[sep + 1:]
    doc_title = line[0:sep]     
    doc_list.append(doc_txt)
    doc_title_list.append(doc_title)

vectorizer = TfidfVectorizer(stop_words={'english'})

doc_list = list(divide_chunks(doc_list, 10000))

final = []
extra = 0
for chunk in doc_list:
    
    if len(chunk) < 100:
        for i in range(100 - len(chunk)):
            extra += 1
            chunk.append("empty")            
            
    vect_samples = vectorizer.fit_transform(chunk)

    file_prediction = model.fit_predict(vect_samples)
    
    for i in range(extra):
        file_prediction.pop()

    for cluster in file_prediction:
        final.append(cluster)

final_final = []
doc_list = []
model = ""

for i in range(len(doc_title_list)):
    final_final.append((final[i], doc_title_list[i]))

with open(path + folder + args.WARC_File + ".pkl", "wb+") as w:
    pickle.dump(final_final, w, protocol=-1)
