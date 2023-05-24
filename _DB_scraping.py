# -*- coding: utf-8 -*-
# WebScraping
# Kazınan verilerin 88 kolonlu tablo haline getirilmesi 
# Kazandıran oranların liste içerisinde target [2.07]
# kaynak adres: 'http://www.******.com/iddaa-programi/'


from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select # WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup

from nltk import flatten
from collections import Iterable
from time import sleep, strftime
from locale import setlocale, LC_ALL, LC_TIME
from cv2 import imread
from pandas import DataFrame, to_datetime, concat
from pathlib import Path
from bs4 import BeautifulSoup
from sys import argv, exit
from os import path
import regex as re
import os
import openpyxl


setlocale(LC_ALL,'Turkish_Turkey.1254')
setlocale(LC_TIME, "tr")

class IddiaDB(): # QMainWindow
        
    def __init__(self):
    #     super(IddiaDB, self).__init__()

        # self.ui = Ui_MainRaporKontrol()
        # self.ui.setupUi(self)

        self.ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        self.home = str(Path.home())+'\\iddiaDB'
        self.WeekName = ''
        self.DayName  = ''
        #kolonlar;

        self.Giris()


    def flatten(self, lis):
            for item in lis:
                if isinstance(item, Iterable) and not isinstance(item, str):
                    for x in self.flatten(item):
                        yield x
                else:        
                    yield item

    def Giris(self): # kazıma / tablolara aktarma
        
        # options = Options()
        # options.set_headless(headless=True)     
        # self.driver = webdriver.Chrome(r'C:\Users\umit\data science\PyQt5\_Rapor_Kontrol\chromedriver.exe', options=opt)
        # dosya = self.ui.txtDosyaYolLoad.text()
        self.site = 'http://www.*****.com/iddaa-programi/'

        # try:
        opt = webdriver.ChromeOptions()
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        opt.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(self.home+r'\chromedriver.exe', options=opt)
        self.driver.get(self.site)
        sleep(0.5)

################################################################# Haftalar ####################################################################################

        HaftaXPathSelect = self.driver.find_element(By.ID, 'iddaa_daterange')
        HaftaXPathSelectText = HaftaXPathSelect.get_attribute("textContent").strip()
        slices = int(len(HaftaXPathSelectText) / 23)
        Haftaliste = []
        s = 0
        l = 23
        for i in range(slices):
            slc = HaftaXPathSelectText[s:l]
            Haftaliste.append(slc)
            s += 23
            l += 23
        
        selectHafta = Select(self.driver.find_element(By.ID, 'iddaa_daterange'))
        selectTextHafta = Haftaliste[0] #seççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççç
        selectHafta.select_by_visible_text(selectTextHafta) #Hafta Burada Seçiliyor
        sleep(12)
        self.WeekName = selectTextHafta

################################################################ Gün Seçimi ####################################################################################

        GunXPathSelect = self.driver.find_element(By.ID, 'iddaa_dateselector')
        GunXPathSelectText = GunXPathSelect.get_attribute("textContent").strip()
        Hespi = GunXPathSelectText[:5]
        GunXPathSelectText = GunXPathSelectText[22:]
        slices = int(len(GunXPathSelectText) / 10)
        Gunliste = []
        s = 0
        l = 10
        for i in range(slices):
            slc = GunXPathSelectText[s:l]
            Gunliste.append(slc)
            s += 10
            l += 10
        Gunliste.append(Hespi)
        # print(['02.05.2023', '03.05.2023', '04.05.2023', '05.05.2023', '06.05.2023', '07.05.2023', '08.05.2023', 'Hepsi'])
        selectGun = Select(self.driver.find_element(By.ID, 'iddaa_dateselector'))
        selectTexGun = Gunliste[7] #seçççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççççç #7-Hepsi
        selectGun.select_by_visible_text(selectTexGun) #Gün burada seçiliyor
        sleep(12)
        self.DayName = selectTexGun

################################################################ Click ####################################################################################

        # self.driver.find_element_by_xpath(
        #         '//*[@id="iddaa_ajaxtable"]/div/table/tbody/tr[2]/td/label[3]/input'
        #     ).click()

        # sleep(4)
        
        soup=BeautifulSoup(self.driver.page_source,"html.parser")

##########################################################################################################################################################
################################################################## KAZIMA İŞLEMLERE #########################################################################
##########################################################################################################################################################

################################################################ Takımlar Kazıma ####################################################################################
        
        Takimlar__Soup = soup.find_all("span", class_="hide-on-mobile")
        Takimlar = []
        for span in Takimlar__Soup:
            Takimlar.append(span.text)
        Takimlar = Takimlar[3:]
        
        Evsahibi  = Takimlar[::2]
        Deplasman = Takimlar[1::2]

############################################################# Klasman-MBS-IY Kazıma ####################################################################################
        
        Klasman_MBS_IY__Soup = soup.find_all("td", class_="hide-on-mobile")
        Klasman_MBS_IY = []

        for td in Klasman_MBS_IY__Soup:
            Klasman_MBS_IY.append(td.text)

        Klasman = Klasman_MBS_IY[::3]
        MBs     = Klasman_MBS_IY[1::3]
        İlkYari = Klasman_MBS_IY[2::3]

############################################################## Maç Sonucu Kazıma ####################################################################################
        
        Klasman_Ev_MacSonucu_Dep__Soup = soup.find_all("a", target="_blank")
        Klasman_Ev_MacSonucu_Dep = []

        for a in Klasman_Ev_MacSonucu_Dep__Soup:
            Klasman_Ev_MacSonucu_Dep.append(a.text)
        Klasman_Ev_MacSonucu_Dep = Klasman_Ev_MacSonucu_Dep[3:]

        MacSonucu = Klasman_Ev_MacSonucu_Dep[2::4]

################################################################ Maç Saati Kazıma ####################################################################################

        Tarih__Soup = soup.find_all("tr", class_="tablemainheader")
        Tarih = []  #sayfadaki tarihler
        for tr in Tarih__Soup:
            Tarih.append(tr.text)
        Tarih = Tarih[1:]

        MacSaati__Soup = soup.find_all('td', attrs={'sortvalue' : True})
        MacSaati = [] #maç saatleri
        for tds in MacSaati__Soup:
            MacSaati.append((tds.text).strip())

        MacTarihi__Soup = soup.find_all('i', {'class': 'fa fa-angle-double-right'})
        MacTarihi = [] #titleda tarih bulunan tarihler
        for trh in MacTarihi__Soup:
            MacTarihi.append(trh.get('title'))
        
        ZamanSerisi = []
        if len(MacTarihi) == len(MacSaati):
            for trih, zmn in zip(MacTarihi, MacSaati):
                ZamanSerisi.append(trih+' '+zmn)
        else:
            frk = len(MacSaati) - len(MacTarihi)
            for zman in MacSaati[:frk]:
                ZamanSerisi.append(Tarih[0]+' '+zman)
            for tarih, zaman in zip(MacTarihi, MacSaati[frk:]):
                ZamanSerisi.append(tarih+' '+zaman)
        # ZamanSerisiTS = to_datetime(ZamanSerisi, format="%d.%m.%Y %H:%M")
        ZamanSerisiTS = ZamanSerisi

#######################################################################################################################################################
################################################################# ORANLAR KAZIMA ####################################################################################
#####################################################################################################################################################
       
        Tuttu__Soup = soup.find_all("span", class_="betred")
        Tuttu = []
        for spanr in Tuttu__Soup:
            Tuttu.append(spanr.text)
        
        Diger__Soup = soup.find_all("span", class_="betwhite")
        Diger = []
        for spanw in Diger__Soup:
            Diger.append(spanw.text)

        Oran_detail__Soup = soup.find_all("tr", class_="detail")
        Oran_detail = []
        for sw in Oran_detail__Soup:
            Oran_detail.append(sw.text)
        
        # KOLONLARIN HAZIRLANMASI
        CifteSans_1_0_ = []
        CifteSans_1_2_ = []
        CifteSans_0_2_ = []
        Ilk_Yari_CifteSans_10_ = []
        Ilk_Yari_CifteSans_12_ = []
        Ilk_Yari_CifteSans_02_ = []
        Ilk_Yari_Sonucu_1_ = []
        Ilk_Yari_Sonucu_0_ = []
        Ilk_Yari_Sonucu_2_ = []
        Ikinci_Yari_Sonucu_1_ = []
        Ikinci_Yari_Sonucu_0_ = []
        Ikinci_Yari_Sonucu_2_ = []
        Ilk_Yari_15_Alt_ = []
        Ilk_Yari_15_Ust_ = []
        MS_15_Alt_ = []
        MS_15_Ust_ = []
        MS_35_Alt_ = []
        MS_35_Ust_ = []
        MS_Tek_ = []
        MS_Cift_ = []
        Toplam_Gol_0_1_ = []
        Toplam_Gol_2_3_ = []
        Toplam_Gol_4_5_ = []
        Toplam_Gol_6_a_ = []
        IlkYari_MacSonucu_1_1_ = []
        IlkYari_MacSonucu_1_0_ = []
        IlkYari_MacSonucu_1_2_ = []
        IlkYari_MacSonucu_0_1_ = []
        IlkYari_MacSonucu_0_0_ = []
        IlkYari_MacSonucu_0_2_ = []
        IlkYari_MacSonucu_2_1_ = []
        IlkYari_MacSonucu_2_0_ = []
        IlkYari_MacSonucu_2_2_ = []
        MacSkoru_1__1_0_ = []
        MacSkoru_1__2_0_ = []
        MacSkoru_1__3_0_ = []
        MacSkoru_1__4_0_ = []
        MacSkoru_1__5_0_ = []
        MacSkoru_1__2_1_ = []
        MacSkoru_1__3_1_ = []
        MacSkoru_1__4_1_ = []
        MacSkoru_1__5_1_ = []
        MacSkoru_1__3_2_ = []
        MacSkoru_1__4_2_ = []
        MacSkoru_1__5_2_ = []
        MacSkoru_1__4_3_ = []
        MacSkoru_1__5_3_ = []
        MacSkoru_1__5_4_ = []
        MacSkoru_0__0_0_ = []
        MacSkoru_0__1_1_ = []
        MacSkoru_0__2_2_ = []
        MacSkoru_0__3_3_ = []
        MacSkoru_0__4_4_ = []
        MacSkoru_0__5_5_ = []
        MacSkoru_2__0_1_ = []
        MacSkoru_2__0_2_ = []
        MacSkoru_2__0_3_ = []
        MacSkoru_2__0_4_ = []
        MacSkoru_2__0_5_ = []
        MacSkoru_2__1_2_ = []
        MacSkoru_2__1_3_ = []
        MacSkoru_2__1_4_ = []
        MacSkoru_2__1_5_ = []
        MacSkoru_2__2_3_ = []
        MacSkoru_2__2_4_ = []
        MacSkoru_2__2_5_ = []
        MacSkoru_2__3_4_ = []
        MacSkoru_2__3_5_ = []
        MacSkoru_2__4_5_ = []

