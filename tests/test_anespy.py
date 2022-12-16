from anespy import anespy as anes
import pytest


def test_load_anes_data():
    test_years = [2000, 2004, 2008, 2012, 2016, 2020]
    for ty in test_years:
        data = anes.load_ANES_data(ty)
        assert data.year == ty

@pytest.mark.parametrize("test_year, expected", [
    ('cumulative', 'Version'),
    (2020, 'Year'),
    (2016, 'Year'),
    (2012, 'Year'),
    (2008, 'Year'),
    (2004, 'Year'),
    (2000, 'Year')
    ])

def test_add_year(test_year, expected):
    data = anes.load_ANES_data(test_year)
    data.add_year()
    assert data.columns[0] == expected

def test_var_recode():
    data = anes.load_ANES_data(2016)
    data.recode_to_char('V168520')
    assert len(data['V168520'][0]) > 3


def test_convert_var_names():
    test_years = [2000, 2004, 2008, 2012, 2016, 2020]
    for ty in test_years:
        data = anes.load_ANES_data(ty)
        data.convert_var_names
        assert sum([len(var) for var in list(data.columns.values)])/len(data.columns.values) > 7


@pytest.mark.parametrize("test_year, test_n", [
    ('cumulative', 400),
    (2020, 650),
    (2016, 400),
    (2012, 900),
    (2008, 200),
    (2004, 1100),
    (2000, 1600)
    ])

def test_generate_sample(test_year, test_n):
    data = anes.load_ANES_data(test_year)
    sample = data.generate_sample(list(data.columns.values[10:15]), n_respondents=test_n)
    assert len(sample.index) == test_n