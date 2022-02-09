from import_data.functions import *
import pandas as pd


input_path = r'/home/adrian/npd/Projekt zaliczeniowy/'
output_path = r'/home/adrian/npd/Projekt zaliczeniowy/'

name_gminy_2020 = '20210215_Gminy_2_za_2020.xlsx'
name_woj_2020 = '20210211_Województwa_za_2020.xlsx'
name_miasta_npp_2020 = '20210215_Miasta_NPP_2_za_2020.xlsx'
name_powiaty_2020 = '20210211_Powiaty_za_2020.xlsx'
name_metropolia_2020 ='20210211_Metropolia_2020.xlsx'

name_gminy_2019 = '20200214_Gminy_za_2019.xlsx'
name_woj_2019 = '20200214_Wojewodztwa_za_2019.xlsx'
name_miasta_npp_2019 = '20200214_Miasta_NPP_za_2019.xlsx'
name_powiaty_2019 = '20200214_Powiaty_za_2019.xlsx'
name_metropolia_2019 ='20200214_Gornoslasko_Zaglebiowska_Metropolia.xlsx'

name_population = 'tabela11.xls'

income_2019 = import_data_tax_all(input_path, name_gminy_2019, name_woj_2019, name_miasta_npp_2019, name_powiaty_2019, name_metropolia_2019)
income_2020 = import_data_tax_all(input_path, name_gminy_2020, name_woj_2020, name_miasta_npp_2020, name_powiaty_2020, name_metropolia_2020)

# test, czy wczytane dane mają ten sam rozmiar
def test_import_data_income_all_length():
    
    assert len(income_2019) == len(income_2020)
    assert len(income_2019.columns) == len(income_2020.columns)
  
    
# testy, czy w danych mamy brakujące dane   
def test_import_data_income_all_missings_2019(): 
    for col in income_2019.columns:
        assert income_2019[col].isnull().sum() == 0
        
def test_import_data_income_all_missings_2020(): 
    for col in income_2020.columns:
        assert income_2020[col].isnull().sum() == 0
    