########################################################################## REGEPX ##########################################################################
       
        for son1 in Oran_detail:
            CifteSans_1_0 = re.search("(?<=\\n\\n\\nÇifte Şans\\n[0-9]\\n1/X).*?(?=\\n1/2)", son1)
            try:
                CifteSans_1_0 = CifteSans_1_0.group()
                CifteSans_1_0_.append(CifteSans_1_0)
            except:
                CifteSans_1_0_.append('Basket')

            CifteSans_1_2 = re.search("(?<=\\n1/2).*?(?=\\n0/2)", son1)
            try:    
                CifteSans_1_2 = CifteSans_1_2.group()
                CifteSans_1_2_.append(CifteSans_1_2)
            except:
                CifteSans_1_2_.append('basket')

            CifteSans_0_2 = re.search("(?<=\\n0/2).*?(?=\\n\\n\\nİlk Yarı)", son1)
            try:
                CifteSans_0_2 = CifteSans_0_2.group()
                CifteSans_0_2_.append(CifteSans_0_2)
            except:
                CifteSans_0_2_.append('Basket')

            Ilk_Yari_CifteSans_10 = re.search("(?<=\\nİlk Yarı Çifte Şans\\n[0-9]\\n1/X).*?(?=\\n1/2)", son1)
            try:
                Ilk_Yari_CifteSans_10 = Ilk_Yari_CifteSans_10.group()
                Ilk_Yari_CifteSans_10_.append(Ilk_Yari_CifteSans_10)
            except:
                Ilk_Yari_CifteSans_10_.append('Basket')

            Ilk_Yari_CifteSans_12 = re.search("(?<=\\nİlk Yarı Çifte Şans\\n[0-9]\\n1/X(-|\d+(?:\.\d+)?)\\n1/2).*?(?=\\n0/2)", son1)
            try:
                Ilk_Yari_CifteSans_12 = Ilk_Yari_CifteSans_12.group()
                Ilk_Yari_CifteSans_12_.append(Ilk_Yari_CifteSans_12)
            except:
                Ilk_Yari_CifteSans_12_.append('Basket')

            Ilk_Yari_CifteSans_02 = re.search("(?<=\\nİlk Yarı Çifte Şans\\n[0-9]\\n1/X(-|\d+(?:\.\d+)?)\\n1/2(-|\d+(?:\.\d+)?)\\n0/2).*?(?=\\n\\n\\nİlk Yarı Sonucu)", son1)
            try:
                Ilk_Yari_CifteSans_02 = Ilk_Yari_CifteSans_02.group()
                Ilk_Yari_CifteSans_02_.append(Ilk_Yari_CifteSans_02)
            except:
                Ilk_Yari_CifteSans_02_.append('Basket')

            Ilk_Yari_Sonucu_1 = re.search("(?<=\\n\\n\\nİlk Yarı Sonucu\\n[0-9]\\n1).*?(?=\\n0)", son1)
            try:
                Ilk_Yari_Sonucu_1 = Ilk_Yari_Sonucu_1.group()
                Ilk_Yari_Sonucu_1_.append(Ilk_Yari_Sonucu_1)
            except:
                Ilk_Yari_Sonucu_1_.append('Basket')

            Ilk_Yari_Sonucu_0 = re.search("(?<=\\n\\n\\nİlk Yarı Sonucu\\n[0-9]\\n1(-|\d+(?:\.\d+)?)\\n[0-9]).*?(?=\\n2)", son1)
            try:
                Ilk_Yari_Sonucu_0 = Ilk_Yari_Sonucu_0.group()
                Ilk_Yari_Sonucu_0_.append(Ilk_Yari_Sonucu_0)
            except:
                Ilk_Yari_Sonucu_0_.append('Basket')

            Ilk_Yari_Sonucu_2 = re.search("(?<=\\n\\n\\nİlk Yarı Sonucu\\n[0-9]\\n1(-|\d+(?:\.\d+)?)\\n[0-9](-|\d+(?:\.\d+)?)\\n[0-9]).*?(?=\\n\\n\\nİkinci Yarı Sonucu)", son1)
            try:
                Ilk_Yari_Sonucu_2 = Ilk_Yari_Sonucu_2.group()
                Ilk_Yari_Sonucu_2_.append(Ilk_Yari_Sonucu_2)
            except:
                Ilk_Yari_Sonucu_2_.append('Basket')
    
            Ikinci_Yari_Sonucu_1 = re.search("(?<=\\n\\n\\nİkinci Yarı Sonucu\\n[0-9]\\n1).*?(?=\\n0)", son1)
            try:
                Ikinci_Yari_Sonucu_1 = Ikinci_Yari_Sonucu_1.group()
                Ikinci_Yari_Sonucu_1_.append(Ikinci_Yari_Sonucu_1)
            except:
                Ikinci_Yari_Sonucu_1_.append('Basket')

            Ikinci_Yari_Sonucu_0 = re.search("(?<=\\n\\n\\nİkinci Yarı Sonucu\\n[0-9]\\n1(-|\d+(?:\.\d+)?)\\n0).*?(?=\\n2)", son1)
            try:
                Ikinci_Yari_Sonucu_0 = Ikinci_Yari_Sonucu_0.group()
                Ikinci_Yari_Sonucu_0_.append(Ikinci_Yari_Sonucu_0)
            except:
                Ikinci_Yari_Sonucu_0_.append('Basket')

            Ikinci_Yari_Sonucu_2 = re.search("(?<=\\n\\n\\nİkinci Yarı Sonucu\\n[0-9]\\n1(-|\d+(?:\.\d+)?)\\n0(-|\d+(?:\.\d+)?)\\n2).*?(?=\\n\\n\\nİlk Yarı)", son1)
            try:
                Ikinci_Yari_Sonucu_2 = Ikinci_Yari_Sonucu_2.group()
                Ikinci_Yari_Sonucu_2_.append(Ikinci_Yari_Sonucu_2)
            except:
                Ikinci_Yari_Sonucu_2_.append('Basket')

            Ilk_Yari_15_Alt = re.search("(?<=\\n\\n\\nİlk Yarı 1.5 Altı/Üstü\\n[0-9]\\nAlt).*?(?=\\nÜst)", son1)
            try:
                Ilk_Yari_15_Alt = Ilk_Yari_15_Alt.group()
                Ilk_Yari_15_Alt_.append(Ilk_Yari_15_Alt)
            except:
                Ilk_Yari_15_Alt_.append('Basket')

            Ilk_Yari_15_Ust = re.search("(?<=\\n\\n\\nİlk Yarı 1.5 Altı/Üstü\\n[0-9]\\nAlt(-|\d+(?:\.\d+)?)\\nÜst).*?(?=\\n\\n\\n1.5 Altı/Üstü)", son1)
            try:
                Ilk_Yari_15_Ust = Ilk_Yari_15_Ust.group()
                Ilk_Yari_15_Ust_.append(Ilk_Yari_15_Ust)
            except:
                Ilk_Yari_15_Ust_.append('Basket')

            MS_15_Alt = re.search("(?<=\\n\\n\\n1.5 Altı/Üstü\\n[0-9]\\nAlt).*?(?=\\nÜst)", son1)
            try:
                MS_15_Alt = MS_15_Alt.group()
                MS_15_Alt_.append(MS_15_Alt)
            except:
                MS_15_Alt_.append('Basket')

            MS_15_Ust = re.search("(?<=\\n\\n\\n1.5 Altı/Üstü\\n[0-9]\\nAlt(-|\d+(?:\.\d+)?)\\nÜst).*?(?=\\n\\n\\n3.5 Altı/Üstü)", son1)
            try:
                MS_15_Ust = MS_15_Ust.group()
                MS_15_Ust_.append(MS_15_Ust)
            except:
                MS_15_Ust_.append('Basket')

            MS_35_Alt = re.search("(?<=\\n\\n\\n3.5 Altı/Üstü\\n[0-9]\\nAlt).*?(?=\\nÜst)", son1)
            try:
                MS_35_Alt = MS_35_Alt.group()
                MS_35_Alt_.append(MS_35_Alt)
            except:
                MS_35_Alt_.append('Basket')
            
            MS_35_Ust = re.search("(?<=\\n\\n\\n3.5 Altı/Üstü\\n[0-9]\\nAlt(-|\d+(?:\.\d+)?)\\nÜst).*?(?=\\n\\n\\nTek / Çift)", son1)
            try:
                MS_35_Ust = MS_35_Ust.group()
                MS_35_Ust_.append(MS_35_Ust)
            except:
                MS_35_Ust_.append('Basket')

            MS_Tek = re.search("(?<=\\n\\n\\nTek / Çift\\n[0-9]\\nTek).*?(?=\\nÇift)", son1)
            try:
                MS_Tek = MS_Tek.group()
                MS_Tek_.append(MS_Tek)
            except:
                MS_Tek_.append('Basket')

            MS_Cift = re.search("(?<=\\n\\n\\nTek / Çift\\n[0-9]\\nTek(-|\d+(?:\.\d+)?)\\nÇift).*?(?=\\n\\n\\nToplam Gol)", son1)
            try:
                MS_Cift = MS_Cift.group()
                MS_Cift_.append(MS_Cift)
            except:
                MS_Cift_.append('Basket')

            Toplam_Gol_0_1 = re.search("(?<=\\n\\n\\nToplam Gol\\n[0-9]\\n0-1).*?(?=\\n2-3)", son1)
            try:
                Toplam_Gol_0_1 = Toplam_Gol_0_1.group()
                Toplam_Gol_0_1_.append(Toplam_Gol_0_1)
            except:
                Toplam_Gol_0_1_.append('Basket')

            Toplam_Gol_2_3 = re.search("(?<=\\n2-3).*?(?=\\n4-5)", son1)
            try:
                Toplam_Gol_2_3 = Toplam_Gol_2_3.group()
                Toplam_Gol_2_3_.append(Toplam_Gol_2_3)
            except:
                Toplam_Gol_2_3_.append('Basket')

            Toplam_Gol_4_5 = re.search("(?<=\\n4-5).*?(?=\\n6\+)", son1)
            try:
                Toplam_Gol_4_5 = Toplam_Gol_4_5.group()
                Toplam_Gol_4_5_.append(Toplam_Gol_4_5)
            except:
                Toplam_Gol_4_5_.append('Basket')

            Toplam_Gol_6_a = re.search("(?<=\\n6\++\s).*?(?=\\n\\n\\n İlk Yarı / Maç Sonuc)", son1) #burada bir boşluk hatası olabilir
            try:
                Toplam_Gol_6_a = Toplam_Gol_6_a.group()
                Toplam_Gol_6_a_.append(Toplam_Gol_6_a)
            except:
                Toplam_Gol_6_a_.append('Basket')

            IlkYari_MacSonucu_1_1 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1).*?(?=\\n1/0)", son1)
            try:
                IlkYari_MacSonucu_1_1 = IlkYari_MacSonucu_1_1.group()
                IlkYari_MacSonucu_1_1_.append(IlkYari_MacSonucu_1_1)
            except:
                IlkYari_MacSonucu_1_1_.append('Basket')

            IlkYari_MacSonucu_1_0 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0).*?(?=\\n1/2)", son1)
            try:
                IlkYari_MacSonucu_1_0 = IlkYari_MacSonucu_1_0.group()
                IlkYari_MacSonucu_1_0_.append(IlkYari_MacSonucu_1_0)
            except:
                IlkYari_MacSonucu_1_0_.append('basket')

            IlkYari_MacSonucu_1_2 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0(-|\d+(?:\.\d+)?)\\n1/2).*?(?=\\n0/1)", son1)
            try:
                IlkYari_MacSonucu_1_2 = IlkYari_MacSonucu_1_2.group()
                IlkYari_MacSonucu_1_2_.append(IlkYari_MacSonucu_1_2)
            except:
                IlkYari_MacSonucu_1_2_.append('Basket')

            IlkYari_MacSonucu_0_1 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0(-|\d+(?:\.\d+)?)\\n1/2(-|\d+(?:\.\d+)?)\\n0/1).*?(?=\\n0/0)", son1)
            try:
                IlkYari_MacSonucu_0_1 = IlkYari_MacSonucu_0_1.group()
                IlkYari_MacSonucu_0_1_.append(IlkYari_MacSonucu_0_1)
            except:
                IlkYari_MacSonucu_0_1_.append('Basket')

            IlkYari_MacSonucu_0_0 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0(-|\d+(?:\.\d+)?)\\n1/2(-|\d+(?:\.\d+)?)\\n0/1(-|\d+(?:\.\d+)?)\\n0/0).*?(?=\\n0/2)", son1)
            try:
                IlkYari_MacSonucu_0_0 = IlkYari_MacSonucu_0_0.group()
                IlkYari_MacSonucu_0_0_.append(IlkYari_MacSonucu_0_0)
            except:
                IlkYari_MacSonucu_0_0_.append('Basket')

            IlkYari_MacSonucu_0_2 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0(-|\d+(?:\.\d+)?)\\n1/2(-|\d+(?:\.\d+)?)\\n0/1(-|\d+(?:\.\d+)?)\\n0/0(-|\d+(?:\.\d+)?)\\n0/2).*?(?=\\n2/1)", son1)
            try:
                IlkYari_MacSonucu_0_2 = IlkYari_MacSonucu_0_2.group()
                IlkYari_MacSonucu_0_2_.append(IlkYari_MacSonucu_0_2)
            except:
                IlkYari_MacSonucu_0_2_.append('Basket')

            IlkYari_MacSonucu_2_1 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0(-|\d+(?:\.\d+)?)\\n1/2(-|\d+(?:\.\d+)?)\\n0/1(-|\d+(?:\.\d+)?)\\n0/0(-|\d+(?:\.\d+)?)\\n0/2(-|\d+(?:\.\d+)?)\\n2/1).*?(?=\\n2/0)", son1)
            try:
                IlkYari_MacSonucu_2_1 = IlkYari_MacSonucu_2_1.group()
                IlkYari_MacSonucu_2_1_.append(IlkYari_MacSonucu_2_1)
            except:
                IlkYari_MacSonucu_2_1_.append('Basket')

            IlkYari_MacSonucu_2_0 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0(-|\d+(?:\.\d+)?)\\n1/2(-|\d+(?:\.\d+)?)\\n0/1(-|\d+(?:\.\d+)?)\\n0/0(-|\d+(?:\.\d+)?)\\n0/2(-|\d+(?:\.\d+)?)\\n2/1(-|\d+(?:\.\d+)?)\\n2/0).*?(?=\\n2/2)", son1)
            try:
                IlkYari_MacSonucu_2_0 = IlkYari_MacSonucu_2_0.group()
                IlkYari_MacSonucu_2_0_.append(IlkYari_MacSonucu_2_0)
            except:
                IlkYari_MacSonucu_2_0_.append('Basket')

            IlkYari_MacSonucu_2_2 = re.search("(?<=\\n\\n\\n İlk Yarı / Maç Sonucu\\n[0-9]\\n1/1(-|\d+(?:\.\d+)?)\\n1/0(-|\d+(?:\.\d+)?)\\n1/2(-|\d+(?:\.\d+)?)\\n0/1(-|\d+(?:\.\d+)?)\\n0/0(-|\d+(?:\.\d+)?)\\n0/2(-|\d+(?:\.\d+)?)\\n2/1(-|\d+(?:\.\d+)?)\\n2/0(-|\d+(?:\.\d+)?)\\n2/2).*?(?=\\n\\n\\n Maç Skoru)", son1)
            try:
                IlkYari_MacSonucu_2_2 = IlkYari_MacSonucu_2_2.group()
                IlkYari_MacSonucu_2_2_.append(IlkYari_MacSonucu_2_2)
            except:
                IlkYari_MacSonucu_2_2_.append('Basket')

            MacSkoru_1__1_0 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0).*?(?=2-0)", son1)
            try:
                MacSkoru_1__1_0 = MacSkoru_1__1_0.group()
                MacSkoru_1__1_0_.append(MacSkoru_1__1_0)
            except:
                MacSkoru_1__1_0_.append('Basket')

            MacSkoru_1__2_0 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0).*?(?=3-0)", son1)
            try:
                MacSkoru_1__2_0 = MacSkoru_1__2_0.group()
                MacSkoru_1__2_0_.append(MacSkoru_1__2_0)
            except:
                MacSkoru_1__2_0_.append('Basket')

            MacSkoru_1__3_0 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0).*?(?=4-0)", son1)
            try:
                MacSkoru_1__3_0 = MacSkoru_1__3_0.group()
                MacSkoru_1__3_0_.append(MacSkoru_1__3_0)
            except:
                MacSkoru_1__3_0_.append('Basket')

            MacSkoru_1__4_0 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0).*?(?=5-0)", son1)
            try:
                MacSkoru_1__4_0 = MacSkoru_1__4_0.group()
                MacSkoru_1__4_0_.append(MacSkoru_1__4_0)
            except:
                MacSkoru_1__4_0_.append('Basket')
            
            MacSkoru_1__5_0 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0).*?(?=2-1)", son1)
            try:
                MacSkoru_1__5_0 = MacSkoru_1__5_0.group()
                MacSkoru_1__5_0_.append(MacSkoru_1__5_0)
            except:
                MacSkoru_1__5_0_.append('Basket')

            MacSkoru_1__2_1 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1).*?(?=3-1)", son1)
            try:
                MacSkoru_1__2_1 = MacSkoru_1__2_1.group()
                MacSkoru_1__2_1_.append(MacSkoru_1__2_1)
            except:
                MacSkoru_1__2_1_.append('Basket')

            MacSkoru_1__3_1 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1).*?(?=4-1)", son1)
            try:
                MacSkoru_1__3_1 = MacSkoru_1__3_1.group()
                MacSkoru_1__3_1_.append(MacSkoru_1__3_1)
            except:
                MacSkoru_1__3_1_.append('Basket')

            MacSkoru_1__4_1 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1).*?(?=5-1)", son1)
            try:
                MacSkoru_1__4_1 = MacSkoru_1__4_1.group()
                MacSkoru_1__4_1_.append(MacSkoru_1__4_1)
            except:
                MacSkoru_1__4_1_.append('Basket')

            MacSkoru_1__5_1 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1(-|\d+(?:\.\d+)?)5-1).*?(?=3-2)", son1)
            try:
                MacSkoru_1__5_1 = MacSkoru_1__5_1.group()
                MacSkoru_1__5_1_.append(MacSkoru_1__5_1)
            except:
                MacSkoru_1__5_1_.append('basket')

            MacSkoru_1__3_2 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1(-|\d+(?:\.\d+)?)5-1(-|\d+(?:\.\d+)?)3-2).*?(?=4-2)", son1)
            try:
                MacSkoru_1__3_2 = MacSkoru_1__3_2.group()
                MacSkoru_1__3_2_.append(MacSkoru_1__3_2)
            except:
                MacSkoru_1__3_2_.append('Basket')

            MacSkoru_1__4_2 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1(-|\d+(?:\.\d+)?)5-1(-|\d+(?:\.\d+)?)3-2(-|\d+(?:\.\d+)?)4-2).*?(?=5-2)", son1)
            try:
                MacSkoru_1__4_2 = MacSkoru_1__4_2.group()
                MacSkoru_1__4_2_.append(MacSkoru_1__4_2)
            except:
                MacSkoru_1__4_2_.append('Basket')

            MacSkoru_1__5_2 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1(-|\d+(?:\.\d+)?)5-1(-|\d+(?:\.\d+)?)3-2(-|\d+(?:\.\d+)?)4-2(-|\d+(?:\.\d+)?)5-2).*?(?=4-3)", son1)
            try:
                MacSkoru_1__5_2 = MacSkoru_1__5_2.group()
                MacSkoru_1__5_2_.append(MacSkoru_1__5_2)
            except:
                MacSkoru_1__5_2_.append('Basket')

            MacSkoru_1__4_3 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1(-|\d+(?:\.\d+)?)5-1(-|\d+(?:\.\d+)?)3-2(-|\d+(?:\.\d+)?)4-2(-|\d+(?:\.\d+)?)5-2(-|\d+(?:\.\d+)?)4-3).*?(?=5-3)", son1)
            try:
                MacSkoru_1__4_3 = MacSkoru_1__4_3.group()
                MacSkoru_1__4_3_.append(MacSkoru_1__4_3)
            except:
                MacSkoru_1__4_3_.append('Basket')

            MacSkoru_1__5_3 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1(-|\d+(?:\.\d+)?)5-1(-|\d+(?:\.\d+)?)3-2(-|\d+(?:\.\d+)?)4-2(-|\d+(?:\.\d+)?)5-2(-|\d+(?:\.\d+)?)4-3(-|\d+(?:\.\d+)?)5-3).*?(?=5-4)", son1)
            try:
                MacSkoru_1__5_3 = MacSkoru_1__5_3.group()
                MacSkoru_1__5_3_.append(MacSkoru_1__5_3)
            except:
                MacSkoru_1__5_3_.append('Basket')

            MacSkoru_1__5_4 = re.search("(?<=\\n\\n\\n Maç Skoru\\n 1\\n[0-9]\\n1-0(-|\d+(?:\.\d+)?)2-0(-|\d+(?:\.\d+)?)3-0(-|\d+(?:\.\d+)?)4-0(-|\d+(?:\.\d+)?)5-0(-|\d+(?:\.\d+)?)2-1(-|\d+(?:\.\d+)?)3-1(-|\d+(?:\.\d+)?)4-1(-|\d+(?:\.\d+)?)5-1(-|\d+(?:\.\d+)?)3-2(-|\d+(?:\.\d+)?)4-2(-|\d+(?:\.\d+)?)5-2(-|\d+(?:\.\d+)?)4-3(-|\d+(?:\.\d+)?)5-3(-|\d+(?:\.\d+)?)5-4).*?(?=\\n)", son1)
            try:
                MacSkoru_1__5_4 = MacSkoru_1__5_4.group()
                MacSkoru_1__5_4_.append(MacSkoru_1__5_4)
            except:
                MacSkoru_1__5_4_.append('Basket')

            MacSkoru_0__0_0 = re.search("(?<=\\n0-0).*?(?=1-1)", son1)
            try:
                MacSkoru_0__0_0 = MacSkoru_0__0_0.group()
                MacSkoru_0__0_0_.append(MacSkoru_0__0_0)
            except:
                MacSkoru_0__0_0_.append('Basket')

            MacSkoru_0__1_1 = re.search("(?<=\\n0-0(-|\d+(?:\.\d+)?)1-1).*?(?=2-2)", son1)
            try:
                MacSkoru_0__1_1 = MacSkoru_0__1_1.group()
                MacSkoru_0__1_1_.append(MacSkoru_0__1_1)
            except:
                MacSkoru_0__1_1_.append('Basket')

            MacSkoru_0__2_2 = re.search("(?<=\\n0-0(-|\d+(?:\.\d+)?)1-1(-|\d+(?:\.\d+)?)2-2).*?(?=3-3)", son1)
            try:
                MacSkoru_0__2_2 = MacSkoru_0__2_2.group()
                MacSkoru_0__2_2_.append(MacSkoru_0__2_2)
            except:
                MacSkoru_0__2_2_.append('Basket')

            MacSkoru_0__3_3 = re.search("(?<=\\n0-0(-|\d+(?:\.\d+)?)1-1(-|\d+(?:\.\d+)?)2-2(-|\d+(?:\.\d+)?)3-3).*?(?=4-4)", son1)
            try:
                MacSkoru_0__3_3 = MacSkoru_0__3_3.group()
                MacSkoru_0__3_3_.append(MacSkoru_0__3_3)
            except:
                MacSkoru_0__3_3_.append('Basket')

            MacSkoru_0__4_4 = re.search("(?<=\\n0-0(-|\d+(?:\.\d+)?)1-1(-|\d+(?:\.\d+)?)2-2(-|\d+(?:\.\d+)?)3-3(-|\d+(?:\.\d+)?)4-4).*?(?=5-5)", son1)
            try:
                MacSkoru_0__4_4 = MacSkoru_0__4_4.group()
                MacSkoru_0__4_4_.append(MacSkoru_0__4_4)
            except:
                MacSkoru_0__4_4_.append('Basket')

            MacSkoru_0__5_5 = re.search("(?<=\\n0-0(-|\d+(?:\.\d+)?)1-1(-|\d+(?:\.\d+)?)2-2(-|\d+(?:\.\d+)?)3-3(-|\d+(?:\.\d+)?)4-4(-|\d+(?:\.\d+)?)5-5).*?(?=\\n)", son1)
            try:
                MacSkoru_0__5_5 = MacSkoru_0__5_5.group()
                MacSkoru_0__5_5_.append(MacSkoru_0__5_5)
            except:
                MacSkoru_0__5_5_.append('Basket')

            MacSkoru_2__0_1 = re.search("(?<=\\xa0\\n0-1).*?(?=0-2)", son1)
            try:
                MacSkoru_2__0_1 = MacSkoru_2__0_1.group()
                MacSkoru_2__0_1_.append(MacSkoru_2__0_1)
            except:
                MacSkoru_2__0_1_.append('Basket')

            MacSkoru_2__0_2 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2).*?(?=0-3)", son1)
            try:
                MacSkoru_2__0_2 = MacSkoru_2__0_2.group()
                MacSkoru_2__0_2_.append(MacSkoru_2__0_2)
            except:
                MacSkoru_2__0_2_.append('Basket')

            MacSkoru_2__0_3 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3).*?(?=0-4)", son1)
            try:
                MacSkoru_2__0_3 = MacSkoru_2__0_3.group()
                MacSkoru_2__0_3_.append(MacSkoru_2__0_3)
            except:
                MacSkoru_2__0_3_.append('Basket')

            MacSkoru_2__0_4 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4).*?(?=0-5)", son1)
            try:
                MacSkoru_2__0_4 = MacSkoru_2__0_4.group()
                MacSkoru_2__0_4_.append(MacSkoru_2__0_4)
            except:
                MacSkoru_2__0_4_.append('Basket')

            MacSkoru_2__0_5 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5).*?(?=1-2)", son1)
            try:
                MacSkoru_2__0_5 = MacSkoru_2__0_5.group()
                MacSkoru_2__0_5_.append(MacSkoru_2__0_5)
            except:
                MacSkoru_2__0_5_.append('Basket')

            MacSkoru_2__1_2 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2).*?(?=1-3)", son1)
            try:
                MacSkoru_2__1_2 = MacSkoru_2__1_2.group()
                MacSkoru_2__1_2_.append(MacSkoru_2__1_2)
            except:
                MacSkoru_2__1_2_.append('Basket')

            MacSkoru_2__1_3 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3).*?(?=1-4)", son1)
            try:
                MacSkoru_2__1_3 = MacSkoru_2__1_3.group()
                MacSkoru_2__1_3_.append(MacSkoru_2__1_3)
            except:
                MacSkoru_2__1_3_.append('Basket')

            MacSkoru_2__1_4 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4).*?(?=1-5)", son1)
            try:
                MacSkoru_2__1_4 = MacSkoru_2__1_4.group()
                MacSkoru_2__1_4_.append(MacSkoru_2__1_4)
            except:
                MacSkoru_2__1_4_.append('Basket')

            MacSkoru_2__1_5 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4(-|\d+(?:\.\d+)?)1-5).*?(?=2-3)", son1)
            try:
                MacSkoru_2__1_5 = MacSkoru_2__1_5.group()
                MacSkoru_2__1_5_.append(MacSkoru_2__1_5)
            except:
                MacSkoru_2__1_5_.append('Basket')

            MacSkoru_2__2_3 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4(-|\d+(?:\.\d+)?)1-5(-|\d+(?:\.\d+)?)2-3).*?(?=2-4)", son1)
            try:
                MacSkoru_2__2_3 = MacSkoru_2__2_3.group()
                MacSkoru_2__2_3_.append(MacSkoru_2__2_3)
            except:
                MacSkoru_2__2_3_.append('Basket')
            
            MacSkoru_2__2_4 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4(-|\d+(?:\.\d+)?)1-5(-|\d+(?:\.\d+)?)2-3(-|\d+(?:\.\d+)?)2-4).*?(?=2-5)", son1)
            try:
                MacSkoru_2__2_4 = MacSkoru_2__2_4.group()
                MacSkoru_2__2_4_.append(MacSkoru_2__2_4)
            except:
                MacSkoru_2__2_4_.append('Basket')

            MacSkoru_2__2_5 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4(-|\d+(?:\.\d+)?)1-5(-|\d+(?:\.\d+)?)2-3(-|\d+(?:\.\d+)?)2-4(-|\d+(?:\.\d+)?)2-5).*?(?=3-4)", son1)
            try:
                MacSkoru_2__2_5 = MacSkoru_2__2_5.group()
                MacSkoru_2__2_5_.append(MacSkoru_2__2_5)
            except:
                MacSkoru_2__2_5_.append('Basket')

            MacSkoru_2__3_4 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4(-|\d+(?:\.\d+)?)1-5(-|\d+(?:\.\d+)?)2-3(-|\d+(?:\.\d+)?)2-4(-|\d+(?:\.\d+)?)2-5(-|\d+(?:\.\d+)?)3-4).*?(?=3-5)", son1)
            try:
                MacSkoru_2__3_4 = MacSkoru_2__3_4.group()
                MacSkoru_2__3_4_.append(MacSkoru_2__3_4)
            except:
                MacSkoru_2__3_4_.append('Basket')

            MacSkoru_2__3_5 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4(-|\d+(?:\.\d+)?)1-5(-|\d+(?:\.\d+)?)2-3(-|\d+(?:\.\d+)?)2-4(-|\d+(?:\.\d+)?)2-5(-|\d+(?:\.\d+)?)3-4(-|\d+(?:\.\d+)?)3-5).*?(?=4-5)", son1)
            try:
                MacSkoru_2__3_5 = MacSkoru_2__3_5.group()
                MacSkoru_2__3_5_.append(MacSkoru_2__3_5)
            except:
                MacSkoru_2__3_5_.append('Basket')

            MacSkoru_2__4_5 = re.search("(?<=\\xa0\\n0-1(-|\d+(?:\.\d+)?)0-2(-|\d+(?:\.\d+)?)0-3(-|\d+(?:\.\d+)?)0-4(-|\d+(?:\.\d+)?)0-5(-|\d+(?:\.\d+)?)1-2(-|\d+(?:\.\d+)?)1-3(-|\d+(?:\.\d+)?)1-4(-|\d+(?:\.\d+)?)1-5(-|\d+(?:\.\d+)?)2-3(-|\d+(?:\.\d+)?)2-4(-|\d+(?:\.\d+)?)2-5(-|\d+(?:\.\d+)?)3-4(-|\d+(?:\.\d+)?)3-5(-|\d+(?:\.\d+)?)4-5).*?(?=\\n\\n\\n)", son1)
            try:
                MacSkoru_2__4_5 = MacSkoru_2__4_5.group()
                MacSkoru_2__4_5_.append(MacSkoru_2__4_5)
            except:
                MacSkoru_2__4_5_.append('Basket')

