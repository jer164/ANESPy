import pytest
from unittest.mock import patch, MagicMock
from anespy.core.anes import ANESTimeSeriesSupplement
from anespy.core.constants import DATA_DICT
from pandas import DataFrame as PandasDF
from polars import DataFrame as PolarsDF

# Mock data and constants
DATA_DICT = DATA_DICT[2020]
DUPED_VARS = []

@pytest.fixture
def mock_requester_transformer():
    with patch('anespy.core.loaders.Requester') as MockRequester, \
         patch('anespy.core.loaders.Transformer') as MockTransformer:
        mock_requester = MockRequester.return_value
        mock_transformer = MockTransformer.return_value
        mock_transformer.as_pandas.return_value = PandasDF()
        mock_transformer.as_polars.return_value = PolarsDF()
        yield mock_requester, mock_transformer

def test_initialization(mock_requester_transformer):
    anes = ANESTimeSeriesSupplement(year=2020, variables=['var1', 'var2'], return_type='pandas')
    assert anes.year == 2020
    assert anes.variables == ['var1', 'var2']
    assert isinstance(anes.return_type, PandasDF)

def test_year_property(mock_requester_transformer):
    anes = ANESTimeSeriesSupplement(year=2020)
    assert anes.year == 2020
    with pytest.raises(KeyError):
        ANESTimeSeriesSupplement(year=2019)

def test_return_type_property(mock_requester_transformer):
    anes = ANESTimeSeriesSupplement(year=2020, return_type='polars')
    assert isinstance(anes.return_type, PolarsDF)
    anes.return_type = 'pandas'
    assert isinstance(anes.return_type, PandasDF)

def test_get_data_pandas(mock_requester_transformer):
    anes = ANESTimeSeriesSupplement(year=2020, return_type='pandas')
    data = anes._get_data(anes.return_type)
    assert isinstance(data, PandasDF)

def test_get_data_polars(mock_requester_transformer):
    anes = ANESTimeSeriesSupplement(year=2020, return_type='polars')
    data = anes._get_data(anes.return_type)
    assert isinstance(data, PolarsDF)