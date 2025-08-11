import os
import requests
import json
import time
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeRemainingColumn, TransferSpeedColumn

import sorter
def c_time(s):
    seconds=int(s)%(24*3600*365)
    years=seconds//(365*3600*24)
    seconds=seconds%(365*3600*24)
    days=seconds//(3600*24)
    seconds=seconds%(3600*24)
    hours=seconds//(3600)
    seconds=seconds%(3600)
    minutes=seconds//60
    seconds=seconds%60
    time="%dyr %03dd %02dhr %02dmin %02ds"%(years,days,hours,minutes,seconds)
    for x,y in zip([years,days,hours,minutes,seconds],["yr","d","hr","min","s"]):
     if x==0:
          time=time.replace(str(x),"")
          time=time.replace(y,"")
    return time.strip()
def c(s):
    for x in ['bytes','KB','MB','GB','TB']:
        if s < 1024.0 and x!='GB':
                return "%3.1f %s"%(s,x)
        elif s < 1024.0 and x=='GB':
                return "%3.2f %s"%(s,x)
        s/=1024.0

def download(url:str,name=None,*headers:list):
    path=r'Animes/'
    header={
     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
    }
    #print("Ballz")
    try:
        r=requests.head(url,headers=header)
        #print(r)
    except Exception as e:
        retry=True
        print(e)
        if retry:
            count=0
            while retry and count<=10:
                count+=1
                try:
                    r=requests.head(url,headers=header)
                    retry=True
                except Exception as e:
                    print(e)
    print(r.status_code)
    if r.status_code!=200:
        return 0
    filesize=int(r.headers['Content-Length'])
    if name:
        filename=name
    else:
        filename=r.headers['Content-Disposition'].split('filename=')[1]
    filepath=path+filename
    down=True
    if down:
        if os.path.isfile(filepath):
            header['Range']='bytes=%s- '%(os.path.getsize(filepath))
            r=requests.get(url,headers=header,stream=True)
            print("File exists")
        else:
            r=requests.get(url,headers=header,stream=True)
        with Progress(SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            TransferSpeedColumn()) as progress:
            with open(path+filename,'ab') as f:
                task = progress.add_task(f"{filename}",total=filesize)
                t1=time.perf_counter()
                for chunk in r.iter_content(chunk_size=1024*512):
                    t2=time.perf_counter()
                    f.write(chunk)
                    if t2-t1>=1:
                        progress.update(task,  completed=os.path.getsize(filepath))
                        t1=time.perf_counter()
                        
        print('\n')
    return filesize
def download_links():
    sum=0
    path=r"links.json"
    with open(path,'r') as f:
        links=json.load(f)
    for link in links:
        print(f"({links.index(link)+1}/{len(links)})")
        if link is list:
            sum+=download(link[1],link[0].replace(":","-").replace("?","_"))
        else:
            sum+=download(link)
    print(f"The total download size is {c(sum)}")
    sorter.sorter()

if __name__=="__main__":
    download_links()
    #print(t2-t1)
 