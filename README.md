# StockPicker

This is a Python script which queries Yahoo Finance API and recommend top 10 stocks for that day based on predefined strategies.

The script works like this:

* Step 1: get all tickers as of today. Right now we get from Nasdaq FTP.
* Step 2: call Yahoo Finance to get fundamental information.
* Step 3: Apply investment strategy to pick good tickers.

# Development

Please use [pyenv](https://github.com/pyenv/pyenv) to manage python versions, and `pyenv local <python-version>` to setup the python version for the project.

Please use [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage a virtual environment for the project.

`pip freeze > requirements.txt ` can be used to generate `requirements.txt`.

### Run the script

```
python ./StockPicker.py 
```


# Dependency
https://pypi.python.org/pypi/yahoo-finance
