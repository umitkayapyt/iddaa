# -*- coding: utf-8 -*-

# bütün karşılaşmaların kazanan oranları 18x70 boyutlu tablo hale getiriliyor.
# top15 en çok kazandıran oranlar ve bu oranların toplam analizleri
# unique oranlar


import pandas as pd
import openpyxl
import re


df = pd.read_excel('DBALL.xlsx', engine='openpyxl')


def Pivot2(textUzunluk, df, textColumn):
    uzunluk = len(df[textUzunluk])
    GelenOranlar    = []
    for indx in df[textColumn]:
        if indx !='' and indx !='-': 
            idda = re.search("(?<=\\[).*?(?=\\])", str(indx)) # [] parantez içindeki oran
            if idda:
                idda = idda.group()
                GelenOranlar.append(idda)
                
    sett = set(GelenOranlar)            
    if len(sett) < 10: #burayı kontrol et!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        fark =10-len(sett)
        for m in range(int(fark)):
            GelenOranlar.append('yok-{}'.format(m+1))
       
    DfIndex= ['Toplam Oynanan Mac', 'Toplam Gelen Oran', 'top10-1','top10-2','top10-3','top10-4','top10-5',
             'top10-6','top10-7','top10-8','top10-9','top10-10','top10-11','top10-12','top10-13','top10-14',
              'top10-15','unique']
    
    count  = len(GelenOranlar) #gelen toplam oran
    unique = len(df[textColumn].unique()) #gelen oranlar benzersiz/çeşit
    
    GelenOranlarDF = pd.DataFrame(data=GelenOranlar,index=range(len(GelenOranlar)),columns=[textColumn])
    top10   = GelenOranlarDF.value_counts()[:15] #ilk 10 gelen oran / top5 ve kaç kere gelmiş
    for m in top10.index:
        s    = str(m).replace('(','').replace(')','').replace(',','').replace('\'','')
        
    columnNewData = [uzunluk, count]
    for en, c in enumerate(top10):
        s    = str(top10.index[en]).replace('(','').replace(')','').replace(',','').replace('\'','')
        tp = str(len(df[df[textColumn] == s])+c)
        try:
            yz = c / int(tp)
            yz = "{:.2f}".format(yz)
        except ZeroDivisionError:
            yz = str(0)
        sTop = '%{}  {}   {}/{}'.format(yz,s,str(c),tp) # +'  %'+str(len(df[df[textColumn] == s])/c)
        columnNewData.append(sTop)
    columnNewData.append(unique)
    dff = pd.DataFrame(data=columnNewData,index=DfIndex, columns=[textColumn])

    return dff

OranCesitleri = df.columns
OranCesitleri1 = [OranCesitleri[8:63]]
OranCesitleri2 = [OranCesitleri[67:71]]
OranCesitleri3 = [OranCesitleri[73:84]]
OranCesitleriSon = OranCesitleri1 + OranCesitleri2 + OranCesitleri3

OranCesitleriSonn = []
for i in OranCesitleriSon[0]:
    OranCesitleriSonn.append(i)
for i in OranCesitleriSon[1]:
    OranCesitleriSonn.append(i)
for i in OranCesitleriSon[2]:
    OranCesitleriSonn.append(i)


Sontable = pd.DataFrame()
for son in OranCesitleriSonn:
    table = Pivot2(textUzunluk='ZamanSerisiTS', df=df, textColumn = str(son))
    Sontable =pd.concat([Sontable, table],axis=1)

from os import path
import os
path = os.path.join(os.path.expanduser("~"), "Desktop", "Oran_Analizi.xlsx")
Sontable.to_excel(path)