############################################################### ORAN KAZIMA DEVAM(ANA SAYFA) ######################################################################################
        
        Oranlar__Soup = soup.find_all("td", style="text-align:center;")
        Oranlar = []
        for sw in Oranlar__Soup:
            sreplace = sw.text
            Oranlar.append(sreplace)
        Karsilasma_Kontrol = CifteSans_1_0_ #uzunluk eşitleme
        
        sayac = 0
        indexsayac = 0
        
        Mac_Sonucu_1 = []
        Mac_Sonucu_0 = []
        Mac_Sonucu_2 = []
        Mac_S_2_5_Alt= []
        Mac_S_2_5_Ust= []
        Mac_S_KG_Var = []
        Mac_S_KG_Yok = []
        IlkYari_Gol_Var = []
        IlkYari_Gol_Yok = []
        Mac_S_1_5_Alt= []
        Mac_S_1_5_Ust= []

        for index, msbk in enumerate(Karsilasma_Kontrol): #Basket karşılamaları hariç tutma
            if msbk != 'Basket':
                indexsayac += 26
                Futbol_Oranlari = Oranlar[sayac:indexsayac]

                Mac_Sonucu_1.append(Futbol_Oranlari[2])
                Mac_Sonucu_0.append(Futbol_Oranlari[3])
                Mac_Sonucu_2.append(Futbol_Oranlari[4])
                Mac_S_2_5_Alt.append(Futbol_Oranlari[5])
                Mac_S_2_5_Ust.append(Futbol_Oranlari[6])
                Mac_S_KG_Var.append(Futbol_Oranlari[7])
                Mac_S_KG_Yok.append(Futbol_Oranlari[8])
                IlkYari_Gol_Var.append(Futbol_Oranlari[9])
                IlkYari_Gol_Yok.append(Futbol_Oranlari[10])
                Mac_S_1_5_Alt.append(Futbol_Oranlari[11])
                Mac_S_1_5_Ust.append(Futbol_Oranlari[12])

                sayac += 26

            if msbk == 'Basket':
                indexsayac += 24

                Mac_Sonucu_1.append(msbk)
                Mac_Sonucu_0.append(msbk)
                Mac_Sonucu_2.append(msbk)
                Mac_S_2_5_Alt.append(msbk)
                Mac_S_2_5_Ust.append(msbk)
                Mac_S_KG_Var.append(msbk)
                Mac_S_KG_Yok.append(msbk)
                IlkYari_Gol_Var.append(msbk)
                IlkYari_Gol_Yok.append(msbk)
                Mac_S_1_5_Alt.append(msbk)
                Mac_S_1_5_Ust.append(msbk)

                sayac += 24
        
        Futbol_Oranlari = flatten(Futbol_Oranlari)

        # TÜM ORANLARIN DERLENMESİ / VERİ SETİ ÖNCESİ HAZIRLIK
        df = [ZamanSerisiTS, MacSaati, Klasman, MBs, Evsahibi, MacSonucu, Deplasman, İlkYari,
              Mac_Sonucu_1, Mac_Sonucu_0, Mac_Sonucu_2,
              Mac_S_2_5_Alt, Mac_S_2_5_Ust,
              Mac_S_KG_Var, Mac_S_KG_Yok,
              IlkYari_Gol_Var, IlkYari_Gol_Yok,
              Mac_S_1_5_Alt, Mac_S_1_5_Ust,
              CifteSans_1_0_, CifteSans_1_2_, CifteSans_0_2_,
              Ilk_Yari_CifteSans_10_, Ilk_Yari_CifteSans_12_, Ilk_Yari_CifteSans_02_,
              Ilk_Yari_Sonucu_1_, Ilk_Yari_Sonucu_0_, Ilk_Yari_Sonucu_2_,
              Ikinci_Yari_Sonucu_1_, Ikinci_Yari_Sonucu_0_, Ikinci_Yari_Sonucu_2_,
              Ilk_Yari_15_Alt_, Ilk_Yari_15_Ust_,
              MS_15_Alt_, MS_15_Ust_,
              MS_35_Alt_, MS_35_Ust_,
              MS_Tek_, MS_Cift_,
              Toplam_Gol_0_1_, Toplam_Gol_2_3_, Toplam_Gol_4_5_, Toplam_Gol_6_a_,
              IlkYari_MacSonucu_1_1_, IlkYari_MacSonucu_1_0_, IlkYari_MacSonucu_1_2_, IlkYari_MacSonucu_0_1_, IlkYari_MacSonucu_0_0_, IlkYari_MacSonucu_0_2_, IlkYari_MacSonucu_2_1_, IlkYari_MacSonucu_2_0_, IlkYari_MacSonucu_2_2_,
              MacSkoru_1__1_0_, MacSkoru_1__2_0_, MacSkoru_1__3_0_, MacSkoru_1__4_0_, MacSkoru_1__5_0_, MacSkoru_1__2_1_, MacSkoru_1__3_1_, MacSkoru_1__4_1_, MacSkoru_1__5_1_, MacSkoru_1__3_2_, MacSkoru_1__4_2_, MacSkoru_1__5_2_, MacSkoru_1__4_3_, MacSkoru_1__5_3_, MacSkoru_1__5_4_,
              MacSkoru_0__0_0_, MacSkoru_0__1_1_, MacSkoru_0__2_2_, MacSkoru_0__3_3_, MacSkoru_0__4_4_, MacSkoru_0__5_5_,
              MacSkoru_2__0_1_, MacSkoru_2__0_2_, MacSkoru_2__0_3_, MacSkoru_2__0_4_, MacSkoru_2__0_5_, MacSkoru_2__1_2_, MacSkoru_2__1_3_, MacSkoru_2__1_4_, MacSkoru_2__1_5_, MacSkoru_2__2_3_, MacSkoru_2__2_4_, MacSkoru_2__2_5_, MacSkoru_2__3_4_, MacSkoru_2__3_5_, MacSkoru_2__4_5_]

