import pytest
from unittest.mock import patch
from anespy.core.loaders import Requester
from anespy.core.constants import DATA_DICT, DUMMY_AGENT
from io import BytesIO
from zipfile import ZipFile
import requests

# Mock data
TEST_DICT = DATA_DICT[2020]
TEST_AGENT = {"User-Agent": DUMMY_AGENT}


@pytest.fixture
def real_response():
    url = TEST_DICT["url"]
    response = requests.get(
        f"https://electionstudies.org/wp-content/uploads/{url}",
        headers=TEST_AGENT,
    )
    response.raise_for_status()
    return response


@pytest.fixture
def real_zip(real_response):
    return ZipFile(BytesIO(real_response.content))


@pytest.fixture
def requester():
    with patch.dict("anespy.core.constants.DATA_DICT", DATA_DICT):
        return Requester(2020)


def test_year_setter_valid(requester):
    assert requester.year == 2020


def test_year_setter_invalid():
    with patch.dict("anespy.core.constants.DATA_DICT", DATA_DICT):
        with pytest.raises(KeyError):
            Requester(2019)


def test_user_property(requester):
    assert requester.user == {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }


def test_url_property(requester):
    assert (
        requester.url
        == "https://electionstudies.org/wp-content/uploads/2022/02/anes_timeseries_2020_csv_20220210.zip"
    )


def test_take_request(requester, real_response):
    with patch("requests.get", return_value=real_response):
        content = requester.take_request()
        assert content == real_response.content


def test_zip_property(requester, real_response, real_zip):
    with patch("requests.get", return_value=real_response):
        requester.content = requester.take_request()
        with patch("zipfile.ZipFile", return_value=real_zip):
            zip_file = requester.zip
            assert isinstance(zip_file, ZipFile)
