import pickle5 as pickle
import os, glob
import argparse

path = "/scratch/jq741/work/data/cw09en1/"

parser = argparse.ArgumentParser(description="Docs")
parser.add_argument("f1")
parser.add_argument("f2")
args = parser.parse_args()


with open(path + "en_unranked/en0011_query_expansion.pkl", 'rb') as qf:
        data = pickle.load(qf)

with open(path + args.f2, "r") as f2:
    j = 0
    for rows in f2:
        j += 1
    
with open(path + args.f1) as f1, open(path + args.f2) as f2:
    output = ""
    for x in range (0,j): 
        #print(x)
        line_file1 = f1.readline()
        line_file2 = f2.readline()
        line_file1 = line_file1.strip('\n')
        line_file2 = line_file2.strip('\n')
        t_arr = line_file2.split(":!@#$%^")
        t_arr.pop(0) 

        #final string for trans_expansion
        trans_exp = "?".join(t_arr)

        line_file1 += ";;;TRANSEXP：" + trans_exp

        arr = line_file1.split(".warc.gz")
        number_str = str(x)
        zero_filled_number = number_str.zfill(5)
        queryId = arr[0]+":"+zero_filled_number

        if queryId in data:
            testArr = data[arr[0]+":"+zero_filled_number].split(",")
            if len(testArr) < 20:  
            #set threshold for queries
                query_exp = ";".join(testArr)       
                line_file1 += ";;;QUERYEXP: "+ query_exp
        
        output += line_file1 +"\n"
        print(x)

    with open(path + args.f1 + "_appended.txt", "w+") as f22:
        f22.write(output)
        f22.close()