################################################################# TABLOLAŞTIRMA ######################################################################################

        ColumName = ['ZamanSerisiTS', 'MacSaati', 'Klasman', 'MBs', 'Evsahibi', 'MacSonucu', 'Deplasman', 'İlkYari', 
                     'Mac_Sonucu_1', 'Mac_Sonucu_0', 'Mac_Sonucu_2', 
                     'Mac_S_2_5_Alt', 'Mac_S_2_5_Ust', 
                     'Mac_S_KG_Var', 'Mac_S_KG_Yok', 
                     'IlkYari_Gol_Var', 'IlkYari_Gol_Yok', 
                     'Mac_S_1_5_Alt', 'Mac_S_1_5_Ust', 
                     'CifteSans_1_0_', 'CifteSans_1_2_', 'CifteSans_0_2_', 
                     'Ilk_Yari_CifteSans_10_', 'Ilk_Yari_CifteSans_12_', 'Ilk_Yari_CifteSans_02_', 
                     'Ilk_Yari_Sonucu_1_', 'Ilk_Yari_Sonucu_0_', 'Ilk_Yari_Sonucu_2_', 
                     'Ikinci_Yari_Sonucu_1_', 'Ikinci_Yari_Sonucu_0_', 'Ikinci_Yari_Sonucu_2_', 
                     'Ilk_Yari_15_Alt_', 'Ilk_Yari_15_Ust_', 
                     'MS_15_Alt_', 'MS_15_Ust_', 
                     'MS_35_Alt_', 'MS_35_Ust_', 
                     'MS_Tek_', 'MS_Cift_', 
                     'Toplam_Gol_0_1_', 'Toplam_Gol_2_3_', 'Toplam_Gol_4_5_', 'Toplam_Gol_6_a_', 
                     'IlkYari_MacSonucu_1_1_', 'IlkYari_MacSonucu_1_0_', 'IlkYari_MacSonucu_1_2_', 'IlkYari_MacSonucu_0_1_', 'IlkYari_MacSonucu_0_0_', 'IlkYari_MacSonucu_0_2_', 'IlkYari_MacSonucu_2_1_', 'IlkYari_MacSonucu_2_0_', 'IlkYari_MacSonucu_2_2_', 
                     'MacSkoru_1__1_0_', 'MacSkoru_1__2_0_', 'MacSkoru_1__3_0_', 'MacSkoru_1__4_0_', 'MacSkoru_1__5_0_', 'MacSkoru_1__2_1_', 'MacSkoru_1__3_1_', 'MacSkoru_1__4_1_', 'MacSkoru_1__5_1_', 'MacSkoru_1__3_2_', 'MacSkoru_1__4_2_', 'MacSkoru_1__5_2_', 'MacSkoru_1__4_3_', 'MacSkoru_1__5_3_', 'MacSkoru_1__5_4_', 
                     'MacSkoru_0__0_0_', 'MacSkoru_0__1_1_', 'MacSkoru_0__2_2_', 'MacSkoru_0__3_3_', 'MacSkoru_0__4_4_', 'MacSkoru_0__5_5_', 
                     'MacSkoru_2__0_1_', 'MacSkoru_2__0_2_', 'MacSkoru_2__0_3_', 'MacSkoru_2__0_4_', 'MacSkoru_2__0_5_', 'MacSkoru_2__1_2_', 'MacSkoru_2__1_3_', 'MacSkoru_2__1_4_', 'MacSkoru_2__1_5_', 'MacSkoru_2__2_3_', 'MacSkoru_2__2_4_', 'MacSkoru_2__2_5_', 'MacSkoru_2__3_4_', 'MacSkoru_2__3_5_', 'MacSkoru_2__4_5_']

        df2=DataFrame()
        for indx, cc in enumerate(df):
            st=DataFrame(data=cc,index=range(len(cc)),columns=[indx])
            df2=concat([df2, st],axis=1)

        df2 = df2.set_axis(ColumName, axis=1, inplace=False)
        df2 = df2[~df2['Mac_Sonucu_1'].isin(['Basket'])]
        df2=df2.rename(index={j: i for i, j in enumerate(df2.index)})

        sonuc = df2['MacSonucu']
        ilkyari = df2['İlkYari']

        EvSahibi_Skor = []
        for x in sonuc:
            ev = re.match(".+-",x)
            if ev:
                ev = ev.group()
                EvSahibi_Skor.append(ev[0])
            else:
                EvSahibi_Skor.append('Bekle')
        
        Deplasman_Skor = []
        for y in sonuc:
            dep = re.search("-+[0-9]",y)
            if dep:
                dep = dep.group()
                Deplasman_Skor.append(dep[1])
            else:
                Deplasman_Skor.append('Bekle')

        EvSahibi_İlkYari_Skor = []
        for xilk in ilkyari:
            evilk = re.match(".+-",xilk)
            if evilk:
                evilk = evilk.group()
                EvSahibi_İlkYari_Skor.append(evilk[0])
            else:
                EvSahibi_İlkYari_Skor.append('Bekle')
        
        Deplasman_İlkYari_Skor = []
        for yilk in ilkyari:
            depilk = re.search("-+[0-9]",yilk)
            if depilk:
                depilk = depilk.group()
                Deplasman_İlkYari_Skor.append(depilk[1])
            else:
                Deplasman_İlkYari_Skor.append('Bekle')

        EvSahibi_Skor=DataFrame(data=EvSahibi_Skor,index=range(len(EvSahibi_Skor)),columns=["EvSahibi_Skor"])
        Deplasman_Skor=DataFrame(data=Deplasman_Skor,index=range(len(Deplasman_Skor)),columns=["Deplasman_Skor"])
        EvSahibi_İlkYari_Skor=DataFrame(data=EvSahibi_İlkYari_Skor,index=range(len(EvSahibi_İlkYari_Skor)),columns=["EvSahibi_İlkYari_Skor"])
        Deplasman_İlkYari_Skor=DataFrame(data=Deplasman_İlkYari_Skor,index=range(len(Deplasman_İlkYari_Skor)),columns=["Deplasman_İlkYari_Skor"])
        df2=concat([EvSahibi_Skor, Deplasman_Skor, EvSahibi_İlkYari_Skor, Deplasman_İlkYari_Skor, df2],axis=1)


