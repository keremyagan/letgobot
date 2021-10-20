import requests 
from bs4 import BeautifulSoup
from parsel import Selector
from basic import Basic 

class TrendyolData :
     
    def __init__(self) :
        self.session = requests.Session()
        self.header = {'UserAgent':'UserAgent'}
        
    def get_links_from_category(self, category_name, page=1) :
        data = []
        for n in range(1, page+1):
            response   = requests.get(f"https://www.trendyol.com/{category_name}?pi={n}", headers=self.header)
            selector  = Selector(response.text)

            products = selector.xpath("//div[@class='prdct-cntnr-wrppr']//div[@class='p-card-chldrn-cntnr']")

            for product in products:
                link1 = "https://www.trendyol.com" + product.xpath(".//a/@href").get()
               
                data.append(link1)

        return data
                      
    def get_product_detail(self,link) :
        try:
            response = requests.get(link)
        except :
            return None

        selector = Selector(response.text)

        links = set()
        soup = BeautifulSoup(response.content, "html.parser")
        for img in soup.findAll('img'):
            image = img.get('src')
            if ".jpg" in str(image) and "cdn." in str(image)  :
                extensions = []
                for i in links :
                    extensions.append(i.split("/")[-1])
                
                if not str(image).split("/")[-1] in extensions :
                    links.add(image)

        try:
            return {
                "link"       : link,
                "brand"      : selector.xpath("//h1[@class='pr-new-br']/a/text()").get().strip() if selector.xpath("//h1[@class='pr-new-br']/a/text()").get() else selector.xpath("//h1[@class='pr-new-br']/text()").get().strip(),
                "title"     : selector.xpath("//h1[@class='pr-new-br']/span/text()").get().strip(),
                "pics"      : links,
                "reel_price"     : selector.xpath("//span[@class='prc-org']/text()").get(),
                "discount_price"  : selector.xpath("//span[@class='prc-slg prc-slg-w-dsc']/text()").get() or selector.xpath("//span[@class='prc-slg']/text()").get(),
                "promotion"   : selector.xpath("//div[@class='pr-bx-pr-dsc']/text()").get(),
                "last_price"  : selector.xpath("//span[@class='prc-dsc']/text()").get(),
            }
        except:
            return None

class Trendyol :
    
    def __init__(self,category_trendyol = 'elektronik' , page = 2 ,  category_letgo='elektronik' , price_type = 'last_price' ,
                 profit_rate = 10 , min_price = 100 , description = 'For details contact with me' ) :
        self.category_trendyol = category_trendyol 
        self.page = page 
        self.category_letgo = category_letgo 
        self.price_type = price_type 
        self.profit_rate = profit_rate
        self.min_price = min_price
        self.description = description
        self.basic = Basic()
        
    def get_links(self) :
        get_link = TrendyolData()
        links = get_link.get_links_from_category(self.category_trendyol, self.page)
        return links 
           
    @property
    def run(self) :
        links = self.get_links() 
        for n,link in enumerate(links) :
            trendyol_data = TrendyolData()
            data = trendyol_data.get_product_detail(link)
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
                    profit_rate = 1 + (self.profit_rate/100)
                    price = int(float(data[self.price_type].replace(".","").split()[0].split(",")[0])*profit_rate)
                    new_description = self.basic.set_description(self.description,data)
                    print(new_description)
                    self.basic.connect_to_letgo(data,price,self.category_letgo,data["title"],new_description) 
                    self.basic.remove_pics(data)
                    print('Succesfull.')
            except  AttributeError :
                print('This Link Doesnt Support Selected Price Type.')

            except Exception as err:
                print(f'An Error Occurred. Error is : {err} ')
           

"""                              
trendyol = Trendyol(description="Marka:{brand}\nBaşlık:{title}\nİlk Fiyat:{reel_price}\nİndirim:{promotion}\nİndirimli Fiyat:{discount_price}\nSon Fiyat:{last_price}\n",price_type='reel_price',
                    min_price=5)
trendyol.run
"""


