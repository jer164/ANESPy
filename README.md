## ANESPy

New repository for ANESPy, a package for easy retrieval and use of ANES Time Series data in Python. With this API, users can far more easily 
load in and transform ANES data for survey modeling, machine learning, and other statisical processing.

### Loading a Supplement

Retrieving a supplement by year is simple. 

```Python
>>> from anespy.core.anes import ANESTimeSeriesSupplement
>>> anes = ANESTimeSeriesSupplement(2020)
Retrieving data...
Parsing request...
>>> print(anes.data)
                          version  V200001  V160001_orig  V200002  ...           V203524  V203525           V203526  V203527
0     ANES2020TimeSeries_20220210   200015        401318        3  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
1     ANES2020TimeSeries_20220210   200022        300261        3  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
2     ANES2020TimeSeries_20220210   200039        400181        3  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
3     ANES2020TimeSeries_20220210   200046        300171        3  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
4     ANES2020TimeSeries_20220210   200053        405145        3  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
...                           ...      ...           ...      ...  ...               ...      ...               ...      ...
8275  ANES2020TimeSeries_20220210   535315            -1        1  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
8276  ANES2020TimeSeries_20220210   535360            -1        1  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
8277  ANES2020TimeSeries_20220210   535414            -1        2  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
8278  ANES2020TimeSeries_20220210   535421            -1        3  ...  -1. Inapplicable       -1  -1. Inapplicable       -1
8279  ANES2020TimeSeries_20220210   535469            -1        1  ...  -1. Inapplicable       -1  -1. Inapplicable       -1

[8280 rows x 1771 columns]
```

### Current State

Still in major overhaul, which means that documentation is a work-in-progress. I hope to have more time for this in the near future.
