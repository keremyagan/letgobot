import requests 
from bs4 import BeautifulSoup 
from basic import Basic 

class AmazonData :
    
    def __init__(self,category_name,page,default_size ='US40') :
        self.category_name = category_name
        self.page = page
        self.default_size = default_size
        self.header = {'User-Agent': 'keremyagan'}
        self.main_url = 'https://www.amazon.com.tr/'
      
    def get_links_from_category(self) : 
        links = set()
        self.category_name = self.category_name.replace(' ','+')
        correct_url_1 = f'{self.main_url}s?k={self.category_name}&__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_1'
        correct_url_2 = f'{self.main_url}s?k={self.category_name}&page={str(self.page)}&__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1632343304&ref=sr_pg_{str(self.page)}'
        for page in range(1,self.page+1) :
            try:   
                url = correct_url_2
                if page == 1 :
                    url = correct_url_1

                response = requests.get(url, headers = self.header ).content
                soup = BeautifulSoup(response,'html.parser')
                find_in = ['__mk_tr_TR=']
                find_out = ['/s?k=','#customerReviews']
                for a in soup.find_all('a', href=True)  :
                    link = a['href']
                    if all([substring in link for substring in find_in]) and not any([substring in link for substring in find_out])   :
                        links.add(self.main_url+link)

            except :
                pass
        
        return links

    def get_product_detail(self,url) : 
        try:
            response = requests.get(url , headers = self.header).content
            soup = BeautifulSoup(response , 'html.parser')
            
            brand = soup.find('a',{'id':'bylineInfo'}).text.rstrip().lstrip().split()[1]
            title = soup.find('span',{'id':'productTitle'}).text.rstrip().lstrip()
            try:
                last_price = soup.find('span',{'id':'priceblock_ourprice'}).text.rstrip().lstrip()
                old_price = last_price
            except:
                last_price = soup.find('span',{'id':'priceblock_pospromoprice'}).text.rstrip().lstrip()
                old_price = soup.find('span',{'class':'priceBlockStrikePriceString a-text-strike'}).text.rstrip().lstrip()
            links = set()
            find_in = ['https://m.media-amazon.com/images/','AC_US40','.jpg']
            for img in soup.findAll('img'):    
                image = img.get('src')
                if all([substring in str(image) for substring in find_in]) :
                    #SY450 , US40 , SX679  etc.
                    image = str(image).replace('US40',self.default_size)
                    links.add(image)

            last_price = last_price.replace(u'\xa0','')
            old_price = old_price.replace(u'\xa0','')
            return {
                    "link"       : url,
                    "brand"  : brand ,
                    "title"     : title,
                    "pics"      : links,
                    "reel_price"     : old_price,
                    "last_price"  : last_price ,          
                }  
        except  :
            pass

      
class Amazon :
        
    def __init__(self,category_amazon = 'cep telefonlari' , page = 2 ,  category_letgo='elektronik' , price_type = 'last_price' ,
                 profit_rate = 10 , min_price = 100 , description = 'Default Description(AD)' , image_size = 'SY450' ) :
        self.category_amazon = category_amazon
        self.page = page 
        self.category_letgo = category_letgo 
        self.price_type = price_type 
        self.profit_rate = profit_rate
        self.min_price = min_price
        self.description = description
        self.image_size = image_size
        self.basic = Basic()
        
    def get_links(self) :
        get_link = AmazonData(self.category_amazon, self.page,self.image_size)
        links = get_link.get_links_from_category()
        return links 
           
    @property
    def run(self) :
        links = self.get_links() 
        for n,link in enumerate(links) :
            amazon_data = AmazonData(self.category_amazon, self.page,self.image_size)
            data = amazon_data.get_product_detail(link)
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
amazon = Amazon(min_price=5,
    description="Marka:{brand}\nBaşlık:{title}\nİlk Fiyat:{reel_price}\n\nSon Fiyat:{last_price}\n",price_type='reel_price')
amazon.run
"""
