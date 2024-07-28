import pandas as pd
import numpy as np
from importlib.resources import files, as_file
from pandas.core.common import SettingWithCopyWarning
import pickle
import re
import requests 
import zipfile
import io
import warnings

######### Suppress FutureWarnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

######### DICTIONARIES AND RE-USED VALUES

data_dict = {
        'cumulative': ['2022/09/anes_timeseries_cdf_csv_20220916.zip', 'anes_timeseries_cdf_csv_20220916.csv'],
        2020: ['2022/02/anes_timeseries_2020_csv_20220210.zip', 'anes_timeseries_2020_csv_20220210.csv'],
        2016: ['2018/12/anes_timeseries_2016.zip', 'anes_timeseries_2016_rawdata.txt'],
        2012: ['2018/06/anes_timeseries_2012.zip', 'anes_timeseries_2012_rawdata.txt'],
        2008: ['2018/06/anes_timeseries_2008.zip', 'anes_timeseries_2008_rawdata.txt'],
        2004: ['2018/06/anes2004.zip', 'nes04dat.txt'],
        2000: ['2018/06/anes_2000prepost.zip', 'anes_2000prepost_dat.txt']}

duped_vars = [r'[a-zA-Z]\d\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\d\.\s', 
                    r'[a-zA-Z][0-9]+[a-zA-Z]\.\s', 
                    r'[a-zA-Z][0-9]+[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d[a-zA-Z]\.\s', 
                    r'[a-zA-Z]\d\d\.\s']

######### ANES CLASS

