# StockPicker

This is a Python script which queries Yahoo Finance API and recommend top 10 stocks for that day based on predefined strategies.

The script works like this:

* Step 1: get all tickers as of today. Right now we get from Nasdaq FTP.
* Step 2: call Yahoo Finance to get fundamental information. We are using yfinance library for that.
* Step 3: Apply investment strategy to pick good tickers.

# Pre-Setup

# How to setup a good Python environment for macOS

### Step 1. install pyenv

https://github.com/pyenv/pyenv

Let's install pyenv so that we can switch between multiple versions of Python easily.

```
brew update
brew install pyenv
```

Add these lines to `~/.zshrc` if you are using `zsh`.
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Using pyenv to Install Python:

```
 pyenv install 3.10.3
 ```
 
 List all python version installed by `pyenv`:
 
 ```
 pyenv versions
 ```
 
 Set global python version:
 
 ```
 pyenv global 3.10.3
 ```
 
Now whenever you call python you’ll be using `Python 3.10.3`. Check it with `python --version`. 


To set a Python version for a specific project, `cd` into your project and then run:

```
pyenv local <python-version>
```

That will create a `.python-version` file in the current directory which `pyenv` will see and use to set the appropriate version. __Please always set the local version python if possible.__ It also helps with `pip`: https://stackoverflow.com/questions/52060867/how-to-use-pip-for-pyenv.


Further Read:  
* https://realpython.com/intro-to-pyenv/
* https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe
* https://jordanthomasg.medium.com/python-development-on-macos-with-pyenv-2509c694a808

### Step 2. install pyenv-virtualenv

https://github.com/pyenv/pyenv-virtualenv

```
brew install pyenv-virtualenv
```

Add this line `eval "$(pyenv virtualenv-init -)"` to `~/.zshrc` if you are using `zsh`.

Some useful commmands:

```
pyenv virtualenv 3.7.3 my-virtual-env // Create a new virtual environment my-virtual-env
pyenv activate my-virtual-env // Enter the virtual environment
pyenv deactivate // Exit the virtual environment
pyenv virtualenvs // List all the virtual environments
pyenv uninstall my-virtual-env // Delete the virtual environment
```


# Development

To enter/exit virtual environment: 

```
pyenv activate my-virtual-env // Enter the virtual environment
pyenv deactivate // Exit the virtual environment
```

To install/uninstall package:

```
pip install <PackageName>
pip uninstall <PackageName>
```

`pip freeze > requirements.txt ` can be used to generate `requirements.txt`.


Run the script: 

```
python ./StockPicker.py -t AAPL AMZN SQ FB TSLA GOOGL // get stock information and pick good stock among them
python ./StockPicker.py -h // Show help
python ./StockPicker.py // get all live tickers from Nasdaq and pick good stock among them.
```