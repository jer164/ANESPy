__all__ = ["DATA_DICT", "DUPED_VARS", "DUMMY_AGENT"]

DATA_DICT = {
    "cumulative": {
        "url": "2022/09/anes_timeseries_cdf_csv_20220916.zip",
        "csv_path": "anes_timeseries_cdf_csv_20220916.csv",
    },
    2020: {
        "url": "2022/02/anes_timeseries_2020_csv_20220210.zip",
        "csv_path": "anes_timeseries_2020_csv_20220210.csv",
    },
    2016: {
        "url": "2018/12/anes_timeseries_2016.zip",
        "csv_path": "anes_timeseries_2016_rawdata.txt",
    },
    2012: {
        "url": "2018/06/anes_timeseries_2012.zip",
        "csv_path": "anes_timeseries_2012_rawdata.txt",
    },
    2008: {
        "url": "2018/06/anes_timeseries_2008.zip",
        "csv_path": "anes_timeseries_2008_rawdata.txt",
    },
    2004: {"url": "2018/06/anes2004.zip", "csv_path": "nes04dat.txt"},
    2000: {
        "url": "2018/06/anes_2000prepost.zip",
        "csv_path": "anes_2000prepost_dat.txt",
    },
}

DUPED_VARS = [
    r"[a-zA-Z]\d\.\s",
    r"[a-zA-Z]\d[a-zA-Z]\.\s",
    r"[a-zA-Z]\d[a-zA-Z]\d\.\s",
    r"[a-zA-Z][0-9]+[a-zA-Z]\.\s",
    r"[a-zA-Z][0-9]+[a-zA-Z]\d[a-zA-Z]\.\s",
    r"[a-zA-Z]\d[a-zA-Z]\.\s",
    r"[a-zA-Z]\d[a-zA-Z]\.\s",
    r"[a-zA-Z]\d\d\.\s",
]

DUMMY_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
