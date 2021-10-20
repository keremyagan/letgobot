from gittigidiyor import Gittigidiyor
from amazon import Amazon
from ciceksepeti import Ciceksepeti
from n11 import N11
from trendyol import Trendyol
from hepsiburada import Hepsiburada
from fromexcel import fromExcel

def get_info() :
    site_name = input('Please Enter Site Name:')
    site_category = input('Please Enter Site Category:')
    site_page = int(input('Please Enter Page of Site To Scan:'))
    letgo_category = input('Please Enter Letgo Category:')
    price_type = input('Please Enter Price Type:')
    min_price = float(input('Please Enter Minimum Price:'))
    description = input('Please Enter Description:')
    description = description.replace('*','\n')
    profit_rate = float(input('Please Enter Profit Rate:'))
    pic_size = input('Please Enter Pic Size if Available:')
    return site_name,site_category,site_page,letgo_category,price_type,min_price,description,profit_rate,pic_size

site_name,site_category,site_page,letgo_category,price_type,min_price,description,profit_rate,pic_size = get_info()

if site_name.lower() == 'gittigidiyor' :
    gittigidiyor = Gittigidiyor(site_category,site_page,letgo_category,price_type,profit_rate,min_price,
                                description )
    gittigidiyor.run   
    
elif site_name.lower() == 'amazon' :
    if pic_size == '' :
        pic_size = 'US40'
    amazon = Amazon(site_category,site_page,letgo_category,price_type,profit_rate,min_price,
                                description,image_size=pic_size)
    amazon.run

elif site_name.lower() == 'ciceksepeti' :
    if pic_size == '' :
        pic_size = 'L'
    ciceksepeti = Ciceksepeti(site_category,site_page,letgo_category,price_type,profit_rate,min_price,
                                description,image_size=pic_size)
    ciceksepeti.run

elif site_name.lower() == 'n11' :
    n11 = N11(site_category,site_page,letgo_category,price_type,profit_rate,min_price,
                                description)
    n11.run

elif site_name.lower() == 'trendyol' :
    trendyol = Trendyol(site_category,site_page,letgo_category,price_type,profit_rate,min_price,
                                description)
    trendyol.run   

elif site_name.lower() == 'hepsiburada' :
    if pic_size == '' :
        pic_size = '500'
    hepsiburada = Hepsiburada(site_category,site_page,letgo_category,price_type,profit_rate,min_price,
                                description,image_size=pic_size)
    hepsiburada.run    