import requests
from bs4 import BeautifulSoup
import csv
import re


URL = 'https://playgames.ru/category/videoigry/playstation/playstation-4/igry/?page={}'
HEADERS = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
HOST = 'https://playgames.ru'


tovar = []
catalog = []
links = []
path='play.csv'
  
r = requests.get(URL,headers = HEADERS)
soup = BeautifulSoup(r.text,'html.parser')

def xl(items,path):
    with open (path,'w',newline='') as csv_file:
        writer = csv.writer(csv_file,delimiter=';')
        writer.writerow(['название','цена','разработчик','издатель','релиз','жанр','код товара','главное фото','дополнительные фотографии','путь','Описание','наличие','Видео'])
        for item in items :
            writer.writerow([item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12]])
        
    


for  page in range(1,3):
    r = requests.get(URL.format(page))
    soup = BeautifulSoup(r.text,'html.parser')
    main_ul = soup.find('div',class_='right_col')
    li = main_ul.findAll('li',itemtype="http://schema.org/Product")
    catalog.extend(li)



for sub in catalog:
    link =  HOST + sub.find('div',class_="tab_name").a['href'] 
    links.append(link)
    
    

for i in links :

    rnd =1
    gnar ='Нет информации'
    isd = 'Нет информации'
    raz='Нет информации'
    rel = 'Нет информации'
    col_igr = 'Нет информации'
    cor_nal = ''
    a =True
    unnes = False
    other_foto=''
    character =''
    print(i)
    product=[]
    r = requests.get(i,headers = HEADERS)
    soup = BeautifulSoup(r.text,'html.parser')
    
    title = soup.find('h1',class_='namep').get_text(strip=True)
    price = soup.find('span',class_='price nowrap')['data-price']
    code = soup.find('div',class_='code').get_text(strip =True)
    nal = soup.find('span',class_='dop-price').get_text(strip = True)
    for nl in nal:
        if nl == '.':
            unnes=True
            old_price=len(soup.find('span',class_='dop-price').span.get_text(strip = True)) 
            cor_nal = nal[old_price:]
            
    if unnes == False:
        cor_nal = nal


    if cor_nal =='':
        cor_nal = 'нет информации'    
        
        
        
    
    video = soup.find('iframe')
    if video == None:
        video = 'нет информации'
    else:
        video = video['src']
        
    main_img = HOST+soup.find('a',class_='galer swipebox').img['src']
    charac = soup.find('table',class_='summary').get_text(strip=True)
    charac = re.findall(r'[А-Я]?[^А-Я]*',charac)
    print(charac)

    
    for ch in charac:
       if 'Издатель' in ch :
           isd = ch[10:]
           
       elif 'Разработчик:' in ch :
           raz = ch[13:]
           
       elif 'Дата выхода:' in ch :
           rel = ch[11:]
           
       elif 'Релиз:' in ch :
           rel = ch[6:]
       elif 'Жанр' in ch:
           if  len(ch)>6:
               gnar = ch[6:]
           else:    
               gnar = charac[rnd]
               if '\\' in gnar:
                   gnar+=charac[rnd+1]
                   
                
           print(gnar)
           
           
       rnd+=1        
           
       
    if 'игр' in rel:
       col_igr = rel[-7:]
       rel = rel[:-7]
       
    if ':' in rel:
        rel= rel[1:]
       
        
    
    
        
    
    way = soup.find('nav',class_='breadcrumbs').get_text(strip=True)
    
    des = soup.find('div',class_='description')

    nal = soup.findAll('div',class_='cart')
    for nl in nal:
        pass
        
         

   

    dop_foto = soup.findAll('a',class_='swipebox')
    for fot in dop_foto:
        f =  HOST+fot.img['src'].replace('\n','').replace('\t','').replace(' ','')
        other_foto+=f
        other_foto+=','
        other_foto+=' '

    
            
        
        
        
        
    
    
    
        
    
    product.append(title.replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(price.replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    
    product.append(isd.replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(raz.replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(rel.replace('\n','').replace('\t','').replace(' ','').replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(gnar.replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    
    product.append(code[12:].replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(main_img.replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(other_foto[:-2].replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(way.replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(str(des)[73:-6].replace('\n','').replace('\t','').replace(' ','').replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    product.append(cor_nal.replace('\u200e','').replace('\ufeff',''))
    product.append(video.replace('\n','').replace('\t','').replace(' ','').replace('\u200e','').replace('\u2219','').replace('\ufeff',''))
    
    
    tovar.append(product)
    xl(tovar,path)
   
    
    


    




    


