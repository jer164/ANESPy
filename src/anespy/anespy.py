import pandas as pd
import numpy as np

class ANES(pd.DataFrame):

    def sample_year(self):
        print(self.loc[1, 'Year'])

    def split_pre_post(self):

        pre, post = [col for col in self.columns if any(match in col for match in ['PRE:', 'PRE ADMIN:'])], [col for col in self.columns if any(match in col for match in ['POST:', 'POST ADMIN:'])]

        df_pre = self[pre]
        df_post = self[post]

        return(df_pre, df_post)
    
    
def load_ANES_data(year): 
    
    vars = pd.read_csv(f"anespy/src/anespy/var_lists/{year}_varlist.csv") #get vars
    vars = dict(zip(vars['Number'], vars['Name']))
    vars = {k.upper():v for k,v in vars.items()}

    data = pd.read_csv(f'anespy/src/anespy/data/anes_timeseries_{year}.csv', low_memory=False) 

    data.drop(columns=[col for col in data if col not in vars.keys()], inplace=True)
    data.rename(columns=vars, inplace=True) 
    data.replace(" ", np.nan, inplace=True)
    
    data_obj = data.select_dtypes(['object'])
    for column in data_obj:
        data_obj[column] = data_obj[column].str.replace(r'(-1\. Inapplicable)', '-1', regex=True)
    data[data_obj.columns] = data_obj.replace('-1', np.nan)

    data.insert(0, 'Year', year)
    data = ANES(data)
    
    return data

def split_pre_post(df_in):

    pre, post = [col for col in df_in.columns if any(match in col for match in ['PRE:', 'PRE ADMIN:'])], [col for col in df_in.columns if any(match in col for match in ['POST:', 'POST ADMIN:'])]

    df_pre = df_in[pre]
    df_post = df_in[post]

    return(df_pre, df_post)
    