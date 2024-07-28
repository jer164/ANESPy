from typing import Union, List, overload
from pandas import DataFrame as PandasDF
from polars import DataFrame as PolarsDF
from .constants import DATA_DICT
from .loaders import Requester, Transformer

class ANESTimeSeriesSupplement:
    ACTIVE = {}

    def __init__(self, year: Union[str, int], variables: List[str] = [], return_type: str = 'pandas'):
        self.year = year
        self.return_type = return_type
        self.data = self._get_data(self._return_type)
        self._variables = variables if variables else self.data.columns

    def __repr__(self):
        return f"{self.year} ANES Time Series Supplement with {len(self.variables):,} variables."

    def __str__(self):
        return f"{self.__class__.__name__}, year={self.year}"

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, supp_year):
        if supp_year in DATA_DICT:
            self._year = supp_year
            self.ACTIVE[self.year] = self
        elif supp_year not in DATA_DICT:
            raise KeyError(f"Passed year: '{supp_year}' not in data library.")
        # elif supp_year in self.ACTIVE:
        #     raise NameError(f"{supp_year} has already been downloaded as a supplement.\n{self.ACTIVE[supp_year]}")

    @property
    def variables(self):
        return self._variables

    @property
    def return_type(self):
        return self._return_type

    @return_type.setter
    def return_type(self, value:str):
        self._return_type = PandasDF() if value == 'pandas' else PolarsDF()

    @overload
    def _get_data(self, df_type: PolarsDF) -> PolarsDF:
        ...

    @overload
    def _get_data(self, df_type: PandasDF) -> PandasDF:
        ...

    def _get_data(self, df_type: Union[PandasDF, PolarsDF]) -> Union[PandasDF, PolarsDF]:
        print("Retrieving data...")
        requester = Requester(year=self.year)
        print("Parsing request...")
        transformer = Transformer(requester)
        return transformer.as_pandas() if isinstance(df_type, PandasDF) else transformer.as_polars()