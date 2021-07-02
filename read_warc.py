import warc3_wet_clueweb09 as warc
import re
from datetime import datetime

# Tools to read and process .warc files
# Can Output as raw text
# Can Remove HTML and control characters
# Cannot remove JS

global warc_file_name
global write_file_name
write_file_name = "warc_text.txt"
warc_file_name = "00.warc.gz"


def cleanhtml(raw_html):
    cleanedhtml = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', raw_html)
    return cleanedhtml

def cleancontrol(cleaned_html):
    cleantext = re.sub(r"\\n|\\r|\\t", " ", cleaned_html)
    cleantext = re.sub(r'\s+', ' ',   cleantext)
    return cleantext


def cleanwarc(warcfile):
    w = open(write_file_name, "w+")
    w.truncate(0)
    
    with warc.open(warcfile) as f:
        print("Cleaning Files")
        for i, record in enumerate(f):
            text = record.__str__()
            
            if i != 0:
                text_len = len(text) - 1
                split1 = text.index("Length")
                split2 = text.index("Length", split1 + 1, text_len)
                split3 = text.index(" ", split2 + 8, text_len)
                split4 = text.find(">", split3 + 1, text_len)
                if split4 != -1:
                    text = text[split4 + 1:]
                else:
                    text = text[split3 + 1:]
                #print(text, split)
            
            cleaned_text = cleancontrol(cleanhtml(text))
            w.write(cleaned_text + "\n")

    w.close()
    print("Done cleaning")


def get_warc_raw(warcfile):
    print("Writing File")
    w = open(write_file_name, "a+")
    w.truncate(0)
    with warc.open(warcfile) as f:
        for record in f:
            w.write(record.__str__() + "\n")
    print("Done")


def main():
    start_time = datetime.now()
    
    #1. Clean warc
    cleanwarc(warc_file_name)
    #2. Get raw warc data
    #get_warc_raw(warc_file_name)
    
    print("Done with Program", datetime.now() - start_time)

if __name__ == "__main__":
    main()
