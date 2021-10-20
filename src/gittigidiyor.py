import requests 
from bs4 import BeautifulSoup 
from basic import Basic 

class GittigidiyorData :
    
    def __init__(self,category_name,page) :
        self.main_url = 'https://www.gittigidiyor.com/'
        self.page = page 
        self.category_name = category_name
    
    def get_links_from_category(self) : 
        links = set()
        for page in range(1,self.page+1) :
            try:
                response = requests.get(self.main_url+self.category_name+"?sf="+str(self.page)).content
                soup = BeautifulSoup(response,'html.parser')
                for a in soup.find_all('a', href=True)  :
                    link = a['href'].splitlines()[0]
                    if self.main_url+self.category_name in link and not "?sf=" in link and link.count('/')>3 :
                        links.add(self.main_url + link )
                    elif link[:29] == self.main_url and 'sf=' not in link and '_pdp_' in link :
                        links.add(link)

            except :
                pass

        return links

    def get_product_detail(self,url) :
        try:
            response = requests.get(url).content 
            soup = BeautifulSoup(response , 'html.parser')
            title = soup.find("h1", attrs={"class": "title r-onepp-title"}).text
            old_price = soup.find("span", attrs={"id": "sp-price-highPrice"}).text.rstrip().lstrip()
            rank = soup.find("span", attrs={"id": "sp-positiveCommentPercentage"}).text  
            discount = soup.find("span", attrs={"id": "sp-price-discountPercentage"}).text.rstrip().lstrip() 
            last_price = soup.find("div", attrs={"id": "sp-price-lowPrice"}).text.rstrip().lstrip() 
            
            if discount == '' :
                last_price = old_price
            
            try:
                star_info = soup.find("div", attrs={"class": "p0 review-point-container"}).text.rstrip().lstrip() 
            except:
                star_info = 'None'
            links = set()    
            for img in soup.findAll('img'):
                image = img.get('data-original')
                find_in = ['.jpg','cdn']
                find_out = ['kargo','fred']
                if all([substring in str(image) for substring in find_in]) and not any([substring in str(image) for substring in find_out])   :
                    image = str(image).split('.jpg')[0] + '.jpg'
                    if 'tn14' not in image:
                        links.add(image)
            
            return {
                    "link"       : url,
                    "star_info" : star_info ,
                    "title"     : title,
                    "pics"      : links,
                    "reel_price"     : old_price,
                    "promotion"   : discount,
                    "last_price"  : last_price ,
                    "rank" : rank           
                }       
        except :
            pass
 
class Gittigidiyor :
        
    def __init__(self,category_gittigidiyor = 'cep-telefonu' , page = 2 ,  category_letgo='diger' , price_type = 'last_price' ,
                 profit_rate = 10 , min_price = 100 , description = 'For details contact with me'  ) :
        self.category_gittigidiyor = category_gittigidiyor
        self.page = page 
        self.category_letgo = category_letgo 
        self.price_type = price_type 
        self.profit_rate = profit_rate
        self.min_price = min_price
        self.description = description
        self.basic = Basic()
        
    def get_links(self) :
        get_link = GittigidiyorData(self.category_gittigidiyor, self.page)
        links = get_link.get_links_from_category()
        return links 
           
    @property
    def run(self) :
        links = self.get_links() 
        for n,link in enumerate(links) :
            gittigidiyor_data= GittigidiyorData(self.category_gittigidiyor, self.page)
            data = gittigidiyor_data.get_product_detail(link)
            print(f'Scannig Url {n+1}/{len(links)} : {link} ')
            try:
                if len(data["pics"]) > 0 and float(data[self.price_type].split()[0].split(",")[0].replace('.','')) > self.min_price  :
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
                    self.basic.connect_to_letgo(data,price,self.category_letgo,data["title"],new_description) 
                    self.basic.remove_pics(data)
                    print('Succesfull.')
            except  AttributeError :
                print('This Link Doesnt Support Selected Price Type.')
            except Exception as err:
                print(f'An Error Occurred. Error is : {err} ')
   
"""
gittigidiyor = Gittigidiyor('cep-telefonu',3,'elektronik','last_price',10,50,
                            'Başlık:{title}\nİlk Fiyat:{reel_price}\nİndirim:{promotion}\nSon Fiyat:{last_price}\nRank:{rank}\n' )

gittigidiyor.run
"""
