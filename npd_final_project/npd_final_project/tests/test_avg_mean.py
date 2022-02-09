from calculate_statistics.functions import *
import pandas as pd


df = pd.DataFrame({
                    "Group": ['1', '1', '1', '2'],
                    "City": ['A','B','C','D'], 
                    "Population": [2, 1, 2, 1],
                    "Income": [1000, 200, 150, 0]
                  })


def test_avg_mean():

    df_agg = calculate_weigted_average(input_table = df, variable = 'Income', weight = 'Population', by = 'Group', output_variable = 'avg_mean')
    
    assert df_agg.loc['1','avg_mean'] == 500
    assert df_agg.loc['2','avg_mean'] == 0
    
    