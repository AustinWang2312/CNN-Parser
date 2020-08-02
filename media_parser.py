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

    def extract_years(self):
        counter=2011
        years=[]
        while (counter<2021):
            years.append("https://www.cnn.com/article/sitemap-"+str(counter)+".html")
            counter+=1
        print (years)
        return years

    def extract_months(self,url):
        home_url=url
        page=req.get(home_url)
        soup=BeautifulSoup(page.content, 'html.parser')
        months=soup.find("section")
        month_href=months.find_all("a")
        month_urls=[]
        for url in month_href:
            month_urls.append("https://www.cnn.com"+url['href'])
        print (month_urls)
        return month_urls

    def extract_urls(self,url):
        home_url= url
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
        #print(url_list)
        return url_list

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
        
    
    

#url="https://www.cnn.com/2020/07/29/politics/donald-trump-suburbs-housing/index.html"
#url="https://www.reuters.com/article/us-usa-tech-congress/u-s-lawmakers-accuse-big-tech-of-crushing-rivals-to-boost-profits-idUSKCN24U1FI"
#url2="https://www.reuters.com/article/us-science-stonehenge/scientists-solve-mystery-of-the-origin-of-stonehenge-megaliths-idUSKCN24U2VG"
#x=CNNParser(url)
#x.extract_urls()
#x.extract_years()
#x.extract_months("https://www.cnn.com/article/sitemap-2011.html")
#x.extract_urls("https://www.cnn.com"+'/article/sitemap-2011-10.html')
#x=ReutersParser(url2)
#print(x.get_title())
#x.get_body_text()
#print(x.get_release_datetime())
