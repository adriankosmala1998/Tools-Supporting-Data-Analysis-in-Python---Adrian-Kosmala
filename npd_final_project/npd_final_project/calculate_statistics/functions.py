import pandas as pd



# Funkcja pomocnicza - licząca średnią ważoną na DataFrame
def calculate_weigted_average(input_table, variable, weight, by, output_variable):
    
    temp = input_table
    temp['proxy_var'] = temp[variable] * temp[weight] 
    temp_agg = temp.groupby(by = by).sum()
    temp_agg[output_variable] = temp_agg['proxy_var'] / temp_agg[weight]
    return temp_agg[[output_variable]] 
    


# Funkcja licząca wariancję i średnią ważoną jednostek podległych (na sparametryzowanym poziomie)
def calculate_partial_statistics(input_data, level, by):
    
    if by == 'Powiat':
        by_list = ['Powiat', 'Miasto na prawach powiatu']
        
    elif by == 'Gmina':
        if level == 'Powiat':
            by_list = ['Gmina']
        elif level == 'Województwo': 
            by_list = ['Gmina', 'Miasto na prawach powiatu']
            
    if level == 'Województwo':
        groupby_list = ['Województwo']
    elif level == 'Powiat':
        groupby_list = ['Województwo', 'Powiat']
        
        
    input_to_stats = input_data[input_data['Kategoria JST'].isin(by_list)]
    
    var_table = input_to_stats.groupby(by=groupby_list).var()
    var_table['Wariancja dochodu (' + by +')'] = var_table['Średni dochód opodatkowany ludności']
    var_table = var_table[['Wariancja dochodu (' + by +')'] ]
    
    weighted_average_table = calculate_weigted_average(input_table = input_to_stats, variable = 'Średni dochód opodatkowany ludności',
                                                         by = groupby_list, weight = 'Populacja',
                                                         output_variable = 'Średnia ważona dochodu (' + by +')' )
    
    if level == 'Powiat':
        total_income = input_data[input_data['Kategoria JST'] == level].set_index(['Województwo','Nazwa JST'])
        total_income = total_income[['Średni dochód opodatkowany ludności']]
        total_income.index.names = ['Województwo',level]
    
    elif level == 'Województwo':
        total_income = input_data[input_data['Kategoria JST'] == level].set_index(['Nazwa JST'])
        total_income = total_income[['Średni dochód opodatkowany ludności']]
        total_income.index.names = [level]
    
        
    output = pd.concat([total_income, var_table, weighted_average_table], axis=1)
    
    return output 




