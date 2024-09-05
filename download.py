import threading
import os
import requests
import json
import time
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
        path=r'D:\Anime'+'\\'
        #print(url)
        header={
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
        }
        #print("Ballz")
        try:
                r=requests.get(url,headers=header,stream=True)
                #print(r)
        except Exception as e:
                retry=True
                print(e)
                if retry==True:
                        count=0
                        while retry==True and count<=10:
                                count+=1
                                try:
                                        r=requests.get(url,headers=header,stream=True)
                                        retry=True
                                except Exception as e:
                                        print(e)
        #print(r.text)
        print(r)
        if r.status_code!=200:
                return 0
        #print(r.headers)
        filesize=int(r.headers['Content-Length'])
        if name:
            filename=name
        else:
                filename=r.headers['Content-Disposition'].split('filename=')[1]
        filepath=path+filename
        down=True
        now_size=0
        if down==True:
                if os.path.isfile(filepath):
                        header['Range']='bytes=%s- '%(os.path.getsize(filepath))
                        r=requests.get(url,headers=header,stream=True)
                       # print(r)
                        print("File exists")
                        with open(path+filename,'ab') as f:
                                        print('Appending')
                                        now_size=os.path.getsize(path+filename)
                                        t1=time.perf_counter()
                                        for chunk in r.iter_content(chunk_size=1024*512):
                                                t2=time.perf_counter()
                                                f.write(chunk)
                                                if t2-t1>=1:
                                                        print(" "*100,'\r',f"{filename}:","%3.1f%s"%(os.path.getsize(filepath)*100/(filesize),"%"),f'  {c((os.path.getsize(path+filename)-now_size)/(t2-t1))}/s',f'   {c_time(((filesize)-os.path.getsize(path+filename))/((os.path.getsize(path+filename)-now_size)/(t2-t1)))}s','\r',end="")
                                                        now_size=os.path.getsize(path+filename)
                                                        t1=time.perf_counter()
                else:
                                with open(path+filename,'wb') as f:
                                        now_size=os.path.getsize(path+filename)
                                        t1=time.perf_counter()
                                        for chunk in r.iter_content(chunk_size=1024*512):       
                                                t2=time.perf_counter()
                                                f.write(chunk)
                                                if t2-t1>=1:
                                                        print(" "*100,'\r',f"{filename}:","%3.1f%s"%(os.path.getsize(filepath)*100/(filesize),"%"),f'  {c((os.path.getsize(path+filename)-now_size)/(t2-t1))}/s',f'   {c_time(((filesize)-os.path.getsize(path+filename))/((os.path.getsize(path+filename)-now_size)/(t2-t1)))}s','\r',end="")
                                                        now_size=os.path.getsize(path+filename)
                                                        t1=time.perf_counter()
                                                
                print('\n')
        return filesize/(1024*1024)
if __name__=="__main__":
        sum=0
        t1=time.perf_counter()
        path=r"C:\Users\davem\Documents\Code\links.json"
        with open(path,'r') as f:
                links=json.load(f)
                #links=links[:]
        print(links,end='\n\n\n\n\n')
        for link in links:
                print(f"({links.index(link)+1}/{len(links)})")
                if type(link)==list:
                        #threading.Thread(target=download,args=(link[1],link[0])).start()
                        sum+=download(link[1],link[0])
                else:
                        #*/threading.Thread(target=download).start()
                        sum+=download(link)
        print(sum)
        t2=time.perf_counter()
        #print(t2-t1)
