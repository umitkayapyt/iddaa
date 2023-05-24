# -*- coding: utf-8 -*-
# Kazandıran - Kaybettiren oranların 1-0 encoding işlemleri

from locale import setlocale, LC_ALL, LC_TIME
from pandas import DataFrame, to_datetime, concat, read_excel
from pathlib import Path
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

        self.home = str(Path.home())+'\\iddiaDB'
        self.WeekName = '1_'
        self.DayName  = '0'
        #kolonlar;
       
        self.ColumName = ['ZamanSerisiTS', 'MacSaati', 'Klasman', 'MBs', 'Evsahibi', 'MacSonucu', 'Deplasman', 'İlkYari', 
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
    

        self.DosyaProces()

####################################################################### 4 Yeni Kolon ##############################################################################

        
    def DosyaProces(self): #takımların ilk yarı ve ikinci yarı attığı gollerin tabloya eklenmesi
        df2 = read_excel('DBALL.xlsx', engine='openpyxl')

        df2 = df2.set_axis(self.ColumName, axis=1, inplace=False)
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
################################################################# ENCODING ##########################################################################
##########################################################################################################################################################

        def Mac_Sonucu_1(x, y):
            if x > y:
                return 1
            else:
                return 0
            
        df2['Mac_Sonucu_1'] = df2.apply(lambda x: Mac_Sonucu_1(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)

##########################################################################################################################################################

        def Mac_Sonucu_0(x, y):
            if x == y:
                return 1
            else:
                return 0
            
        df2['Mac_Sonucu_0'] = df2.apply(lambda x: Mac_Sonucu_0(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
        
##########################################################################################################################################################

        def Mac_Sonucu_2(x, y):
            if x < y:
                return 1
            else:
                return 0
            
        df2['Mac_Sonucu_2'] = df2.apply(lambda x: Mac_Sonucu_2(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_2_5_Alt(x, y):
            if int(x)+int(y) < 3:
                return 1
            else:
                return 0
            
        df2['Mac_S_2_5_Alt'] = df2.apply(lambda x: Mac_S_2_5_Alt(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_2_5_Ust(x, y):
            if int(x)+int(y) >= 3:
                return 1
            else:
                return 0
            
        df2['Mac_S_2_5_Ust'] = df2.apply(lambda x: Mac_S_2_5_Ust(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################


        def Mac_S_KG_Var(x, y):
            if int(x) and int(y) > 0:
                return 1
            else:
                return 0
            
        df2['Mac_S_KG_Var'] = df2.apply(lambda x: Mac_S_KG_Var(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_KG_Yok(x, y):
            if int(x) == 0 or int(y) == 0:
                return 1
            else:
                return 0
            
        df2['Mac_S_KG_Yok'] = df2.apply(lambda x: Mac_S_KG_Yok(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def IlkYari_Gol_Var(x, y):
            if int(x) + int(y) > 0:
                return 1
            else:
                return 0
            
        df2['IlkYari_Gol_Var'] = df2.apply(lambda x: IlkYari_Gol_Var(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################

        def IlkYari_Gol_Yok(x, y):
            if int(x) + int(y) == 0:
                return 1
            else:
                return 0
            
        df2['IlkYari_Gol_Yok'] = df2.apply(lambda x: IlkYari_Gol_Yok(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_1_5_Alt(x, y):
            if int(x) + int(y) < 2:
                return 1
            else:
                return 0
            
        df2['Mac_S_1_5_Alt'] = df2.apply(lambda x: Mac_S_1_5_Alt(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Mac_S_1_5_Ust(x, y):
            if int(x) + int(y) >= 2:
                return 1
            else:
                return 0
            
        df2['Mac_S_1_5_Ust'] = df2.apply(lambda x: Mac_S_1_5_Ust(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def CifteSans_1_0_(x, y):
            if int(x) >= int(y):
                return 1
            else:
                return 0
            
        df2['CifteSans_1_0_'] = df2.apply(lambda x: CifteSans_1_0_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def CifteSans_1_2_(x, y):
            if int(x) != int(y):
                return 1
            else:
                return 0
            
        df2['CifteSans_1_2_'] = df2.apply(lambda x: CifteSans_1_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def CifteSans_0_2_(x, y):
            if int(x) <= int(y):
                return 1
            else:
                return 0
            
        df2['CifteSans_0_2_'] = df2.apply(lambda x: CifteSans_0_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_CifteSans_10_(x, y):
            if int(x) >= int(y):
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_CifteSans_10_'] = df2.apply(lambda x: Ilk_Yari_CifteSans_10_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################
    
        def Ilk_Yari_CifteSans_12_(x, y):
            if int(x) != int(y):
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_CifteSans_12_'] = df2.apply(lambda x: Ilk_Yari_CifteSans_12_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_CifteSans_02_(x, y):
            if int(x) <= int(y):
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_CifteSans_02_'] = df2.apply(lambda x: Ilk_Yari_CifteSans_02_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_Sonucu_1_(x, y):
            if int(x) > int(y):
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_Sonucu_1_'] = df2.apply(lambda x: Ilk_Yari_Sonucu_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_Sonucu_0_(x, y):
            if int(x) == int(y):
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_Sonucu_0_'] = df2.apply(lambda x: Ilk_Yari_Sonucu_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ilk_Yari_Sonucu_2_(x, y):
            if int(x) < int(y):
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_Sonucu_2_'] = df2.apply(lambda x: Ilk_Yari_Sonucu_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ikinci_Yari_Sonucu_1_(xIlkyariEV, yIlkyariDEP, xMacsonucuEV, yMacsonucuDEP):
            if (int(xMacsonucuEV) - int(xIlkyariEV)) > (int(yMacsonucuDEP) - int(yIlkyariDEP)):
                return 1
            else:
                return 0
            
        df2['Ikinci_Yari_Sonucu_1_'] = df2.apply(lambda x: Ikinci_Yari_Sonucu_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ikinci_Yari_Sonucu_0_(xIlkyariEV, yIlkyariDEP, xMacsonucuEV, yMacsonucuDEP):
            if (int(xMacsonucuEV) - int(xIlkyariEV)) == (int(yMacsonucuDEP) - int(yIlkyariDEP)):
                return 1
            else:
                return 0
            
        df2['Ikinci_Yari_Sonucu_0_'] = df2.apply(lambda x: Ikinci_Yari_Sonucu_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def Ikinci_Yari_Sonucu_2_(xIlkyariEV, yIlkyariDEP, xMacsonucuEV, yMacsonucuDEP):
            if (int(xMacsonucuEV) - int(xIlkyariEV)) < (int(yMacsonucuDEP) - int(yIlkyariDEP)):
                return 1
            else:
                return 0
            
        df2['Ikinci_Yari_Sonucu_2_'] = df2.apply(lambda x: Ikinci_Yari_Sonucu_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor'], x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################
        
        def Ilk_Yari_15_Alt_(x, y):
            if int(x) + int(y) < 2:
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_15_Alt_'] = df2.apply(lambda x: Ilk_Yari_15_Alt_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
        
##########################################################################################################################################################
        
        def Ilk_Yari_15_Ust_(x, y):
            if int(x) + int(y) >= 2:
                return 1
            else:
                return 0
            
        df2['Ilk_Yari_15_Ust_'] = df2.apply(lambda x: Ilk_Yari_15_Ust_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
        
##########################################################################################################################################################
        
        def MS_15_Alt_(x, y):
            if int(x) + int(y) < 2:
                return 1
            else:
                return 0
            
        df2['MS_15_Alt_'] = df2.apply(lambda x: MS_15_Alt_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def MS_15_Ust_(x, y):
            if int(x) + int(y) >= 2:
                return 1
            else:
                return 0
            
        df2['MS_15_Ust_'] = df2.apply(lambda x: MS_15_Ust_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        

##########################################################################################################################################################

        def MS_35_Alt_(x, y):
            if int(x) + int(y) < 4:
                return 1
            else:
                return 0
            
        df2['MS_35_Alt_'] = df2.apply(lambda x: MS_35_Alt_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)        
        
##########################################################################################################################################################

        def MS_35_Ust_(x, y):
            if int(x) + int(y) >= 4:
                return 1
            else:
                return 0
            
        df2['MS_35_Ust_'] = df2.apply(lambda x: MS_35_Ust_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1) 

##########################################################################################################################################################

        def MS_Tek_(x, y):
            if (int(x) + int(y)) %2 != 0:
                return 1
            else:
                return 0
            
        df2['MS_Tek_'] = df2.apply(lambda x: MS_Tek_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1) 

##########################################################################################################################################################

        def MS_Cift_(x, y):
            if (int(x) + int(y)) %2 == 0:
                return 1
            else:
                return 0
            
        df2['MS_Cift_'] = df2.apply(lambda x: MS_Cift_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_0_1_(x, y):
            if (int(x) + int(y)) <= 1:
                return 1
            else:
                return 0
            
        df2['Toplam_Gol_0_1_'] = df2.apply(lambda x: Toplam_Gol_0_1_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_2_3_(x, y):
            if 2 <= (int(x) + int(y)) <= 3:
                return 1
            else:
                return 0
            
        df2['Toplam_Gol_2_3_'] = df2.apply(lambda x: Toplam_Gol_2_3_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_4_5_(x, y):
            if 4 <= (int(x) + int(y)) <= 5:
                return 1
            else:
                return 0
            
        df2['Toplam_Gol_4_5_'] = df2.apply(lambda x: Toplam_Gol_4_5_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1) 

##########################################################################################################################################################

        def Toplam_Gol_6_a_(x, y):
            if (int(x) + int(y)) >= 6:
                return 1
            else:
                return 0
            
        df2['Toplam_Gol_6_a_'] = df2.apply(lambda x: Toplam_Gol_6_a_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1) 

##########################################################################################################################################################

        def IlkYari_MacSonucu_1_1_(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_1_1_'] = df2.apply(lambda x: IlkYari_MacSonucu_1_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
        
##########################################################################################################################################################
        
        def IlkYari_MacSonucu_1_0_(x, y):
            if int(x)==1 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_1_0_'] = df2.apply(lambda x: IlkYari_MacSonucu_1_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_1_2_(x, y):
            if int(x)==1 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_1_2_'] = df2.apply(lambda x: IlkYari_MacSonucu_1_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_0_1_(x, y):
            if int(x)==0 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_0_1_'] = df2.apply(lambda x: IlkYari_MacSonucu_0_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_0_0_(x, y):
            if int(x)==0 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_0_0_'] = df2.apply(lambda x: IlkYari_MacSonucu_0_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_0_2_(x, y):
            if int(x)==0 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_0_2_'] = df2.apply(lambda x: IlkYari_MacSonucu_0_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_2_1_(x, y):
            if int(x)==2 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_2_1_'] = df2.apply(lambda x: IlkYari_MacSonucu_2_1_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_2_0_(x, y):
            if int(x)==2 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_2_0_'] = df2.apply(lambda x: IlkYari_MacSonucu_2_0_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def IlkYari_MacSonucu_2_2_(x, y):
            if int(x)==2 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['IlkYari_MacSonucu_2_2_'] = df2.apply(lambda x: IlkYari_MacSonucu_2_2_(x['EvSahibi_İlkYari_Skor'], x['Deplasman_İlkYari_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__1_0_(x, y):
            if int(x)==1 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__1_0_'] = df2.apply(lambda x: MacSkoru_1__1_0_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__2_0_(x, y):
            if int(x)==2 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__2_0_'] = df2.apply(lambda x: MacSkoru_1__2_0_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__3_0_(x, y):
            if int(x)==3 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__3_0_'] = df2.apply(lambda x: MacSkoru_1__3_0_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_0_(x, y):
            if int(x)==4 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__4_0_'] = df2.apply(lambda x: MacSkoru_1__4_0_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_0_(x, y):
            if int(x)==5 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__5_0_'] = df2.apply(lambda x: MacSkoru_1__5_0_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__2_1_(x, y):
            if int(x)==2 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__2_1_'] = df2.apply(lambda x: MacSkoru_1__2_1_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__3_1_(x, y):
            if int(x)==3 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__3_1_'] = df2.apply(lambda x: MacSkoru_1__3_1_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_1_(x, y):
            if int(x)==4 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__4_1_'] = df2.apply(lambda x: MacSkoru_1__4_1_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_1_(x, y):
            if int(x)==5 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__5_1_'] = df2.apply(lambda x: MacSkoru_1__5_1_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__3_2_(x, y):
            if int(x)==3 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__3_2_'] = df2.apply(lambda x: MacSkoru_1__3_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_2_(x, y):
            if int(x)==4 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__4_2_'] = df2.apply(lambda x: MacSkoru_1__4_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_2_(x, y):
            if int(x)==5 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__5_2_'] = df2.apply(lambda x: MacSkoru_1__5_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__4_3_(x, y):
            if int(x)==4 and int(y)==3:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__4_3_'] = df2.apply(lambda x: MacSkoru_1__4_3_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_3_(x, y):
            if int(x)==5 and int(y)==3:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__5_3_'] = df2.apply(lambda x: MacSkoru_1__5_3_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_1__5_4_(x, y):
            if int(x)==5 and int(y)==4:
                return 1
            else:
                return 0
            
        df2['MacSkoru_1__5_4_'] = df2.apply(lambda x: MacSkoru_1__5_4_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__0_0_(x, y):
            if int(x)==0 and int(y)==0:
                return 1
            else:
                return 0
            
        df2['MacSkoru_0__0_0_'] = df2.apply(lambda x: MacSkoru_0__0_0_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__1_1_(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['MacSkoru_0__1_1_'] = df2.apply(lambda x: MacSkoru_0__1_1_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__2_2_(x, y):
            if int(x)==2 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['MacSkoru_0__2_2_'] = df2.apply(lambda x: MacSkoru_0__2_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__3_3_(x, y):
            if int(x)==3 and int(y)==3:
                return 1
            else:
                return 0
            
        df2['MacSkoru_0__3_3_'] = df2.apply(lambda x: MacSkoru_0__3_3_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__4_4_(x, y):
            if int(x)==4 and int(y)==4:
                return 1
            else:
                return 0
            
        df2['MacSkoru_0__4_4_'] = df2.apply(lambda x: MacSkoru_0__4_4_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_0__5_5_(x, y):
            if int(x)==5 and int(y)==5:
                return 1
            else:
                return 0
            
        df2['MacSkoru_0__5_5_'] = df2.apply(lambda x: MacSkoru_0__5_5_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_1_(x, y):
            if int(x)==0 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__0_1_'] = df2.apply(lambda x: MacSkoru_2__0_1_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_2_(x, y):
            if int(x)==0 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__0_2_'] = df2.apply(lambda x: MacSkoru_2__0_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_3_(x, y):
            if int(x)==0 and int(y)==3:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__0_3_'] = df2.apply(lambda x: MacSkoru_2__0_3_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_4_(x, y):
            if int(x)==0 and int(y)==4:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__0_4_'] = df2.apply(lambda x: MacSkoru_2__0_4_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__0_5_(x, y):
            if int(x)==0 and int(y)==5:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__0_5_'] = df2.apply(lambda x: MacSkoru_2__0_5_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_2_(x, y):
            if int(x)==1 and int(y)==2:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__1_2_'] = df2.apply(lambda x: MacSkoru_2__1_2_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_3_(x, y):
            if int(x)==1 and int(y)==3:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__1_3_'] = df2.apply(lambda x: MacSkoru_2__1_3_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_4_(x, y):
            if int(x)==1 and int(y)==4:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__1_4_'] = df2.apply(lambda x: MacSkoru_2__1_4_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__1_5_(x, y):
            if int(x)==1 and int(y)==5:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__1_5_'] = df2.apply(lambda x: MacSkoru_2__1_5_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__2_3_(x, y):
            if int(x)==2 and int(y)==3:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__2_3_'] = df2.apply(lambda x: MacSkoru_2__2_3_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__2_4_(x, y):
            if int(x)==2 and int(y)==4:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__2_4_'] = df2.apply(lambda x: MacSkoru_2__2_4_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__2_5_(x, y):
            if int(x)==2 and int(y)==5:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__2_5_'] = df2.apply(lambda x: MacSkoru_2__2_5_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__3_4_(x, y):
            if int(x)==3 and int(y)==4:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__3_4_'] = df2.apply(lambda x: MacSkoru_2__3_4_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__3_5_(x, y):
            if int(x)==3 and int(y)==5:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__3_5_'] = df2.apply(lambda x: MacSkoru_2__3_5_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################

        def MacSkoru_2__4_5_(x, y):
            if int(x)==4 and int(y)==5:
                return 1
            else:
                return 0
            
        df2['MacSkoru_2__4_5_'] = df2.apply(lambda x: MacSkoru_2__4_5_(x['EvSahibi_Skor'], x['Deplasman_Skor']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY1_MS0(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY1_MS0'] = df2.apply(lambda x: Mac_IY1_MS0(x['Ilk_Yari_Sonucu_1_'], x['Mac_Sonucu_0']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY1_MS1(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY1_MS1'] = df2.apply(lambda x: Mac_IY1_MS1(x['Ilk_Yari_Sonucu_1_'], x['Mac_Sonucu_1']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY1_MS2(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY1_MS2'] = df2.apply(lambda x: Mac_IY1_MS2(x['Ilk_Yari_Sonucu_1_'], x['Mac_Sonucu_2']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY2_MS0(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY2_MS0'] = df2.apply(lambda x: Mac_IY2_MS0(x['Ilk_Yari_Sonucu_2_'], x['Mac_Sonucu_0']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY2_MS1(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY2_MS1'] = df2.apply(lambda x: Mac_IY2_MS1(x['Ilk_Yari_Sonucu_2_'], x['Mac_Sonucu_1']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY2_MS2(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY2_MS2'] = df2.apply(lambda x: Mac_IY2_MS2(x['Ilk_Yari_Sonucu_2_'], x['Mac_Sonucu_2']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY0_MS0(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY0_MS0'] = df2.apply(lambda x: Mac_IY0_MS0(x['Ilk_Yari_Sonucu_0_'], x['Mac_Sonucu_0']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY0_MS1(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY0_MS1'] = df2.apply(lambda x: Mac_IY0_MS1(x['Ilk_Yari_Sonucu_0_'], x['Mac_Sonucu_1']), axis=1)
    
##########################################################################################################################################################
        
        def Mac_IY0_MS2(x, y):
            if int(x)==1 and int(y)==1:
                return 1
            else:
                return 0
            
        df2['Mac_IY0_MS2'] = df2.apply(lambda x: Mac_IY0_MS2(x['Ilk_Yari_Sonucu_0_'], x['Mac_Sonucu_2']), axis=1)
    
############################################################ Son İşlemler Excel Haline ##################################################################################
        

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
                     'Maç Skoru 0-1', 'Maç Skoru 0-2', 'Maç Skoru 0-3', 'Maç Skoru 0-4', 'Maç Skoru 0-5', 'Maç Skoru 1-2', 'Maç Skoru 1-3', 'Maç Skoru 1-4', 'Maç Skoru 1-5', 'Maç Skoru 2-3', 'Maç Skoru 2-4', 'Maç Skoru 2-5', 'Maç Skoru 3-4-', 'Maç Skoru 3-5', 'Maç Skoru 4-5',
                     'İlk Yarı 1 Maç 0','İlk Yarı 1 Maç 1','İlk Yarı 1 Maç 2',
                     'İlk Yarı 2 Maç 0','İlk Yarı 2 Maç 1','İlk Yarı 2 Maç 2',
                     'İlk Yarı 0 Maç 0','İlk Yarı 0 Maç 1','İlk Yarı 0 Maç 2']
        
        df2 = df2.loc[:, 'ZamanSerisiTS':]
        df2 = df2.set_axis(ColumName2, axis=1, inplace=False)
        path = os.path.join(os.path.expanduser("~"), "Desktop", "DB {}-{}.xlsx".format(self.WeekName, self.DayName))
        df2.to_excel(path, index=False)
        
        
       
IddiaDB()