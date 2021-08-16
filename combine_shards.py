from glob import glob
import pickle

path = "/scratch/jq741/work/data/cw09en1/"
folders = ("en0000", "en0001", "en0002", "en0003", "en0004", 
            "en0005", "en0006", "en0007", "en0008", "en0009",
            "en0010", "en0011", "enwp00", "enwp01", "enwp02",
            "enwp03")
            
folderpaths = []

for folder in folders:
    folderpaths.append(path + folder)

count = 0

files_out = {}

for i in range(100):
    files_out[i] = open(path + "shards/" + "CW09_expanded." + str(i).zfill(3), "w+")

for folderpath in folderpaths:
    for filename in glob(folderpath + "/*.pkl"):
        with open(filename.strip(), "rb") as f:
            info_lst = pickle.load(f)
        print(filename) 
       
        for tup in info_lst:
            #print(tup)
            files_out[int(tup[0])].write(tup[1].strip() + "\n")


