import requests 
from bs4 import BeautifulSoup 
from basic import Basic 
from requests import Session
class N11Data :
    
    def __init__(self,category_name = 'telefon-ve-aksesuarlari' ,page = 2) :
        self.category_name = category_name
        self.page = page
        self.header = {'userAgent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
        self.main_url = 'https://www.n11.com/'
      
    def get_links_from_category(self) : 
        links = set()
        self.category_name = self.category_name.replace(' ','-')
        for page in range(1,self.page+1) :
            try:  
                url = self.main_url+self.category_name+'?pg='+str(page)
                response = requests.get(url , headers = self.header ).content
                soup = BeautifulSoup(response,'html.parser')
                find_in = ['__mk_tr_TR=']
                find_out = ['/s?k=','#customerReviews']
                for a in soup.find_all('a', href=True)  :
                    link = a['href']
                    if 'https://www.n11.com/urun/' in link :
                        links.add(link)

            except :
                pass
        
        return links

    def get_product_detail(self,url) : 
        try:        
            session = Session()    
            response = session.get(url , headers = self.header).content

            soup = BeautifulSoup(response , 'html.parser')
            title = soup.find('div',{'class':'nameHolder'}).text.rstrip().lstrip().split('\n')[0]
            last_price= 'None'
            brand = 'None'
            links = set()    
            for i in str(soup).splitlines() :
                if '"brand":' in i :
                    brand = i.split(':')[1].split('"')[1]
                    break

            for i in str(soup).splitlines() :
                if '"lowPrice":' in i :
                    last_price = i.split(':')[1].split('"')[1]
                    break

            find_in = ['https://n11scdn','.jpg','<li class="image-thumb"']
            find_in1 = ['https://n11scdn','.jpg','<li class="thumb active"']
            first_code = ''           
            for i in str(soup).splitlines() :
                true_link = 0
                if all([substring in i for substring in find_in]) :
                    true_link = 1                       
                elif all([substring in i for substring in find_in1]) :
                    true_link = 1  
                elif 'data-full=' in i :
                    true_link = 1       
                if true_link == 1 :
                    link = i.split('"')[3]
                    if first_code == '' :
                        links.add(link)
                        first_code = link.split('/')[4]
                    else :
                        if first_code == link.split('/')[4] :
                            links.add(link)                            

                               
            return {
                'brand' : brand ,
                'title' : title , 
                'reel_price' : last_price ,
                'pics' : links
            }

        except :
            pass

      
class N11 :
        
    def __init__(self,category_n11 = 'telefon-ve-aksesuarlari' , page = 2 ,  category_letgo='elektronik' , price_type = 'reel_price' ,
                 profit_rate = 10 , min_price = 100 , description = 'Default Description(AD)') :
        self.category_n11 = category_n11
        self.page = page 
        self.category_letgo = category_letgo 
        self.price_type = price_type 
        self.profit_rate = profit_rate
        self.min_price = min_price
        self.description = description
        self.basic = Basic()
        
    def get_links(self) :
        get_link = N11Data(self.category_n11, self.page)
        links = get_link.get_links_from_category()
        return links 
           
    @property
    def run(self) :
        links = self.get_links() 
        for n,link in enumerate(links) :
            n11_data = N11Data(self.category_n11, self.page)
            data = n11_data.get_product_detail(link)
            print(f'Scannig Url {n+1}/{len(links)} : {link} ')
            try:
                if len(data["pics"]) > 0 and float(data[self.price_type].split()[0].split(",")[0].replace('.','')) > self.min_price   :
                    print(f"This Link will be shared on Letgo:\nProduct Title : {data['title']}\nProduct Price : {data[self.price_type]}")
                    if len(data["pics"]) > 7 :
                        data["pics"] = list(data["pics"])[:7]
                    for pic_url in data["pics"]:
                        print('Getting Pics.')
                        self.basic.download_pic(pic_url)
                    self.basic.save_pic_to_file(data)
                    print('Connecting to Letgo.')
                    new_description = self.basic.set_description(self.description,data)
                    print(new_description)
                    profit_rate = 1 + (self.profit_rate/100)
                    price = int(float(data[self.price_type].replace(".","").split()[0].split(",")[0])*profit_rate)
                    if self.description == 'Default Description(AD)' :
                        new_description = data['description']
                    self.basic.connect_to_letgo(data,price,self.category_letgo,data["title"],new_description) 
                    self.basic.remove_pics(data)
                    print('Succesfull.')
            except  AttributeError :
                print('This Link Doesnt Support Selected Price Type.')
            except Exception as err:
                print(f'An Error Occurred. Error is : {err} ')
              
        
"""
n11 = N11(description="Marka:{brand}\nBaşlık:{title}\nSon Fiyat:{reel_price}\n",price_type='reel_price',
                    min_price=5)
n11.run
"""