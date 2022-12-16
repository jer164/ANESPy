# ANESPy

A package for easy import and cleaning of ANES data. 

## Installation

```bash
$ pip install anespy
```

## Usage

```ANESPy``` is intended to bypass the numerous headaches involved in research using ANES data. Though ANES data are used frequently in the social sciences (particularly political science), bringing ANES data into a project can be a difficult task requiring several recodes. The data are only available as CSVs for 2020 and cumulative data files, while the rest are made available as files for STATA and SPSS, or as an ASCII table. When these data are read in, the variables are not named and require that you reference a codebook to understand what they are. Some of the files are even incomplete, or presented with empty cells instead of any specific marker for missing data. 

By using ```ANESPy```, you can bring in data for a selected year (going back to 2000) and work with ANES data as its own class of DataFrame. Aside from speeding up the data acquisition process, this package provides the user with methods specific to the ANES class that expedite challenging transformations. Though there are aspects of this package still in development, its current functionality as a pseudo-API greatly improves the synergy between ANES research and Python-based statistical analysis. 


## Example

Say you wanted to get the 2012 version of the ANES Time Series, but you only wanted the Pre-Election variables. This can be done simply:

```python
import anespy.anespy

data = anespy.load_ANES_data(2012)
data.conver_var_names()
data_pre, data_post = data.split_pre_post()
```

Using just three functions, you now have a DataFrame containing all the pre-election variables for 2012. It can also be exported using any of the available ```to_``` methods from Pandas. 

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`anespy` was created by Jackson Rudoff. It is licensed under the terms of the MIT license.

## ANES Terms of Use

By using these data, you agree to the terms of use established by the ANES:

- Use these datasets solely for research or statistical purposes and not for investigation of specific survey respondents.
- Make no use of the identity of any survey respondent(s) discovered intentionally or inadvertently, and to advise ANES of any such discovery (anes@electionstudies.org)
- Cite ANES data and documentation in your work that makes use of the data and documentation. Authors of publications based on ANES data should send citations of their published works to ANES for inclusion in our bibliography of related publications.
- You acknowledge that the original collector of the data, ANES, and the relevant funding agency/agencies bear no responsibility for use of the data or for interpretations or inferences based upon such uses.

The ANES is not responsible for any mistakes *I* made with these datasets and the packaged functions. 


## Credits

`anespy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
