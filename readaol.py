import json
import time

# Sorts AOL2M results

f = open("aol.run")
stop = 0
arr_check = []
data = {}
start = time.time()
en00_store = ""
en01_store = ""
en02_store = ""
en03_store = ""
en04_store = ""
en05_store = ""
en06_store = ""
en07_store = ""
en08_store = ""
en09_store = ""
en10_store = ""
en11_store = ""
enwp0_store = ""
enwp1_store = ""
enwp2_store = ""
enwp3_store = ""
en_arr = [en00_store,en01_store,en02_store,en03_store,en04_store,en05_store,en06_store,en07_store,en08_store,en09_store,en10_store,en11_store,enwp0_store,enwp1_store,enwp2_store,enwp3_store]
folderName_arr = ['en0000','en0001','en0002','en0003','en0004','en0005','en0006','en0007','en0008','en0009','en0010','en0011','enwp00','enwp01','enwp02','enwp03']
for result in f:
    stop += 1
    result_split = result.strip().split(" ")
    query_num = result_split[0]
    rest = result_split[1].split("-")
    folder_num = rest[1]
    file_num = rest[2]
    line_num = rest[3]
    filename = folder_num + "_" + file_num
    #create files if not exist 
    for i in range (0,len(folderName_arr)):
        if folder_num == folderName_arr[i]:
          txt = filename+":"+line_num+"?"+query_num+" "
          en_arr[i] = en_arr[i] + txt
         # print(txt)
    if stop % 100000 ==0:
        end = time.time()
        print(stop,": ",end - start)
        start = time.time()
        for num in range (0, len(en_arr)):
            path = folderName_arr[num] +  "_middle.txt"
            file = open(path, "a") 
            file.write(en_arr[num] + " ")
        #clean up array since limit memory
        for j in range(0,len(en_arr)):
            en_arr[j] = ""

    
   
