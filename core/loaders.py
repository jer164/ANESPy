import requests
import warnings
from io import StringIO, BytesIO
import pandas as pd
import polars as pol
from typing import Union
from zipfile import ZipFile
from .constants import DATA_DICT, DUMMY_AGENT

__all__ = ["Requester", "Transformer"]

class Requester:
    def __init__(self, year: Union[int, str]):
        self.year = year
        self.content = self.take_request()

    @property
    def year(self) -> Union[int, str]:
        return self._year

    @year.setter
    def year(self, supp_year: Union[int, str]):
        if supp_year in DATA_DICT:
            self._year = supp_year
        else:
            raise KeyError(f"Passed year: '{supp_year}' not in data library.")

    @property
    def user(self) -> dict:
        return {'User-Agent': DUMMY_AGENT}

    @property
    def url(self) -> str:
        return f'https://electionstudies.org/wp-content/uploads/{DATA_DICT[self.year]["url"]}'

    @property
    def zip(self) -> ZipFile:
        return ZipFile(BytesIO(self.content))

    def take_request(self) -> bytes:
        response = requests.get(self.url, headers=self.user, stream=True)
        response.raise_for_status()  # Ensure we raise an error for bad responses
        return response.content

class Transformer:
    def __init__(self, requester: Requester):
        self.to_transform = requester

    @property
    def supp_year(self) -> Union[int, str]:
        return self.to_transform.year

    @property
    def csv_path(self) -> str:
        return DATA_DICT[self.supp_year]['csv_path']

    @property
    def data(self):
        return self.to_transform.zip.open(self.csv_path)

    def _as_string_io(self) -> StringIO:
        write = StringIO()
        self.as_pandas().to_csv(write)
        write.seek(0)
        return write

    def as_pandas(self) -> pd.DataFrame:
        with self.data as csv:
            if isinstance(self.supp_year, int) and 2008 <= self.supp_year <= 2016:
                pd_df = pd.read_csv(csv, sep='|', low_memory=False, encoding='iso-8859-1')
            else:
                pd_df = pd.read_csv(csv, low_memory=False)
        return pd_df
    
    def as_polars(self) -> pol.DataFrame:
        warnings.filterwarnings('ignore', category=UserWarning)
        if isinstance(self.supp_year, int) and 2008 <= self.supp_year <= 2016:
            pol_df = pol.read_csv(self._as_string_io())
        else:
            with self.data as csv:
                pol_df = pol.read_csv(csv, infer_schema_length=int(1e10))
        return pol_df
    


    
