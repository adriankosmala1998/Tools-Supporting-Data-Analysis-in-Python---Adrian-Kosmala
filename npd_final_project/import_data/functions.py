import pandas as pd

# Funkcja importujaca dane o dochodzie z podatku PIT, ktory trafil do kazdej JST 
def import_data_tax(path, input_name, category):
    output = pd.read_excel(path + input_name, header= [0], skiprows=[0,1,2,4,5,6],
                           dtype = {'WK':str,'PK':str,'GK':str,'GT':str, })
    
    
    if category == 'Powiat':
        output['GK'] = '00'
        output['GT'] = '0'
        
    elif category == 'Miasto na prawach powiatu':
        for i in range(len(output)):
            if output.at[i, 'województwo'] in ('dolnośląskie', 'łódzkie'):
                output.at[i, 'GK'] = '00'
                output.at[i, 'GT'] = '0'
            else:
                output.at[i, 'GK'] = '01'
                output.at[i, 'GT'] = '1'
    
    elif category == 'Województwo':
        output['PK'] = '00'
        output['GK'] = '00'
        output['GT'] = '0'
        
        
        
    output['Identyfikator terytorialny'] = output['WK'] +	output['PK'] +	output['GK'] + output['GT']

    output = output.loc[:,['Identyfikator terytorialny', 'Nazwa JST', 'województwo',
                           'powiat', 'Należności \n (saldo początkowe plus przypisy minus odpisy)']]
    
    output = output.rename(columns={'województwo': 'Województwo', 
                                    'powiat': 'Powiat',
                                    'Należności \n (saldo początkowe plus przypisy minus odpisy)':
                                        'Dochód przynależny JST'})
    
    
    if category =='Miasto na prawach powiatu':
        output = output.groupby(by=['Identyfikator terytorialny','Nazwa JST',
                                    'Województwo','Powiat'],
                                as_index=False).sum()
        
    output['Kategoria JST'] = category
    
    return output 



# Funkcja poprawiająca kody terytorialne dla JST, które nie były zgodne z kodami dostępnymi w danych o liczbie ludności
def update_teritorial_codes(input_data_2019, input_data_2020):
    
    output_2019 = input_data_2019
    output_2020 = input_data_2020
    
    output_2019.loc[output_2019['Nazwa JST'] == "PIĄTEK", "Identyfikator terytorialny"] = "1004063"
    output_2019.loc[output_2019['Nazwa JST'] == "LUTUTÓW", "Identyfikator terytorialny"] = "1018043"
    output_2019.loc[output_2019['Nazwa JST']== "CHEŁMIEC", "Identyfikator terytorialny"] = "1210022" 
    output_2019.loc[output_2019['Nazwa JST']== "CZERWIŃSK NAD WISŁĄ", "Identyfikator terytorialny"] = "1420043" 
    output_2019.loc[output_2019['Nazwa JST']== "KLIMONTÓW", "Identyfikator terytorialny"] = "2609033"
    
    output_2020.loc[output_2020['Nazwa JST'] == "KAMIENIEC ZĄBKOWICKI", "Identyfikator terytorialny"] = "0224032"
    output_2020.loc[output_2020['Nazwa JST'] == "GORAJ", "Identyfikator terytorialny"] = "0602062"
    output_2020.loc[output_2020['Nazwa JST']== "KAMIONKA", "Identyfikator terytorialny"] = "0608052" 
    output_2020.loc[output_2020['Nazwa JST']== "SOLEC NAD WISŁĄ", "Identyfikator terytorialny"] = "1409062" 
    output_2020.loc[output_2020['Nazwa JST']== "SOCHOCIN", "Identyfikator terytorialny"] = "1420112"
    output_2020.loc[output_2020['Nazwa JST'] == "WISKITKI", "Identyfikator terytorialny"] = "1438052"
    output_2020.loc[output_2020['Nazwa JST'] == "DUBIECKO", "Identyfikator terytorialny"] = "1813022"
    output_2020.loc[output_2020['Nazwa JST']== "WODZISŁAW", "Identyfikator terytorialny"] = "2602092" 
    output_2020.loc[output_2020['Nazwa JST']== "BUDZYŃ", "Identyfikator terytorialny"] = "3001022" 
    output_2020.loc[output_2020['Nazwa JST']== "KOŹMINEK", "Identyfikator terytorialny"] = "3007052"
    
    output_2020 = output_2020.replace({'karkonoski (jeleniogórski)': 'jeleniogórski'})
    output_2020 = output_2020.replace({'wągrowiecki': 'wągrowicki'})
    output_2019 = output_2019.replace({'wągrowiecki': 'wągrowicki'})
    
    return output_2019, output_2020



