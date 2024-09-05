import sys
import os
import time
import json
import logging.config
import requests
from kwik_extractor import token_extractor
import re
from bs4 import BeautifulSoup
import bs4
import time
my_repo_folder=os.path.dirname(__file__)

class PD:
    def __init__(self,anime,first: int = 6,end: int = 6,should_append: bool = False   ,auto=False) -> None:  
        #Initiating a logger
        self.first=first
        self.end=end
        self.should_append=should_append
        with open(rf"{my_repo_folder}\logs\log_config.json",'r') as f:
            logger_config: dict = json.load(f)
        logger_config["handlers"]["filehand"]["filename"]= my_repo_folder+"\\logs\\"+logger_config["handlers"]["filehand"]["filename"]
        logging.config.dictConfig(config=logger_config)
        self.logger: logging.Logger = logging.getLogger("root")

        self.headers: dict[str:str] = {"Cookie":"__ddgid_=sE1YjW2vvFeZ9eMN; __ddgmark_=lxBaq42Dv71DNn34; __ddg2_=u2F6XKyQ9gVjlihp; __ddg1_=qbup7B4r1G6i5TWkt7RT;SERVERID=janna;XSRF-TOKEN=eyJpdiI6IjMwejVVQWpqYzBCZ0Z1YmhsZnZXM3c9PSIsInZhbHVlIjoiQ25Mdno0cUJyUTc0cU1rUW1NWVB0RXo5R1BkZFhBM1hRd1VObmYxSTRKTUNKZTZHdmF3VWdJbyswcWZMdmM1SUtONmlDc293VGRvbER4MFd3eDNGVEZpZC92L05QNVpjSmxGTEhzMlA3UGh0Wk5wSXVqK01KRXZCc2lWRkVZQXIiLCJtYWMiOiJlZjQxZjJlNzFkNWFlOTc2YjgwOTY5OTQyY2VhMDg2OTg3YTQyNDBjMTdlY2ZiMzllMjE0ZmE0YzI4ZTFiMzg1IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6Im5STkE5Q040dm1pVFFxQzdOR2d2RXc9PSIsInZhbHVlIjoiVTVaQmEvVEd0MVBBVVJ4bjMrVS94RXYzbTAwMnpFelhkVXYxTWFRSFJXSFVPZ2dzNkEyRXlXNW9neXdPeTlUQ0pISzZ2T0c0TUxiOVRnaW14N21OQTBkMW1JbWdEK0FvdFptTWxKQmcrc2pDbWRQMk9kbDkvMnZYSmVuVGhMQnciLCJtYWMiOiI5Yzc5ZmMzNjVlNDAzZDc4MTEzN2VjNjMzNTliZjExY2EyYzQyYzMyMjNiNWIzYTlhODEwMzEyMzk4MzQxODkzIiwidGFnIjoiIn0%3D","Referer":"https://animepahe.ru/anime/type/tv"}
        self.resolution: str = "1080p"
        search_url: str = "https://animepahe.ru/api?m=search&q="+anime
        self.logger.info("Sending GET")
        self.logger.debug(f"Search Term is {anime}")

        try:
            r:requests.Response = requests.get(search_url,headers=self.headers)
            self.logger.debug(f"Response is {r}")
        except requests.ConnectionError:
            self.logger.critical("No Network")
            exit()
        else:
            if r.status_code<=400:
                self.logger.info("Connection Established")
                search_json: dict[any,str] = r.json()
                self.search_results: list[dict[str:str]] = [{n['title']:[n['session'],n['episodes']]} for n in search_json['data']]
                if auto==False:
                    for x in self.search_results:
                        print("%i) %s(%i episodes)"%(self.search_results.index(x),list(x.keys())[0],list(x.values())[0][1]))
                    count: int = 0
                    while True:
                        ins: str = input("Pick anime: ")
                        try:
                            ins =int(ins)
                        except ValueError:
                            pass
                        if isinstance(ins,int) and ins>=0 and ins<=len(self.search_results):
                            break
                        if ins=="end":
                            exit()
                        elif count>=10:
                            self.logger.critical("Too many incorrect Trials")
                            break
                        else:
                            self.logger.warning(f"Enter a valid number(You have {10-count} more trials)")
                        count+=1
                    if count<=10:
                        self.search_result: dict[str:str] = self.search_results[ins]
                        self.logger.debug(f"Search Results: {self.search_result}")
                    else:
                        exit()
                elif auto==True:
                    self.search_result: dict[str:str] = self.search_results[0]
                    self.logger.debug(f"Search Results: {self.search_result}")
            else:
                self.logger.critical("Connection Failed")
                exit()
            

    def searching(self,last)->tuple[str,list[dict]]:
        t1: float = time.perf_counter()
        anime_id: str = self.search_result[list(self.search_result.keys())[0]][0]
        self.logger.debug(f"Anime Id is {anime_id}")

        url: str = "https://animepahe.ru/api?m=release&id=%s&sort=episode_asc&page="%(anime_id)
        header: dict[str:str] = {
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
        }
        self.logger.info("Getting Episode Id List...")
        try:
            r: requests.Response = requests.get(url+'1',headers=self.headers)
            self.logger.debug(f"Response is {r}")
        except requests.ConnectionError:
            self.logger.critical("No Network")
            self.search_result=None
        else:
            if r.status_code<=400:
                self.logger.info("Connection Established")
                sum: float = r.elapsed.total_seconds()
                episodes_json: dict[str:any] =r.json()
                episdoes_dict: list[dict]=[]
                episdoes_dict+=episodes_json['data']    
                with open(os.getcwd()+'/ '.strip()+'episodes1.json','w') as f:
                        json.dump(episdoes_dict,f,indent=2)
                        self.logger.debug("Updated episodes1.json")
                br=False
                while episodes_json['next_page_url']!=None:
                    for x in episdoes_dict:
                        #print(x['episode2'],x['episode'])
                        if x['episode2']>=last or x['episode']>=last:
                            br: bool = True
                            break
                        if br==True:
                            break
                        url: str = "https://animepahe.ru/api?m=release&id=%s&sort=episode_asc&page="%(anime_id)
                        page_num: str = episodes_json["next_page_url"].split("page=")[1]
                        #print(x['episode2'],x['episode'])
                        if x['episode2']>=last or x['episode']>=last:
                            br: bool = True
                            break
                    if br==True: 
                        break
                    url: str = "https://animepahe.ru/api?m=release&id=%s&sort=episode_asc&page="%(anime_id)
                    page_num: str = episodes_json["next_page_url"].split("page=")[1]
                    r: requests.Response = requests.get(url+page_num,headers=self.headers)
                    self.logger.debug(f"Getting page {page_num}")
                    self.logger.debug(f"Response is {r}")
                    sum+=r.elapsed.total_seconds()
                    episodes_json: dict[str:any]=r.json()
                    episdoes_dict+=episodes_json['data']
                    with open(os.getcwd()+'/ '.strip()+'episodes1.json','w') as f:
                        json.dump(episdoes_dict,f,indent=2)
                        self.logger.debug("Updated episodes1.json")
                t2: float = time.perf_counter()
                self.logger.debug(f"Time to make requests is %s seconds",sum)
                self.logger.debug(f"Time to get all episodes id is %s seconds",t2-t1)
                self.logger.info("Retrieved Episode Id List")
                return anime_id,episdoes_dict
                #episodes=episodes_json['data']
                #episode_ids=[n['session'] for n in ]
            else:
                self.logger.critical("Connection Failed")
                exit()
        
    def get_kwix(self,anime,episode):
        url: str = "https://animepahe.ru/play/%s/%s"%(anime,episode)
        self.logger.info("Getting Download links...")
        try:
            r: requests.Response = requests.get(url,headers=self.headers)
            self.logger.info(f"Response is {r.status_code}")
            if r.status_code<=400:
                soup: BeautifulSoup = BeautifulSoup(r.content,'lxml')
                dropdown: bs4.Tag|None=soup.find('div',id='pickDownload')
                links_soup: bs4.element.ResultSet = dropdown.find_all('a')
                link_soup=None

                for x in links_soup:
                    if self.resolution in x.text and "eng" not in x.text:
                        link_soup: bs4.Tag = x
                    else:
                        pass
                else:
                    if link_soup==None:
                        self.logger.info("No resolution")
                        link_soup: bs4.Tag = links_soup[-1]
                link: str = link_soup['href']
                retry=None
                headersp: dict[str:str] = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
                }
                self.logger.debug("Getting Kwix info...")
                try:
                    r: requests.Response=requests.get(link,headers=headersp)      
                    
                except:
                    retry=True
                    count=0
                    self.logger.debug("Failed to retrieve, Trying Again...")
                while retry ==True and count<=10:
                    try:
                        r: requests.Response=requests.get(link,headers=headersp)
                        retry: bool = False
                    except:
                        pass
                    count+=1
                    self.logger.debug(f"Attempt No. {count}")
                self.logger.debug(f"Response is {r}")

                soup=BeautifulSoup(r.content,'lxml')
                #print(soup.prettify())
                url=soup.find("script")
                patt=re.compile(r'https://kwik.(\w+)/f/(.+)"\).html')
                sec=patt.search(url.text).group(1)
                id=patt.search(url.text).group(2)
                #print(url)
                #print(sec)
                #print(id)
                url=f'https://kwik.{sec}/f/'+id
                r=requests.get(url,headers=headersp)
                token=''
                def set_token(response_text):
                        nonlocal token
                        data = re.search("[\S]+\",[\d]+,\"[\S]+\",[\d]+,[\d]+,[\d]+", response_text).group(0)
                        parameters = data.split(",")
                        para1 = parameters[0].strip("\"").split('))}("')[1]
                        para2 = int(parameters[1])
                        para3 = parameters[2].strip("\"")
                        para4 = int(parameters[3])
                        para5 = int(parameters[4])
                        para6 = int(parameters[5])
                        
                        page_data = token_extractor(para1, para2, para3, para4, para5, para6)
                        
                        
                        page_data = BeautifulSoup(page_data, "html.parser")

                        input_field = page_data.find("input", attrs={"name": "_token"})

                        #print(input_field)

                        if input_field is not None:
                            token = input_field["value"]
                            # print(self.token)
                            #print(token)
                            return True

                        return False

                cookie=[]
                try:
                    cookie.append(r.headers['set-cookie'])
                    cookie.append(r)
                except Exception as ex:
                    self.logger.error("ERROR",ex)
                #print(r)
                t1=time.perf_counter()
                set_token(cookie[1].text)
                t2=time.perf_counter()
                self.logger.debug(f"Time taken to get token is {t2-t1}")
                head = {
                            "origin": f"https://kwik.{sec}",
                            "referer": url,
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
                            "cookie": cookie[0]
                        }

                payload = {
                            "_token":token
                        }

                post_url = f"https://kwik.{sec}/d/" + id

                # print(head)
                # print(payload)
                # print(post_url)

                resp_headers = requests.post(post_url, data=payload, headers=head, allow_redirects=False)
                #print(resp_headers)
                # print(resp_headers)
                try:
                    download_url = resp_headers.headers["location"]
                    self.logger.debug(f"The Download url is {download_url}")
                    return download_url
                except:
                    self.logger.info("Stupid Nigga")
        except requests.ConnectionError:
            self.logger.critical("No Network")
            exit()
    
    def download(self): 
        if self.first:   
            first: int|float = self.first
        else:     
            first: int|float = -float('inf')

        if self.end:
            last: int|float = self.end
        else:
            last: int|float = float('inf')
        self.logger.info(f"Getting episodes between {first} and {last} episodes for {list(self.search_result.keys())[0]}")

        self.logger.debug(f"Appending to file is {self.should_append}")
        if self.should_append:
        	with open(my_repo_folder+"/links.json","r") as f:
                    links: list = json.load(f)
                    self.logger.debug("Reading links.json")
        else:
            links: list = []
        if isinstance(self.search_result,dict):
            episodes_search: tuple[str,list[dict]]=self.searching(last)
            e_range: list[dict] = [n for n in episodes_search[1] if first<=int(n['episode'])<=last]
            t1: float = time.perf_counter()
            for x in e_range:
                links.append(self.get_kwix(episodes_search[0],x['session']))
                with open(my_repo_folder+"/links.json","w") as f:
                    json.dump(links,f,indent=2)
                    self.logger.debug("Updated links.json")
            t2=time.perf_counter() 
            self.logger.debug(f"It took {t2-t1} to get the download links")
            self.logger.debug(links)
if __name__=="__main__":
    t1=time.perf_counter()
    if len(sys.argv) >=2:
        print(sys.argv[1])
        pahe=PD(sys.argv[1])
    else:
        pahe=PD("Elusive samurai",first=5)

    i=pahe.download()
    t2=time.perf_counter()
    pahe.logger.info("It took %dseconds"%(t2-t1))
    pahe.logger.info("Done")
