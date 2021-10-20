import requests 
from bs4 import BeautifulSoup 
from basic import Basic 
class HepsiburadaData :
    
    def __init__(self,category_name,page,default_size = 500) :
        self.category_name = category_name
        self.page = page
        self.default_size = default_size
        self.sitemap_category_url = 'https://www.hepsiburada.com/sitemaps/kategoriler/sitemap_1.xml'
        self.header = {'User-Agent': 'keremyagan'}
        self.main_url = 'https://www.hepsiburada.com/'

    def get_categories(self) :
        response = requests.get(self.sitemap_category_url ,headers = self.header ).content
        links = []
        for i in str(response).split('<loc>') :
            link = i.split('</loc>')[0]
            links.append(link)
        
        return links 
        
    def get_correct_links(self) :
        links = self.get_categories()
        correct_link = ''
        for link in links :
            if self.category_name in link and link.index(self.category_name) == 28 :
                if len(link.split(self.category_name)[0]+self.category_name) == link.index('-c-') :
                    correct_link = link
    
        if correct_link == '' :
            print('''Please Check Category Name. May be You Need To Add -lari/-leri to Category Name
                  for example correct category name : cep-telefonlari ''')
        
        else :
            return correct_link
 
    def get_links_from_category(self) : 
        links = set()
        correct_url = self.get_correct_links()
        for page in range(1,self.page+1) :
            try:   
                url = correct_url+"?sayfa="+str(self.page)
                if page == 1 :
                    url = correct_url

                response = requests.get(url, headers = self.header ).content
                soup = BeautifulSoup(response,'html.parser')
                find_in = [self.main_url,'-p-HB']
                for a in soup.find_all('a', href=True)  :
                    link = a['href']
                    if all([substring in str(link) for substring in find_in]) : 
                        links.add(link)

            except :
                pass
        
        return links

    def get_product_detail(self,url) : 
        try:
            response = requests.get(url , headers = self.header).content
            soup = BeautifulSoup(response , 'html.parser')
            
            brand = soup.find('span',{'class':'brand-name'}).text.rstrip().lstrip()
            title = soup.find('h1',{'id':'product-name'}).text.rstrip().lstrip()
            promotion = soup.find('span',{'id':'product-discount-rate'}).text.rstrip().lstrip().split()[0]
            old_price = soup.find('del',{'id':'originalPrice'}).text.rstrip().lstrip()
            discount_price = soup.find('span',{'data-bind':"markupText:'currentPriceBeforePoint'"}).text.rstrip().lstrip()
            last_price = soup.find('div',{'class':'extra-discount-price'}).text.rstrip().lstrip()
            links = set()
            first_code = ''
            for img in soup.findAll('img'):    
                image = img.get('src')
                if 'productimages' in str(image) and '/80/' in str(image) : 
                    img_link = image.replace('/80/',f'/{self.default_size}/')
                    if first_code == '' :
                        first_code = img_link.split(f'/{self.default_size}/')[0][-3:] + '/'
                        links.add(img_link)
                        
                    else :
                        if first_code in img_link :
                            links.add(img_link)

            description = soup.find('div',{'id':'productDescriptionContent'}).text
            description = description.replace(u'\xa0','')
            #it can be edited for text type
            return {
                    "link"       : url,
                    "brand"  : brand ,
                    "title"     : title,
                    "pics"      : links,
                    "reel_price"     : old_price,
                    "promotion"   : promotion,
                    "discount_price" : discount_price ,
                    "last_price"  : last_price ,
                    "description" : description           
                }  
        except :
            pass

   
class Hepsiburada :
        
    def __init__(self,category_hepsiburada = 'cep-telefonlari' , page = 2 ,  category_letgo='elektronik' , price_type = 'last_price' ,
                 profit_rate = 10 , min_price = 100 , description = 'Default Description(AD)' , image_size = '500' ) :
        self.category_hepsiburada = category_hepsiburada 
        self.page = page 
        self.category_letgo = category_letgo 
        self.price_type = price_type 
        self.profit_rate = profit_rate
        self.min_price = min_price
        self.description = description
        self.image_size = image_size
        self.basic = Basic()
        
    def get_links(self) :
        get_link = HepsiburadaData(self.category_hepsiburada, self.page,self.image_size)
        links = get_link.get_links_from_category()
        return links 
           
    @property
    def run(self) :
        links = self.get_links() 
        for n,link in enumerate(links) :
            hepsiburada_data = HepsiburadaData(self.category_hepsiburada, self.page,self.image_size)
            data = hepsiburada_data.get_product_detail(link)
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
hepsiburada = Hepsiburada(min_price=5,
                          description="Marka:{brand}\nBaşlık:{title}\nİlk Fiyat:{reel_price}\nİndirim:{promotion}\nTanım:{description}\nSon Fiyat:{last_price}\n",price_type='reel_price')
hepsiburada.run
"""