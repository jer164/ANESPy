import pandas as pd
import numpy as np
from importlib.resources import files, as_file
import re
import requests 
import zipfile
import io


class ANES(pd.DataFrame):
   
    _metadata = ['year']

    @property
    def _constructor(self):
        return ANES

    def add_year(self):
        try: 
            self.insert(0, 'Year', self.year)
        except ValueError:
            print('Note: Year already added.')
            print('------------------------------------------')
            return self

    def split_pre_post(self):

        pre, post = [col for col in self.columns if any(match in col for match in ['PRE:', 'PRE ADMIN:'])], [
            col for col in self.columns if any(match in col for match in ['POST:', 'POST ADMIN:'])]

        df_pre = self[pre]
        df_post = self[post]

        return(df_pre, df_post)

    def generate_sample(self, variables, n_respondents = 1000):
        sample_df = self[variables]
        sample_df = sample_df.sample(n_respondents)
        return sample_df
    
    def convert_var_names(self):

        src = files('anespy.var_lists').joinpath(f'{self.year}_varlist.csv')
        with as_file(src) as vars:
            vars = pd.read_csv(vars)
        vars = dict(zip(vars['Number'], vars['Name']))
        vars = {k.capitalize():v for k,v in vars.items()}

        if type(self.year) == int:
            vars.update({'Year': 'Year'})
        else:
            pass
        
        if sum([len(var) for var in list(self.columns.values)])/len(self.columns.values) > 13: 
            vars = dict(map(reversed, vars.items()))
            
        else:
            self.drop(columns=[col for col in self if col not in vars.keys()], inplace=True)

            if self.year == 'cumulative':
                pass
            else:
                if self.year <= 2008:
                    duped_vars = [r'[a-zA-Z]\d\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\d\.\s', 
                    r'[a-zA-Z][0-9]+[a-zA-Z]\.\s', 
                    r'[a-zA-Z][0-9]+[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d\d\.\s']
                    
                    vars_vals = list(vars.values())

                    fixed_vals = []
                    for idx, name in enumerate(vars_vals):
                        if self.year == 2008:

                            if idx >= 402 and idx <= 817 :
                                    fixed_vals.append(re.sub('|'.join(duped_vars),'PRE: ', str(name)))
                            else: 
                                    fixed_vals.append(re.sub('|'.join(duped_vars),'POST: ', str(name)))
                        
                        elif self.year == 2004:
                            if idx >= 221 and idx <= 842 :
                                    fixed_vals.append(re.sub('|'.join(duped_vars),'PRE: ', str(name)))
                            else: 
                                    fixed_vals.append(re.sub('|'.join(duped_vars),'POST: ', str(name)))

                    fixed_vars = dict(zip(vars.keys(), fixed_vals))
                    self.rename(columns=fixed_vars, inplace=True) 
                else:
                    pass
        
        self.rename(columns=vars, inplace=True) 
    
    
def load_ANES_data(year, add_names = False): 

    data_dict = {
        'cumulative': ['https://electionstudies.org/wp-content/uploads/2022/09/anes_timeseries_cdf_csv_20220916.zip', 'anes_timeseries_cdf_csv_20220916.csv'],
        2020: ['https://electionstudies.org/wp-content/uploads/2022/02/anes_timeseries_2020_csv_20220210.zip', 'anes_timeseries_2020_csv_20220210.csv'],
        2016: ['https://electionstudies.org/wp-content/uploads/2018/12/anes_timeseries_2016.zip', 'anes_timeseries_2016_rawdata.txt'],
        2012: ['https://electionstudies.org/wp-content/uploads/2018/06/anes_timeseries_2012.zip', 'anes_timeseries_2012_rawdata.txt'],
        2008: ['https://electionstudies.org/wp-content/uploads/2018/06/anes_timeseries_2008.zip', 'anes_timeseries_2008_rawdata.txt'],
        2004: ['https://electionstudies.org/wp-content/uploads/2018/06/anes2004.zip', 'nes04dat.txt'],
        2002: ['https://electionstudies.org/wp-content/uploads/2018/06/anes_2002prepost.zip', 'anes_2002prepost_dat.txt'],
        2000: ['https://electionstudies.org/wp-content/uploads/2018/06/anes_2000prepost.zip', 'anes_2000prepost_dat.txt']}

    src = files('anespy.data')
    with as_file(files('anespy.data')) as data:
        url = data_dict[year][0]
        response = requests.get(url, stream=True)
        zipped = zipfile.ZipFile(io.BytesIO(response.content))
        zipped.extract(data_dict[year][1], path=src)

    
    src_data = files('anespy.data').joinpath(data_dict[year][1])
    with as_file(src_data) as data:
        if year == 'cumulative':
            data = pd.read_csv(data, low_memory=False)
        elif year >= 2008 and year <= 2016:
            data = pd.read_csv(data, sep = '|', low_memory=False)
        else:
            data = pd.read_csv(data, low_memory=False)

    if type(year) == int:
        data_obj = data.select_dtypes(['object'])
        for column in data_obj:
            data_obj[column] = data_obj[column].str.replace(r'(-1\. Inapplicable)', '-1', regex=True)
        data[data_obj.columns] = data_obj.replace('-1', np.nan)
    else: 
        pass
    
    data.replace(" ", np.nan, inplace=True)
    data = ANES(data)
    data.year = year

    if add_names == True:
        src = files('anespy.var_lists').joinpath(f'{year}_varlist.csv')
        data.convert_var_names()
    else:
        pass

    return data