# Funkcja łącząca wszystkie tabele z danymi o podatku PiT przysługującym JST
def import_data_tax_all(input_path, name_gminy, name_woj, name_miasta_npp, name_powiaty, name_metropolia):
    
    df_income_gminy = import_data_tax(input_path, name_gminy, category = 'Gmina')
    df_income_woj = import_data_tax(input_path, name_woj, category = 'Województwo')
    df_income_miasta_npp = import_data_tax(input_path, name_miasta_npp, category = 'Miasto na prawach powiatu')
    df_income_powiaty = import_data_tax(input_path, name_powiaty, category = 'Powiat')
    df_income_metropolia = import_data_tax(input_path, name_metropolia, category = 'Metropolia')
                             
    df_income = pd.concat([df_income_gminy, df_income_miasta_npp, df_income_powiaty, df_income_metropolia, df_income_woj])
    df_income = df_income.reset_index(drop=True)
    
    return df_income



# Funkcja importująca dane o populacji
def import_data_population(path, input_name):
    
    output_final = pd.DataFrame()
    
    for i in range(16): # osobny arkusz dla każdego województwa, stąd pętla
        
        output = pd.read_excel(path + input_name,  sheet_name = i, header= [0], skiprows=[0,1,2,3,4,6], dtype = {'Identyfikator terytorialny\nCode': str})
        output = output.rename(columns={'Wyszczególnienie\nSpecification': 'Nazwa JST', 'Identyfikator terytorialny\nCode': 'Identyfikator terytorialny',
                                                 'Ogółem \nTotal': 'Populacja'})
        output = output.loc[:, ['Nazwa JST', 'Identyfikator terytorialny', 'Populacja']]
        output = output.dropna(axis=0, how= 'all', subset = ['Populacja'])
        output_final = pd.concat([output_final, output])
        output_final = output_final.reset_index(drop=True)
        
    return output_final



# Funkcja licząca całkowity podatek zapłacony przez mieszkańców JST
def calculate_total_people_tax(input_df):
    total_income = []
    for i in range(len(input_df)):
        if input_df['Kategoria JST'][i] == 'Gmina':
            total_income.append((1/0.3934)*input_df['Dochód przynależny JST'][i]) 
        elif input_df['Kategoria JST'][i] == 'Powiat':
            total_income.append((1/0.1025)*input_df['Dochód przynależny JST'][i])
        elif input_df['Kategoria JST'][i] == 'Miasto na prawach powiatu':
            total_income.append((1/(0.3934+ 0.1025))*input_df['Dochód przynależny JST'][i]) 
        elif input_df['Kategoria JST'][i] == 'Metropolia':
            total_income.append((1/0.05)*input_df['Dochód przynależny JST'][i]) 
        elif input_df['Kategoria JST'][i] == 'Województwo':
            total_income.append((1/0.0160)*input_df['Dochód przynależny JST'][i]) 
        else:
            print("Nieprawidłowa kategoria przyporządkowana dla " + input_df['Nazwa JST'][i])
         
    output_df = input_df
    output_df['Podatek całkowity ludności'] = total_income
    return output_df