class ANES_deprecated(pd.DataFrame):
   
    _metadata = ['year']

    @property
    def _constructor(self):
        return ANES

    def add_year(self):
        '''
        Insert a year column into an ANES object. 

        Parameters:
        -----------
        self : anespy.anespy.ANES
            An ANES instance.  

        Returns:
        --------
        pandas.core.series.Series: 
            A column filled with n rows of the ANES object's year. 

        Example:
        --------
        >>> import anespy.anespy as anes
        >>> data=load_ANES_data(2020)
        >>> data.add_year()
        >>> data.iloc[:, :5].head()
           Year  version  V200001  V160001_orig  V200002
        0  2020       -1   200015        401318        3
        1  2020       -1   200022        300261        3
        2  2020       -1   200039        400181        3
        3  2020       -1   200046        300171        3
        4  2020       -1   200053        405145        3
        '''
        if type(self.year) == int:
            try: 
                self.insert(0, 'Year', self.year)
            except ValueError:
                print('Note: Year already added.')
                print('------------------------------------------')
                return self
        else:
            print('Cumulative data does not have a year.')


    def convert_var_names(self, drop_extra = True):
        '''
        Renames variables (column headers) to full, context-inclusive name from ANES codebook. Can also be used 
        backwards to rename variables to their "V____"-formatted name. 

        Parameters:
        -----------
        self : anespy.anespy.ANES
            An ANES instance.
        drop_extra : bool
            A boolean indicating where columns not present in codebook should be dropped. Defaults to True.

        Returns:
        --------
        self: anespy.anespy.ANES
            An ANES object containing the selected colums and *n* number of respondents. 

        Example:
        --------
        >>> import anespy.anespy as anes
        >>> data=load_ANES_data(2004)
        >>> data.convert_var_names()
        Converted to named variables.
        >>> data.iloc[:, 100:102].head()
           PreAdmin.37b. Comment: positive - enjoy surveys  PreAdmin.37c. Comment: other positive
        0                                                5                                      1
        1                                                5                                      5
        2                                                5                                      1
        3                                                5                                      1
        4                                                5                                      5
        # You can still convert these back!
        >>> data.convert_var_names()
        Converted to numbered variables.
           V042037b  V042037c
        0         5         1
        1         5         5
        2         5         1
        3         5         1
        4         5         5
        '''

        print_out= 'named variables'
        src = files('anespy.var_lists').joinpath(f'{self.year}_varlist.csv')
        with as_file(src) as new_vars:
            new_vars = pd.read_csv(new_vars)
        new_vars = dict(zip(new_vars['Number'], new_vars['Name']))
        if self.year != 2012:
            new_vars = {k.capitalize():v for k,v in new_vars.items()}
        else:
            pass

        if type(self.year) == int:
            new_vars.update({'Year': 'Year'})
        else:
            pass
        
        if sum([len(var) for var in list(self.columns.values)])/len(self.columns.values) > 18:
            if self.year in [2000, 2004, 2008]:
                src_vars = files('anespy.data')
                with as_file(src_vars) as data_out:
                    new_vars = pickle.load(open(f"{data_out}/updated_vars{self.year}.pkl", "rb"))
            else:
                pass
            rev_vars = dict(map(reversed, new_vars.items()))
            self.rename(columns=rev_vars, inplace=True)
            print_out = 'numbered variables'
            
        else:
            if drop_extra == True:
                self.drop(columns=[col for col in self if col not in new_vars.keys()], inplace=True)
            else:
                pass

            if self.year == 'cumulative':
                self.rename(columns=new_vars, inplace=True) 
            else:
                if self.year <= 2008:
    
                    new_vars_vals = list(new_vars.values())

                    fixed_vals = []
                    for idx, name in enumerate(new_vars_vals):
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
                        
                        elif self.year == 2000:
                            if idx >= 305 and idx <= 1112 :
                                    fixed_vals.append(re.sub('|'.join(duped_vars),'PRE: ', str(name)))
                            else: 
                                    fixed_vals.append(re.sub('|'.join(duped_vars),'POST: ', str(name)))


                    fixed_vars = dict(zip(new_vars.keys(), fixed_vals))
                    self.rename(columns=fixed_vars, inplace=True) 
                    
                    src_vars = files('anespy.data')
                    with as_file(src_vars) as data_out:
                        pickle.dump(fixed_vars, open(f"{data_out}/updated_vars{self.year}.pkl", "wb"))
                else: 
                    self.rename(columns=new_vars, inplace=True)
        print(f'Converted to {print_out}.')
    
    def recode_to_char(self, col_in):
        '''
        Recode an ANES column from numeric to a textual category.   

        Parameters:
        -----------
        self : anespy.anespy.ANES
            An ANES instance. 
        
        col_in: str
            Name of the column to be transformed. 

        Returns:
        --------
        pandas.core.series.Series
            The recoded column. 

        Example:
        
        >>> import anespy.anespy as anes
        >>> data=anes.load_ANES_data(2008)
        >>> data['V085409a']
        0       12
        1       -1
        2       12
        3       12
        4       13
                ..
        2317    13
        2318    12
        2319    12
        2320    12
        2321     7
        Name: V085409a, Length: 2322, dtype: int64
        >>> data.recode_to_char('V085409a')
        >>> data['V085409a']
        0                  Negative - too complicated
        1                                Inapplicable
        2                  Negative - too complicated
        3                  Negative - too complicated
        4       Negative - boring/tedious/repetitious
                                ...                  
        2317    Negative - boring/tedious/repetitious
        2318               Negative - too complicated
        2319               Negative - too complicated
        2320               Negative - too complicated
        2321                              Unavailable
        Name: V085409a, Length: 2322, dtype: category
        Categories (6, object): ['Inapplicable', 'Negative - boring/tedious/repetitious',
                                'Negative - general', 
                                'Negative - too complicated', 
                                'Negative - too long',
                                'Unavailable'] 
        '''

        try: 
            assert type(self[col_in].iloc[0]) != str, 'Column data must be numeric.'

            src_var_labs = files('anespy.data')
            with as_file(src_var_labs) as lab_path:
                recode_dict = pd.read_csv(f'{lab_path}/{self.year}_labels_values.csv')
            recode_dict.drop(columns=recode_dict.columns[0], inplace=True)
            recode_dict['label'] = recode_dict['label'].str.replace(r'-?\d+\.\s', '')
            recode_dict['value'] = recode_dict['value']
            if self.year != 2012:
                recode_dict['id'] = recode_dict['id'].apply(lambda x: x.capitalize())
            else:
                pass
            
            if len(col_in) > 10 and '_' not in col_in:
                src = files('anespy.var_lists').joinpath(f'{self.year}_varlist.csv')
                with as_file(src) as new_vars:
                    new_vars = pd.read_csv(new_vars)
                new_vars = dict(zip(new_vars['Number'], new_vars['Name']))
                if self.year != 2012:
                    new_vars = {k.capitalize():v for k,v in new_vars.items()}
                else:
                    pass
                recode_dict['id'] = recode_dict['id'].map(new_vars)
                col_in = new_vars[col_in]
            else: 
                pass

            recode_dict = recode_dict.set_index(['id', 'value'])
            recode_dict = recode_dict.T.to_dict('list')

            for idx, row in enumerate(self[col_in]):
                if self.year in [2000, 2008]:
                    tmp_tuple = (self[col_in].name, int((row)))
                else:
                    tmp_tuple = (self[col_in].name, str((row)))
                if len(str(tmp_tuple)) < 30 and tmp_tuple in recode_dict.keys():
                    self[col_in].iloc[idx] = recode_dict[tmp_tuple][0]
                elif self[col_in].iloc[idx] < 0:
                    self[col_in].iloc[idx] = 'Inapplicable'
                else:
                    self[col_in].iloc[idx] = 'Unavailable'
            self[col_in].astype('category')
        except KeyError:
            print("Please use original variable names.")
    
    def split_pre_post(self):
        '''
        Split an ANES object between its Pre and Post-election variables. 

        Parameters:
        -----------
        self: anespy.anespy.ANES
            An ANES instance.

        Returns:
        --------
        df_pre : anespy.anespy.ANES
            An ANES instance.

        df_post : anespy.anespy.ANES
            An ANES instance.

        Example:
        
        >>> import anespy.anespy as anes
        >>> data=anes.load_ANES_data(2016)
        >>> data.convert_var_names()
            Converted to named variables.
        >>> data_pre, data_post = data.split_pre_post()
        >>> data_pre.head()
        PRE: FTF ONLY: Audio Consent ...PRE ADMIN: Elapsed time interview...
        0                             1  ...                       72.433333       
        1                             1  ...                       55.433333       
        2                             1  ...                       54.166667       
        3                             1  ...                       58.500000       
        4                             1  ...                       85.016667 
        '''

        pre, post = [col for col in self.columns if any(
            match in col for match in ['PRE:', 'PRE ADMIN:', 'Pre ', 'Pre.', 'Pre-'])], [
            col for col in self.columns if any(
                match in col for match in ['POST:', 'POST ADMIN:', 'Post ', 'Post.', 'Post-'])]

        df_pre = self[pre]
        df_post = self[post]

        return(df_pre, df_post)


    def generate_sample(self, variables, n_respondents = 1000):
        '''
        Create a sample of data of *n* respondents from an ANES object.

        Parameters:
        -----------
        self : anespy.anespy.ANES
            An ANES instance.
        variables : str or list()
            A string or list of string names for the column(s) being sampled.
        n_respondents : int
            Size of the sample (defaults to 1000)

        Returns:
        --------
        sample_df: anespy.anespy.ANES
            An ANES object containing the selected colums and *n* number of respondents. 

        Example:
        --------
        >>> import anespy.anespy as anes
        >>> data=load_ANES_data(2008)
        >>> sample =  data.generate_sample(['V082423g', 'V082424'], n_respondents = 500)
        >>> sample.head()
              V082423g  V082424
        1886         2        2
        1294         3        1
        472          3        1
        135          5        1
        139          7        2
        '''

        sample_df = self[variables]
        sample_df = sample_df.sample(n_respondents)
        return sample_df
    

