import pandas as pd
from basic import Basic 

class fromExcel :
        
    def __init__(self,file_path) :
        self.file_path = file_path
        self.basic = Basic()
        
    def read_file(self):
        try :
            df = pd.read_excel(self.file_path)
            return df 
        except :
            print('An Error Occurred While Reading Excel File.')
    
    def get_data(self) :
        try:
            df = self.read_file()
            titles = df.iloc[:,0:1].values 
            descriptions = df.iloc[:,1:2].values
            prices  = df.iloc[:,2:3].values
            categories = df.iloc[:,3:4].values
            image_links = df.iloc[:,4:5].values  
            
            return {
                    "title"     : titles,
                    "pics"      : image_links,
                    "last_price"  : prices ,
                    'description' : descriptions ,
                    'category' : categories
                }   
                
        except :
            pass
             
    @property
    def run(self) :
        df = self.read_file()
        data = self.get_data()
        for n in range(len(df)) :
            print(f'Scannig Url {n+1}/{len(df)}')
            try:
                data = data[n]
                if len(data["pics"]) > 0 :
                    print(f"This Link will be shared on Letgo:\nProduct Title : {data['title']}\nProduct Price : {data['last_price']}")
                    if len(data["pics"]) > 7 :
                        data["pics"] = list(data["pics"])[:7]
                    for pic_url in data["pics"]:
                        print('Getting Pics.')
                        self.basic.download_pic(pic_url)
                    self.basic.save_pic_to_file(data)
                    print('Connecting to Letgo.')
                    self.description = self.basic.set_description(self.description,data)
                    print(self.description)
                    profit_rate = 1 + (self.profit_rate/100)
                    price = int(float(data[self.price_type].replace(".","").split()[0].split(",")[0])*profit_rate)
                    self.basic.connect_to_letgo(data,price,self.category_letgo,data["title"],self.description) 
                    self.basic.remove_pics(data)
                    print('Succesfull.')
            except  AttributeError :
                print('This Link Doesnt Support Selected Price Type.')
            except Exception as err:
                print(f'An Error Occurred. Error is : {err} ')
   