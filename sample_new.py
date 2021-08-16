# Generate 500k sample file to do clustering from CW09 dataset
# 1492 files 
# 500k/1492 = 335 samples from each document
from random import sample
import random
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from glob import glob
import numpy  as np

now = datetime.now()

path = "/scratch/jq741/work/data/cw09en1/"
folders = ("en0000", "en0001", "en0002", "en0003", "en0004", 
            "en0005", "en0006", "en0007", "en0008", "en0009",
            "en0010", "en0011", "enwp00", "enwp01", "enwp02",
            "enwp03")

folderpaths = []

for folder in folders:
    folderpaths.append(path + folder)

SAMPLE_NUM = 355

samples = []
titles = []
stop = 0
for folderpath in folderpaths:
    print(folderpath)

    for filename in glob(folderpath + "/*.warc.gz.txt"):

        if stop >= 500000:
            break
        stop += 1
        print(stop)
        print(filename)
        doc_array = []
        title_temp = []

        cwfile = open(filename.strip(), "r")

        # Get all docs from cwfile
        for doc in cwfile:
            if len(doc) != 0:
                sep = doc.find("\\n")
                doc_array.append(doc[sep + 1:])
                title_temp.append(doc[0:sep])
                
        # Sample 355
        if len(doc_array) > 0:
            old_state = random.getstate()
            samp = sample(doc_array, SAMPLE_NUM)

            random.setstate(old_state)
            title_samp = sample(title_temp, SAMPLE_NUM)

            samples.extend(samp)
            titles.extend(title_samp)

# Vectorize all docs from 1 file
# Reduces storage needed
# vectorizer = TfidfVectorizer(stop_words={'english'})
# vect_samples = vectorizer.fit_transform(samples)


# print(vect_samples.shape[0]/355)

cwfile.close()

# Pickle samples
# with open(path + "samples_out_vect.pkl", "wb+") as f:
#     pickle.dump(vect_samples, f)

with open(path + "sampletitles_out.txt", "w+") as k:
    for title in titles:
        k.write(title + "\n")

print("Done in:", datetime.now() - now)
#---
path = "/scratch/jq741/work/data/cw09en1/"
#path = "./"
NUM_OF_LINES = 355

now = datetime.now()

f = open(path + "sampletitles_out.txt", "r")
expansion_list = []


# Iterate through all files
# Store 355 samples in a list since it is ordered
for line in f:
    fold_file_line = line.strip().split("_")
    folder = fold_file_line[0]
    lines = [fold_file_line[2]]
    filename = fold_file_line[1]
    filename_split = filename.split(".")

    if int(filename_split[0]) < 10:
        filename_split[0] = str(int(filename_split[0]))
        filename = ".".join(filename_split)

    file_path = path + folder + "/" + filename + ".txt" 
    print(file_path)

    # Load all relevant docs from a warc file
    for i in range(354):
        line_num = f.readline().strip().split("_")[-1]
        lines.append(line_num) 
    #print(len(lines))
    
    # Get list of all sample expansion terms from a warc file
    term_f = open(file_path, "r")
    line_ind_count = 0

    for j, expansion_line in enumerate(term_f):
        if j == lines[line_ind_count]: 
            expansion_list.append(expansion_line.strip())
            line_ind_count += 1

f.close()
term_f.close()

for i in range(len(samples)):
    samples[i] = samples[i] + " " + expansion_list[i]

# Vectorize terms
vectorizer = TfidfVectorizer(stop_words={'english'})
vect_samples = vectorizer.fit_transform(expansion_list)
print(vect_samples.shape[0]/355)

# Pickle samples
with open(path + "samples_expans_out_vect.pkl", "wb+") as k:
    pickle.dump(vect_samples, k)

print("Done in:", datetime.now() - now)