##########################################################################################################################################################
######################################################## KAZANAN ORANLARIN İŞARETLENMESİ [] ###############################################################
##########################################################################################################################################################

        def Mac_Sonucu_1(x, y, z):
            if z == "" or x == 'Bekle':
                return z
            elif x > y:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_Sonucu_1'] = df2.apply(lambda x: Mac_Sonucu_1(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_Sonucu_1']), axis=1)

##########################################################################################################################################################

        def Mac_Sonucu_0(x, y, z):
            if z == "" or x == 'Bekle':
                return z
            elif x == y:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_Sonucu_0'] = df2.apply(lambda x: Mac_Sonucu_0(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_Sonucu_0']), axis=1)
        
##########################################################################################################################################################

        def Mac_Sonucu_2(x, y, z):
            if z == "" or x == 'Bekle':
                return z
            elif x < y:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_Sonucu_2'] = df2.apply(lambda x: Mac_Sonucu_2(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_Sonucu_2']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_2_5_Alt(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E': # E sonradan çıkan hata geçici bloke edildi 
                return z
            elif int(x)+int(y) < 3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_S_2_5_Alt'] = df2.apply(lambda x: Mac_S_2_5_Alt(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_S_2_5_Alt']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_2_5_Ust(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E':
                return z
            elif int(x)+int(y) >= 3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_S_2_5_Ust'] = df2.apply(lambda x: Mac_S_2_5_Ust(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_S_2_5_Ust']), axis=1)        
        
