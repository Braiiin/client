#Braiiin Presentation Tier

front-end visuals

##Developer Version


1. Make sure Python3, Pip, and Mongodb are installed.
1. Create new virtaulenv named "env" `python3 -m venv env`.
1. Launch virtualenv `source env/bin/activate`.
1. Install requirements `pip3 install -r requirements.txt`.
1. Launch service. `python3 run.py`.

*For subsequent runs, after installation, you can use `source activate.sh`.*

## Developer Guidelines

###Docstrings

All docstrings should use one of the following two formats:

Minimal
```
"""Basic docstring for the method or class"""
```

Detailed
```
"""
One-liner description

Information
-----------
Basic information about usage

Detail
------
Optional section with clarifications that may not be needed

Example
-------
Sample Usage
"""
```

###Separation of Purpose