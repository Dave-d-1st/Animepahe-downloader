import os
import json
from pprint import pprint
import re
def sorter():
    path=r"Animes/"
    files=[n for n in os.listdir(path) if os.path.isfile(path+n) and n.startswith("AnimePahe")]
    pattern=re.compile(r'AnimePahe_(.+)_-_(\d*(?:\.\d+)?)_(\d+)p_')
    pattern2=re.compile(r'AnimePahe_(.+)_-_(\d*(?:\.\d+)?)_BD_(\d+)p_')
    for file in files:
        try:
            if "BD" in file.split("_-_")[-1]:
                search=pattern2.search(file)
                name=search.group(1)
                if os.path.isdir(path+name):
                    os.rename(path+file,path+name+"\\"+file)
                else:
                    os.mkdir(path+name)
                    os.rename(path+file,path+name+"\\"+file)
            else:
                search=pattern.search(file)
                name=search.group(1)
                print(name)
                if os.path.isdir(path+name):
                    print(path,name)
                    os.rename(path+file,path+name+"\\"+file)
                else:
                    os.mkdir(path+name)
                    os.rename(path+file,path+name+"\\"+file)
        except Exception as e:
            print("**"+file)
            print(e)

if __name__=="__main__":
    sorter()