##########################################################################################################################################################


        def Mac_S_KG_Var(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E':
                return z
            elif int(x) and int(y) > 0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_S_KG_Var'] = df2.apply(lambda x: Mac_S_KG_Var(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_S_KG_Var']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_KG_Yok(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E':
                return z
            elif int(x) == 0 or int(y) == 0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_S_KG_Yok'] = df2.apply(lambda x: Mac_S_KG_Yok(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_S_KG_Yok']), axis=1)        
        
##########################################################################################################################################################

        def IlkYari_Gol_Var(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E':
                return z
            elif int(x) + int(y) > 0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_Gol_Var'] = df2.apply(lambda x: IlkYari_Gol_Var(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_Gol_Var']), axis=1)        
        
##########################################################################################################################################################

        def IlkYari_Gol_Yok(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E':
                return z
            elif int(x) + int(y) == 0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_Gol_Yok'] = df2.apply(lambda x: IlkYari_Gol_Yok(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_Gol_Yok']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_1_5_Alt(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E':
                return z
            elif int(x) + int(y) < 2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_S_1_5_Alt'] = df2.apply(lambda x: Mac_S_1_5_Alt(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_S_1_5_Alt']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_1_5_Ust(x, y, z):
            if z == "" or x == 'Bekle'or x == 'E':
                return z
            elif int(x) + int(y) >= 2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Mac_S_1_5_Ust'] = df2.apply(lambda x: Mac_S_1_5_Ust(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Mac_S_1_5_Ust']), axis=1)        
        
