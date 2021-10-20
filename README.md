### Features

- Amazon Data
- N11 Data
- Trendyol Data
- Gittigidiyor Data
- Ciceksepeti Data
- Hepsiburada Data
- Support Loading File from Excel 
- Support Choosing Pic Size(if available)
- Support Choosing Profit Rate 
- Support Choosing Minimum Price
- Support Using Description With Variables
- Support Price Type(Discount Price, First Price,Last Price)
- Runs with Default User Account
# Letgo Bot Pro
![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Letgo_logo.png/150px-Letgo_logo.png)

**Table of Contents**

[TOCM]

[TOC]

#What is Letgo Bot Pro ? 
Letgo Bot Pro is a bot which shares post on Letgo . The bot contains some features . Usable some shopping sites products to share on Letgo . You can choose site name , category name  ,  profit rate , price type , minimum price , description .  
##Site Name
The bot can get data from some websites :
- Amazon 
- N11 
- Trendyol 
- Gittigidiyor
- Ciceksepeti 
- Hepsiburada . 
Other websites addable easily because this project developed with OOP .
##Category Name 
You can choose category from websites but there is a important point. You need to check category name from website before running bot . 
##Profit Rate
Profit rate calculates out of 100 so if profit rate is 5 equal to %5 . Bot adds profit to price .
Default profit rate is 10 . (int)
##Price Type 
Some products may have discounts . You can choose price type to use on calculating profit rate . Options are last_price , reel_price , discount_price . 
last_price is last price of product .
reel_price is first price of product .
discount_price is discounted price of product (some website doesnt support it) 
Default price type is last_price . (str)
##Minimum Price
Some products have low price . You can use minimum price feature to dont share this products .
Default min_price 100 . (int)
## Description 
Description required on Letgo . You can use same description all products or use special description . For example you can add brand name of product to description . Description variables changes from website to website, please look at what  'get_product_detail' function returns . This variables usable on description . 
Example Usage : Brand Name :{brand}
To go to the bottom line , use '\n' .
##Page Number 
The bot scans website . You can choose page number to scanning .
Default page number is 2 . (int)
##Image Size 
Some website supports image size . You can change if available .
##Letgo Category 
Category required on Letgo . 
Category names :
- elektronik 
- spor
- araba 
- motosiklet
- ev 
- moda
- bebek
- film
Default is 'diger' . (str)

#Usage of the Bot 
You can use direct a website data . Choose site name and look at relevant python file . Each file contains example usage code in comment lines the bottom of page .


#Notes : 
- Bot uses Chrome browser with default user so  loginnig Letgo one time is a enough to share post .  
- Chrome must be closed before bot running . Bot opens browser . 


[![Video](https://disk.yandex.com.tr/client/disk/Letgo?idApp=client&dialog=slider&idDialog=%2Fdisk%2FLetgo%2Fletgociceksepeti.mp4 "Video")](https://disk.yandex.com.tr/client/disk/Letgo?idApp=client&dialog=slider&idDialog=%2Fdisk%2FLetgo%2Fletgociceksepeti.mp4 "Video")
