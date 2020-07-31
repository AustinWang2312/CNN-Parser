import requests as req
import re
import pandas as pd
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup


class WebParser():

    def __init__(self,url):
        self.page=req.get(url)
        self.soup=BeautifulSoup(self.page.content, 'html.parser')
        self.url=url

    def utc_to_est(self,datetime_str):
        datetime_obj=datetime.strptime(datetime_str,"%Y-%m-%d %H:%M:%S")
        datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
        datetime_obj_est=datetime_obj_utc.astimezone(timezone('US/Eastern'))
        datetime_obj_est=datetime_obj_est.replace(tzinfo=None)
        return datetime_obj_est


    def get_title(self):
        title=self.soup.find("title")
        return re.findall(">\n*\ *(.*)<",str(title))[0]

    def get_release_datetime(self):
        pass

    def get_body_text(self):
        pass

    def process_datetime(self,meta_data):
        date=re.findall("\"(.*)T",meta_data)[0]
        time=re.findall("T(.*)Z",meta_data)[0][:6]+"00"
        datetime_str=date+" "+time
        return datetime_str
        


class CNNParser(WebParser):

    def extract_months(self):
        home_url="https://www.cnn.com/article/sitemap-2019.html"
        page=req.get(home_url)
        soup=BeautifulSoup(page.content, 'html.parser')


    def extract_urls(self):
        home_url= "https://www.cnn.com/article/sitemap-2019-12.html"
        page=req.get(home_url)
        soup=BeautifulSoup(page.content, 'html.parser')
        links=soup.find_all(attrs={"data-analytics":"_list-hierarchical-xs_article_"})
        body=soup.find_all("body")[0]
        pg= body.find_all("div",class_="pg-no-rail pg-wrapper pg t-light")[0]
        sm_container=pg.find_all("div",class_="sitemap-entry")[1]
        hrefs=sm_container.find_all("a")
        url_list=[]
        for url in hrefs:
            url_list.append(url['href'])

        print(len(url_list))



    def get_release_datetime(self):
        meta_data=self.soup.find_all("meta",limit=7)
        datetime_str=self.process_datetime(str(meta_data[6]))
        return super().utc_to_est(datetime_str)

    def get_body_text(self):
        body_tags=self.soup.find_all(class_="l-container")
        return body_tags[0].get_text()
        

class ReutersParser(WebParser):
    def process_datetime(self,meta_data):
        date=re.findall("\"(.*)T",meta_data)[0]
        time=re.findall("T(.*)\+",meta_data)[0][:6]+"00"
        datetime_str=date+" "+time
        return datetime_str

    def get_release_datetime(self):
        meta_data=self.soup.find_all(attrs={"name":"sailthru.date"})
        datetime_str=self.process_datetime(str(meta_data[0]))     
        return super().utc_to_est(datetime_str)

    def get_body_text(self):
        body_tags=self.soup.find_all(class_="StandardArticleBody_body")
        return body_tags[0].get_text()
        
    
    


url="https://www.cnn.com/2020/07/29/politics/donald-trump-suburbs-housing/index.html"
#url="https://www.reuters.com/article/us-usa-tech-congress/u-s-lawmakers-accuse-big-tech-of-crushing-rivals-to-boost-profits-idUSKCN24U1FI"
#url2="https://www.reuters.com/article/us-science-stonehenge/scientists-solve-mystery-of-the-origin-of-stonehenge-megaliths-idUSKCN24U2VG"
x=CNNParser(url)
x.extract_urls()
#x=ReutersParser(url2)
#print(x.get_title())
#x.get_body_text()
#print(x.get_release_datetime())
