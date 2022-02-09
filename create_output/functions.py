from npd_final_project.import_data.functions import *
from npd_final_project.calculate_statistics.functions import *



#funkcja pozwalająca przeprowadzić obliczenia od początka do końca - łączy działanie funkcji z pozostałych modułów 
def calculate_all_statistics(input_path, name_gminy_2020, name_woj_2020, name_miasta_npp_2020, name_powiaty_2020, name_metropolia_2020, 
                             name_gminy_2019, name_woj_2019, name_miasta_npp_2019, name_powiaty_2019, name_metropolia_2019,
                             name_population, output_path, output_name,
                             tax_perc_2020 = 0.17, tax_perc_2019 = 0.18, working_people_share_2020 =0.7, working_people_share_2019 = 0.7):
    
    population = import_data_population(input_path, name_population)
    
    tax_2019 = import_data_tax_all(input_path, name_gminy_2019, name_woj_2019, name_miasta_npp_2019, name_powiaty_2019, name_metropolia_2019)
    tax_2020 = import_data_tax_all(input_path, name_gminy_2020, name_woj_2020, name_miasta_npp_2020, name_powiaty_2020, name_metropolia_2020)
    
    tax_2019, tax_2020 = update_teritorial_codes(tax_2019, tax_2020)
    
    df_total_tax_2019 = calculate_total_people_tax(tax_2019)
    df_total_tax_2020 = calculate_total_people_tax(tax_2020)
    
    df_tax_population_2019 = join_population(df_total_tax_2019, population)
    df_tax_population_2020 = join_population(df_total_tax_2020, population)
    
    df_tax_population_2019 = calculate_metropolia_population(df_tax_population_2019)
    df_tax_population_2020 = calculate_metropolia_population(df_tax_population_2020)
    
    df_avg_taxed_income_2019 = calculate_average_taxed_income(df_tax_population_2019, tax = tax_perc_2019, working_people_share = working_people_share_2019 )
    df_avg_taxed_income_2020 = calculate_average_taxed_income(df_tax_population_2020, tax = tax_perc_2020, working_people_share = working_people_share_2020 )
    df_avg_income = df_avg_taxed_income_2019.merge(right = df_avg_taxed_income_2020[['Identyfikator terytorialny', 'Dochód przynależny JST',	                             
                                                'Podatek całkowity ludności', 'Średni zapłacony podatek PIT', 'Średni dochód opodatkowany ludności']], 
                                                 how = 'outer', on = ['Identyfikator terytorialny'], suffixes = (' 2019', ' 2020'))
    
    
    df_stats_woj_by_powiat_2019 = calculate_partial_statistics(df_avg_taxed_income_2019, level = 'Województwo', by = 'Powiat')
    df_stats_woj_by_powiat_2020 = calculate_partial_statistics(df_avg_taxed_income_2020, level = 'Województwo', by = 'Powiat')
    df_stats_woj_by_powiat = df_stats_woj_by_powiat_2019.merge(right = df_stats_woj_by_powiat_2020, how = 'outer', on = 'Województwo',
                                                               suffixes = (' 2019', ' 2020'))
    
    
    df_stats_woj_by_gmina_2019 = calculate_partial_statistics(df_avg_taxed_income_2019, level = 'Województwo', by = 'Gmina')
    df_stats_woj_by_gmina_2020 = calculate_partial_statistics(df_avg_taxed_income_2020, level = 'Województwo', by = 'Gmina')
    df_stats_woj_by_gmina = df_stats_woj_by_gmina_2019.merge(right = df_stats_woj_by_gmina_2020, how = 'outer', on = 'Województwo',
                                                             suffixes = (' 2019', ' 2020'))
    
    
    df_stats_powiat_by_gmina_2019 = calculate_partial_statistics(df_avg_taxed_income_2019, level = 'Powiat', by = 'Gmina')
    df_stats_powiat_by_gmina_2020 = calculate_partial_statistics(df_avg_taxed_income_2020, level = 'Powiat', by = 'Gmina')
    df_stats_powiat_by_gmina = df_stats_powiat_by_gmina_2019.merge(right = df_stats_powiat_by_gmina_2020, how = 'outer', on = ['Województwo', 'Powiat'],
                                                                   suffixes = (' 2019', ' 2020'))
    
    
    writer = pd.ExcelWriter(output_path + output_name, engine='xlsxwriter')

    df_avg_income.to_excel(writer, sheet_name='Dochód i populacja', float_format="%.2f")
    df_stats_woj_by_powiat.to_excel(writer, sheet_name='Statystyki województw (powiaty)', float_format="%.2f")
    df_stats_woj_by_gmina.to_excel(writer, sheet_name='Statystyki województw (gminy)', float_format="%.2f")
    df_stats_powiat_by_gmina.to_excel(writer, sheet_name='Statystyki powiatów (gminy)', float_format="%.2f")
    
    writer.save()

