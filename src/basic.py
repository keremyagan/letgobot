import os 
import requests 
from letgo import Letgo

class Basic :
    
    def __init__(self) :
        pass 
    
    def download_pic(self,url) :
        pic_url_save = url.replace("'","").split("/")[-1]
        with open(pic_url_save, 'wb') as handle:
            response = requests.get(url , stream=True)
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block) 
                
    def save_pic_to_file(self,data) :
        file = open("pic.txt","w") 
        file.close()
        file1 = open("pic.txt","a",encoding="utf-8")
        for n,pic_url in enumerate(data["pics"]) :
            pic_url_save = pic_url.replace("'","").split("/")[-1]
            file1.write(fr"{os.getcwd()}\{pic_url_save}")
            if n != len(data["pics"])-1 :
                file1.write("\n")
        file1.close()
    
    def remove_pics(self,data) :
        for pic_url in data["pics"] :
            pic_url_save = pic_url.replace("'","").split("/")[-1]
            os.remove(pic_url_save) 
            
    def connect_to_letgo(self,data, price , category_name , title , description ) :
        try:
            letgo = Letgo(category_name, price , title ,description )
            letgo.sale_first_click()
            letgo.select_category()
            letgo.add_pic()
            letgo.add_details()
            letgo.close_driver()        
        except:
            try:
                letgo.close_driver()
            except:
                pass
 
    def set_description(self,description,data) :
        features = data.keys()
        for feature in features :
            if f'{feature}' in description and isinstance(data[feature],(str,float,int)):
                description =  description.split("{" +f"{feature}" + "}")[0] + data[feature] + description.split("{" +f"{feature}" + "}")[1]
            if f'{feature}' in description and data[feature] is None :
                description =  description.split("{" +f"{feature}" + "}")[0] + 'None' + description.split("{" +f"{feature}" + "}")[1]
                
        return description             