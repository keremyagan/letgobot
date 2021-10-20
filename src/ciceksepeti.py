import requests 
from bs4 import BeautifulSoup
from basic import Basic 

class CiceksepetiData :
    
    def __init__(self,category_name,page,image_size='L') :
        self.main_url = 'https://www.ciceksepeti.com/'
        self.category_name = category_name
        self.page = page
        self.image_size = image_size
    
    def check_category(self) :
        try:
            response = requests.get(self.main_url+self.category_name+'?page='+str(self.page)).status_code
        except:
            return None
        if response == 200 :
            return True
        else :
            return 'Link Doesnt Found.Please Check it. '

    def get_links_from_category(self) :
        links = []
        for page in range(1,self.page+1) :
            try:
                response = requests.get(self.main_url+self.category_name+'?page='+str(page)).content
                soup = BeautifulSoup(response,'html.parser')
                for a in soup.find_all('a', href=True):
                    if str(a['href'])[0] =='/'  :
                        try:
                            int(str(a['href'])[-1])   
                            links.append(self.main_url + a['href'])
                        except:
                            pass
            except :
                pass

        return links

    def get_product_detail(self,url) :
        try:
            response = requests.get(url).content
            
            soup = BeautifulSoup(response , 'html.parser')
            
            title = soup.find('div',{'class':'product__info-wrapper--left'}).text.rstrip().lstrip()
            
            old_price_integer = soup.find('div',{'class':'product__info__original-price__integer js-date-based-original-price-integer'}).text 
            old_price_decimal =  soup.find('div',{'class':'product__info__original-price__decimal js-date-based-original-price-decimal'}).text
            old_price = old_price_integer + old_price_decimal

            if old_price_integer == '' :
                old_price = soup.find('span',{'class':'js-old-price'}).text.rstrip().lstrip()
            try:
                old_price = old_price.replace(u'\xa0','')
            except:
                pass 
            
            promotion = soup.find('span',{'class':'js-date-based-discount-percentage-text'}).text
            if promotion == '' :
                promotion = soup.find('div',{'class':'product__info__discount-percentage js-discount-percentage'}).text.rstrip().lstrip()

            
            last_price_integer = soup.find('div',{'class':'product__info__new-price__integer js-price-integer'}).text
            last_price_decimal = soup.find('div',{'class':'product__info__new-price__decimal js-price-decimal'}).text
            last_price = last_price_integer + last_price_decimal
            try:
                last_price = last_price.replace(u'\xa0','')
            except:
                pass
            star_info = soup.find('div',{'class':'dropdown-menu product__header-summary__evaluation__dropdown'}).text.split('\n')[1]
            
            description = soup.find('div',{'class':'js-clear-inline-styles'}).text.lstrip().rstrip()

            extensions = []
            links = []
            for i in str(soup).splitlines()[249].split('https://cdn03') :
                if  '.ciceksepeti.com/' in i :
                    link = 'https://cdn03'+i.split(',')[0]      
                    if not link.split('/')[-1] in extensions :
                        link = link.replace((link.split('/')[5]),self.image_size) 
                        links.append(link.replace('"',''))
                        extensions.append(link.split('/')[-1])
                        
            return {
                    "link"       : url,
                    "star_info" : star_info ,
                    "title"     : title,
                    "pics"      : links,
                    "reel_price"     : old_price,
                    "promotion"   : promotion,
                    "last_price"  : last_price, 
                    "description" : description            
                }

        except :
            return None


class Ciceksepeti :
        
    def __init__(self,category_ciceksepeti = 'ev-hediyeleri' , page = 2 ,  category_letgo='diger' , price_type = 'last_price' ,
                 profit_rate = 10 , min_price = 100 , description = 'Default Description(AD)' , image_size = 'L' ) :
        self.category_ciceksepeti = category_ciceksepeti 
        self.page = page 
        self.category_letgo = category_letgo 
        self.price_type = price_type 
        self.profit_rate = profit_rate
        self.min_price = min_price
        self.description = description
        self.image_size = image_size
        self.basic = Basic()
        
    def get_links(self) :
        get_link = CiceksepetiData(self.category_ciceksepeti, self.page,self.image_size)
        links = get_link.get_links_from_category()
        return links 
           
    @property
    def run(self) :
        links = self.get_links() 
        for n,link in enumerate(links) :
            ciceksepeti_data = CiceksepetiData(self.category_ciceksepeti, self.page,self.image_size)
            data = ciceksepeti_data.get_product_detail(link)
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
ciceksepeti = Ciceksepeti(min_price=5,
                          description="Yıldız:{star_info}\nBaşlık:{title}\nİlk Fiyat:{reel_price}\nİndirim:{promotion}\nTanım:{description}\nSon Fiyat:{last_price}\n",price_type='reel_price')
ciceksepeti.run
"""