##########################################################################################################################################################

        def CifteSans_1_0_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) >= int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['CifteSans_1_0_'] = df2.apply(lambda x: CifteSans_1_0_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['CifteSans_1_0_']), axis=1)        
        
##########################################################################################################################################################

        def CifteSans_1_2_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) != int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['CifteSans_1_2_'] = df2.apply(lambda x: CifteSans_1_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['CifteSans_1_2_']), axis=1)        
        
##########################################################################################################################################################

        def CifteSans_0_2_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) <= int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['CifteSans_0_2_'] = df2.apply(lambda x: CifteSans_0_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['CifteSans_0_2_']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_CifteSans_10_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) >= int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_CifteSans_10_'] = df2.apply(lambda x: Ilk_Yari_CifteSans_10_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_CifteSans_10_']), axis=1)        
        
##########################################################################################################################################################
    
        def Ilk_Yari_CifteSans_12_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) != int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_CifteSans_12_'] = df2.apply(lambda x: Ilk_Yari_CifteSans_12_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_CifteSans_12_']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_CifteSans_02_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) <= int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_CifteSans_02_'] = df2.apply(lambda x: Ilk_Yari_CifteSans_02_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_CifteSans_02_']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_Sonucu_1_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) > int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_Sonucu_1_'] = df2.apply(lambda x: Ilk_Yari_Sonucu_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_Sonucu_1_']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_Sonucu_0_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) == int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_Sonucu_0_'] = df2.apply(lambda x: Ilk_Yari_Sonucu_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_Sonucu_0_']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_Sonucu_2_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) < int(y):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_Sonucu_2_'] = df2.apply(lambda x: Ilk_Yari_Sonucu_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_Sonucu_2_']), axis=1)        
        
##########################################################################################################################################################

        def Ikinci_Yari_Sonucu_1_(xIlkyariEV, yIlkyariDEP, xMacsonucuEV, yMacsonucuDEP, z):
            if z == "" or xIlkyariEV == 'Bekle' or z == '-'or x == 'E':
                return z
            elif (int(xMacsonucuEV) - int(xIlkyariEV)) > (int(yMacsonucuDEP) - int(yIlkyariDEP)):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ikinci_Yari_Sonucu_1_'] = df2.apply(lambda x: Ikinci_Yari_Sonucu_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Ikinci_Yari_Sonucu_1_']), axis=1)        
        
##########################################################################################################################################################

        def Ikinci_Yari_Sonucu_0_(xIlkyariEV, yIlkyariDEP, xMacsonucuEV, yMacsonucuDEP, z):
            if z == "" or xIlkyariEV == 'Bekle' or z == '-'or x == 'E':
                return z
            elif (int(xMacsonucuEV) - int(xIlkyariEV)) == (int(yMacsonucuDEP) - int(yIlkyariDEP)):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ikinci_Yari_Sonucu_0_'] = df2.apply(lambda x: Ikinci_Yari_Sonucu_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Ikinci_Yari_Sonucu_0_']), axis=1)        
        
##########################################################################################################################################################

        def Ikinci_Yari_Sonucu_2_(xIlkyariEV, yIlkyariDEP, xMacsonucuEV, yMacsonucuDEP, z):
            if z == "" or xIlkyariEV == 'Bekle' or z == '-'or x == 'E':
                return z
            elif (int(xMacsonucuEV) - int(xIlkyariEV)) < (int(yMacsonucuDEP) - int(yIlkyariDEP)):
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ikinci_Yari_Sonucu_2_'] = df2.apply(lambda x: Ikinci_Yari_Sonucu_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Ikinci_Yari_Sonucu_2_']), axis=1)        
        
##########################################################################################################################################################
        
        def Ilk_Yari_15_Alt_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x) + int(y) < 2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_15_Alt_'] = df2.apply(lambda x: Ilk_Yari_15_Alt_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_15_Alt_']), axis=1)
        
##########################################################################################################################################################
        
        def Ilk_Yari_15_Ust_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x) + int(y) >= 2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Ilk_Yari_15_Ust_'] = df2.apply(lambda x: Ilk_Yari_15_Ust_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['Ilk_Yari_15_Ust_']), axis=1)
        
##########################################################################################################################################################
        
        def MS_15_Alt_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) + int(y) < 2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MS_15_Alt_'] = df2.apply(lambda x: MS_15_Alt_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MS_15_Alt_']), axis=1)        
        
##########################################################################################################################################################

        def MS_15_Ust_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) + int(y) >= 2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MS_15_Ust_'] = df2.apply(lambda x: MS_15_Ust_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MS_15_Ust_']), axis=1)        

##########################################################################################################################################################

        def MS_35_Alt_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) + int(y) < 4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MS_35_Alt_'] = df2.apply(lambda x: MS_35_Alt_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MS_35_Alt_']), axis=1)        
        
##########################################################################################################################################################

        def MS_35_Ust_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif int(x) + int(y) >= 4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MS_35_Ust_'] = df2.apply(lambda x: MS_35_Ust_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MS_35_Ust_']), axis=1) 

##########################################################################################################################################################

        def MS_Tek_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif (int(x) + int(y)) %2 != 0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MS_Tek_'] = df2.apply(lambda x: MS_Tek_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MS_Tek_']), axis=1) 

##########################################################################################################################################################

        def MS_Cift_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif (int(x) + int(y)) %2 == 0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MS_Cift_'] = df2.apply(lambda x: MS_Cift_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MS_Cift_']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_0_1_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif (int(x) + int(y)) <= 1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Toplam_Gol_0_1_'] = df2.apply(lambda x: Toplam_Gol_0_1_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Toplam_Gol_0_1_']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_2_3_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif 2 <= (int(x) + int(y)) <= 3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Toplam_Gol_2_3_'] = df2.apply(lambda x: Toplam_Gol_2_3_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Toplam_Gol_2_3_']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_4_5_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif 4 <= (int(x) + int(y)) <= 5:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Toplam_Gol_4_5_'] = df2.apply(lambda x: Toplam_Gol_4_5_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Toplam_Gol_4_5_']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_6_a_(x, y, z):
            if z == "" or x == 'Bekle' or z == '-'or x == 'E':
                return z
            elif (int(x) + int(y)) >= 6:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['Toplam_Gol_6_a_'] = df2.apply(lambda x: Toplam_Gol_6_a_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['Toplam_Gol_6_a_']), axis=1) 

##########################################################################################################################################################

        def IlkYari_MacSonucu_1_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_1_1_'] = df2.apply(lambda x: IlkYari_MacSonucu_1_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_1_1_']), axis=1)
        