# Funkcja łącząca dane o podatku z danymi o populacji
def join_population(income_data, population_data):
    
    woj_df = income_data[income_data['Kategoria JST']=='Województwo'][['Identyfikator terytorialny', 'Nazwa JST']].reset_index(drop=True)
    woj_df['Nazwa JST'] = 'WOJ. ' + woj_df['Nazwa JST'].str.upper()
    
    population_temp = population_data
    population_temp.replace({'WOJ. KUJAWSKO-': 'WOJ. KUJAWSKO-POMORSKIE', 'WOJ. WARMIŃSKO-': 'WOJ. WARMIŃSKO-MAZURSKIE',
                             'WOJ. ZACHODNIO-': 'WOJ. ZACHODNIOPOMORSKIE'}, inplace=True) #obsługa wyjątków
    
    
        
    for i in range(len(population_temp)):
        
        for j in range(len(woj_df)):
            
            if population_temp.at[i,'Nazwa JST'] == woj_df.at[j,'Nazwa JST']:
                population_temp.at[i,'Identyfikator terytorialny'] = woj_df.at[j,'Identyfikator terytorialny']
                
    population_temp = population_temp[['Identyfikator terytorialny', 'Populacja']]
                
    output = income_data.merge(population_temp, how = 'left', on = 'Identyfikator terytorialny')
                
    return output



# Funkcja przyporządkowująca populację dla Metropolii (tych danych nie ma w tabeli z populacją)
def calculate_metropolia_population(input_data):
    
    jst_in_metropolia = input_data[input_data['Identyfikator terytorialny'].isin(['2401011', #Będzin
                                                                                  '2414011',#Bieruń
                                                                                  '2401042',#Bobrowniki
                                                                                  '2414042',#Bojszowy
                                                                                  '2462011',#Bytom
                                                                                  '2414052',#Chełm Śląski
                                                                                  '2463011',#Chorzów
                                                                                  '2401021',#Czeladź
                                                                                  '2465011',#Dąbrowa Górnicza
                                                                                  '2405032',#Gierałtowice
                                                                                  '2466011',#Gliwice
                                                                                  '2414021',#Imielin
                                                                                  '2469011',#Katowice
                                                                                  '2405011',#Knurów
                                                                                  '2410022',#Kobiór
                                                                                  '2414031',#Lędziny
                                                                                  '2408011',#Łaziska Górne
                                                                                  '2401052',#Mierzęcice
                                                                                  '2408021',#Mikołów
                                                                                  '2470011',#Mysłowice
                                                                                  '2413062',#Ożarowice
                                                                                  '2471011',#Piekary 
                                                                                  '2405042',#Pilchowice
                                                                                  '2401062',#Psary
                                                                                  '2405021',#Pyskowice
                                                                                  '2413031',#Radzionków
                                                                                  '2472011',#Ruda Śląska
                                                                                  '2405052',#Rudziniec
                                                                                  '2474011',#Siemianowice Śląskie
                                                                                  '2401073',#Siewierz
                                                                                  '2401081',#Sławków
                                                                                  '2475011',#Sosnowiec
                                                                                  '2405063',#Sośnicowice
                                                                                  '2413072',#Świerklaniec
                                                                                  '2476011',#Świętochłowice
                                                                                  '2413041',#Tarnowskie Góry
                                                                                  '2477011',#Tychy
                                                                                  '2401031',#Wojkowice
                                                                                  '2408052',#Wyry
                                                                                  '2478011',#Zabrze
                                                                                  '2413092'#Zbrosławice
                                                                                      ])]
    
    metropolia_population = jst_in_metropolia['Populacja'].sum()
    output = input_data
    output.loc[output['Kategoria JST'] == "Metropolia", "Populacja"] = metropolia_population
    
    return output
    


# Funkcja licząca średni dochód na mieszkańca
def calculate_average_taxed_income(input_data, tax, working_people_share = 0.7 ):
    
    output = input_data
    
    output['Średni zapłacony podatek PIT'] = output['Podatek całkowity ludności'] / (output['Populacja'] * working_people_share)
    
    output['Średni dochód opodatkowany ludności'] = (1/tax) * output['Średni zapłacony podatek PIT'] 
    
    output = output[['Identyfikator terytorialny', 'Kategoria JST', 'Nazwa JST', 'Województwo', 'Powiat', 'Populacja', 'Dochód przynależny JST',	
                     'Podatek całkowity ludności', 'Średni zapłacony podatek PIT', 'Średni dochód opodatkowany ludności']]


    
    return output
    
    
    