######### DATA FUNCTIONS

def editions():
    '''
        Returns the editions of the ANES Time Series the package contains. 

        Parameters:
        -----------
        None 

        Returns:
        --------
        None

        Example:
        --------
        >>> import anespy.anespy as anes
        >>> anes.editions()
        cumulative
        2020
        2016
        2012
        2008
        2004
        2000
        '''

    for keys, values in data_dict.items():
        print(keys)
    
def load_ANES_data(year, add_names = False): 
    '''
        Acquires data from the ANES internal API as a zip file, before unzipping and instantiating an ANES object
        for the selected year. 

        Parameters:
        -----------
        year : int
            Year of the data to be acquired. 
        add_names : bool
            A boolean indicating whether the convert_var_names() method should be applied on ingest. Defaults to False.

        Returns:
        --------
        data: anespy.anespy.ANES
            An ANES object containing the Time Series data from the selected year. 

        Example:
        --------
        >>> import anespy.anespy as anes
        >>> data=load_ANES_data(2000, add_names = False) #not adding names
        Converted to named variables.
        >>> data.iloc[:, :5].head()
           VERSION  DSETID  V000001  V000001a  V000002
        0       -1      -1        1       787   1.2886
        1       -1      -1        2      1271   0.8959
        2       -1      -1        3       934   1.0454
        3       -1      -1        4       285   0.6005
        4       -1      -1        5       191   1.9270
        '''

    src = files('anespy.data')
    with as_file(src) as data:
        param = data_dict[year][0]
        response = requests.get(f'https://electionstudies.org/wp-content/uploads/{param}', stream=True)
        zipped = zipfile.ZipFile(io.BytesIO(response.content))
        zipped.extract(data_dict[year][1], path=src)

    
    src_data = files('anespy.data').joinpath(data_dict[year][1])
    with as_file(src_data) as in_data:
        if year == 'cumulative':
            data = pd.read_csv(in_data, low_memory=False)
        elif year >= 2008 and year <= 2016:
            data = pd.read_csv(in_data, sep = '|', low_memory=False, encoding='iso-8859-1')
        else:
            data = pd.read_csv(in_data, low_memory=False)

    if type(year) == int:
        data_obj = data.select_dtypes(['object'])
        for column in data_obj:
            data_obj[column] = data_obj[column].str.replace(r'(\. Inapplicable)|(\. Inap)', '').replace(
                r'^\s*$', np.nan, inplace= True)
        data[data_obj.columns] = data_obj.replace('-1', -1)

        data_num = data.select_dtypes('number') 
        data_num = data_num.applymap(lambda x: -1 if x < 0 else x)
        data[data_num.columns] = data_num

    else: 
        pass
    
    data.fillna(-1, inplace=True)
    data = ANES(data)
    data.year = year

    if add_names == True:
        src = files('anespy.var_lists').joinpath(f'{year}_varlist.csv')
        data.convert_var_names()
    else:
        pass

    return data