##########################################################################################################################################################
        
        def IlkYari_MacSonucu_1_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_1_0_'] = df2.apply(lambda x: IlkYari_MacSonucu_1_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_1_0_']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_1_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_1_2_'] = df2.apply(lambda x: IlkYari_MacSonucu_1_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_1_2_']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_0_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_0_1_'] = df2.apply(lambda x: IlkYari_MacSonucu_0_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_0_1_']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_0_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_0_0_'] = df2.apply(lambda x: IlkYari_MacSonucu_0_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_0_0_']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_0_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_0_2_'] = df2.apply(lambda x: IlkYari_MacSonucu_0_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_0_2_']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_2_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_2_1_'] = df2.apply(lambda x: IlkYari_MacSonucu_2_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_2_1_']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_2_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_2_0_'] = df2.apply(lambda x: IlkYari_MacSonucu_2_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_2_0_']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_2_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['IlkYari_MacSonucu_2_2_'] = df2.apply(lambda x: IlkYari_MacSonucu_2_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['IlkYari_MacSonucu_2_2_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__1_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__1_0_'] = df2.apply(lambda x: MacSkoru_1__1_0_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__1_0_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__2_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__2_0_'] = df2.apply(lambda x: MacSkoru_1__2_0_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__2_0_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__3_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==3 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__3_0_'] = df2.apply(lambda x: MacSkoru_1__3_0_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__3_0_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==4 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__4_0_'] = df2.apply(lambda x: MacSkoru_1__4_0_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__4_0_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==5 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__5_0_'] = df2.apply(lambda x: MacSkoru_1__5_0_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__5_0_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__2_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__2_1_'] = df2.apply(lambda x: MacSkoru_1__2_1_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__2_1_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__3_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==3 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__3_1_'] = df2.apply(lambda x: MacSkoru_1__3_1_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__3_1_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==4 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__4_1_'] = df2.apply(lambda x: MacSkoru_1__4_1_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__4_1_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==5 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__5_1_'] = df2.apply(lambda x: MacSkoru_1__5_1_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__5_1_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__3_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==3 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__3_2_'] = df2.apply(lambda x: MacSkoru_1__3_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__3_2_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==4 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__4_2_'] = df2.apply(lambda x: MacSkoru_1__4_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__4_2_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==5 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__5_2_'] = df2.apply(lambda x: MacSkoru_1__5_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__5_2_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_3_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==4 and int(y)==3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__4_3_'] = df2.apply(lambda x: MacSkoru_1__4_3_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__4_3_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_3_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==5 and int(y)==3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__5_3_'] = df2.apply(lambda x: MacSkoru_1__5_3_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__5_3_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_4_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==5 and int(y)==4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_1__5_4_'] = df2.apply(lambda x: MacSkoru_1__5_4_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_1__5_4_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__0_0_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==0:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_0__0_0_'] = df2.apply(lambda x: MacSkoru_0__0_0_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_0__0_0_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__1_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_0__1_1_'] = df2.apply(lambda x: MacSkoru_0__1_1_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_0__1_1_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__2_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_0__2_2_'] = df2.apply(lambda x: MacSkoru_0__2_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_0__2_2_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__3_3_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==3 and int(y)==3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_0__3_3_'] = df2.apply(lambda x: MacSkoru_0__3_3_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_0__3_3_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__4_4_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==4 and int(y)==4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_0__4_4_'] = df2.apply(lambda x: MacSkoru_0__4_4_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_0__4_4_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__5_5_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==5 and int(y)==5:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_0__5_5_'] = df2.apply(lambda x: MacSkoru_0__5_5_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_0__5_5_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_1_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==1:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__0_1_'] = df2.apply(lambda x: MacSkoru_2__0_1_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__0_1_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__0_2_'] = df2.apply(lambda x: MacSkoru_2__0_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__0_2_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_3_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__0_3_'] = df2.apply(lambda x: MacSkoru_2__0_3_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__0_3_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_4_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__0_4_'] = df2.apply(lambda x: MacSkoru_2__0_4_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__0_4_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_5_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==0 and int(y)==5:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__0_5_'] = df2.apply(lambda x: MacSkoru_2__0_5_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__0_5_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_2_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==2:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__1_2_'] = df2.apply(lambda x: MacSkoru_2__1_2_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__1_2_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_3_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__1_3_'] = df2.apply(lambda x: MacSkoru_2__1_3_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__1_3_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_4_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__1_4_'] = df2.apply(lambda x: MacSkoru_2__1_4_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__1_4_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_5_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==1 and int(y)==5:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__1_5_'] = df2.apply(lambda x: MacSkoru_2__1_5_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__1_5_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__2_3_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==3:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__2_3_'] = df2.apply(lambda x: MacSkoru_2__2_3_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__2_3_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__2_4_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__2_4_'] = df2.apply(lambda x: MacSkoru_2__2_4_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__2_4_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__2_5_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==2 and int(y)==5:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__2_5_'] = df2.apply(lambda x: MacSkoru_2__2_5_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__2_5_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__3_4_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==3 and int(y)==4:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__3_4_'] = df2.apply(lambda x: MacSkoru_2__3_4_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__3_4_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__3_5_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==3 and int(y)==5:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__3_5_'] = df2.apply(lambda x: MacSkoru_2__3_5_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__3_5_']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__4_5_(x, y, z):
            if z == "" or x == 'Bekle'or z == '-'or x == 'E':
                return z
            elif int(x)==4 and int(y)==5:
                return '[{}]'.format(z)
            else:
                return '{}'.format(z)
            
        df2['MacSkoru_2__4_5_'] = df2.apply(lambda x: MacSkoru_2__4_5_(x['EvSahibi_Skor'], x['Deplasman_Skor'], x['MacSkoru_2__4_5_']), axis=1)
    
################################################################# Excel Haline #########################################################################################
        
        ColumName2 = ['ZamanSerisiTS', 'Maç Saati', 'Klasman', 'MBs', 'Evsahibi Tkm', 'Maç Sonucu', 'Deplasman Tkm', 'İlkYari Sonucu', 
                     'Mac Sonucu 1', 'Mac Sonucu 0', 'Mac Sonucu 2', 
                     '2.5 Alt', '2.5 Üst', 
                     'KG Var', 'KG Yok', 
                     'İl Yarı Gol Var', 'İlk Yarı Gol Yok', 
                     '1.5 Alt', '1.5 Üst', 
                     'Çifte Şans 1/0', 'Çifte Şans 1/2', 'Çifte Şans 0/2', 
                     'İlk Yarı Çifte Şans 1/0', 'İlk Yarı Çifte Şans 1/2', 'İl Yarı Çifte Şans 0/2', 
                     'İlk Yarı Sonucu 1', 'İlk Yarı Sonucu 0', 'İlk Yarı Sonucu 2', 
                     'İkinci Yarı Sonucu 1', 'İkinci Yarı Sonucu 0', 'İkinci Yarı Sonucu 2', 
                     'İlk Yarı 1.5 Alt', 'İl Yarı 1.5 Üst', 
                     'MS_ 1.5 Alt', 'MS_ 1.5 Üst', 
                     'MS_ 3.5 Alt', 'MS_ 3.5 Üst', 
                     'Tek', 'Çift', 
                     'Toplam Gol 0-1', 'Toplam Gol 2-3', 'Toplam Gol 4-5', 'Toplam Gol 6+', 
                     'İlk Yarı Maç Sonucu 1-1', 'İlk Yarı Maç Sonucu 1-0', 'İlk Yarı Maç Sonucu 1-2', 'İlk Yarı Maç Sonucu 0-1', 'İlk Yarı Maç Sonucu 0-0', 'İlk Yarı Maç Sonucu 0-2', 'İlk Yarı Maç Sonucu 2-1', 'İlk Yarı Maç Sonucu 2-0', 'İlk Yarı Maç Sonucu 2-2', 
                     'Maç Skoru 1-0', 'Maç Skoru 2-0', 'Maç Skoru 3-0', 'Maç Skoru 4-0', 'Maç Skoru 5-0', 'Maç Skoru 2-1', 'Maç Skoru 3-1', 'Maç Skoru 4-1', 'Maç Skoru 5-1', 'Maç Skoru 3-2', 'Maç Skoru 4-2', 'Maç Skoru 5-2', 'Maç Skoru 4-3', 'Maç Skoru 5-3', 'Maç Skoru 5-4', 
                     'Maç Skoru 0-0', 'Maç Skoru 1-1', 'Maç Skoru 2-2', 'Maç Skoru 3-3', 'Maç Skoru 4-4', 'Maç Skoru 5-5', 
                     'Maç Skoru 0-1', 'Maç Skoru 0-2', 'Maç Skoru 0-3', 'Maç Skoru 0-4', 'Maç Skoru 0-5', 'Maç Skoru 1-2', 'Maç Skoru 1-3', 'Maç Skoru 1-4', 'Maç Skoru 1-5', 'Maç Skoru 2-3', 'Maç Skoru 2-4', 'Maç Skoru 2-5', 'Maç Skoru 3-4-', 'Maç Skoru 3-5', 'Maç Skoru 4-5']
        
        df2 = df2.loc[:, 'ZamanSerisiTS':]
        df2 = df2.set_axis(ColumName2, axis=1, inplace=False)
        path = os.path.join(os.path.expanduser("~"), "Desktop", "DB {}-{}.xlsx".format(self.WeekName, self.DayName))
        df2.to_excel(path, index=False)
        
        
       
IddiaDB()