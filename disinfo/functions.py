#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions
"""

import datetime as dt
import pandas as pd
import yaml

def convert_date(x):
   return dt.datetime.fromtimestamp(x)

def hello(name):
    print("Hello " + name)
    return


def date_range(x):
    early = min(x)
    late = max(x)
    return early, late, print(f"The latest date is is {late} and the earliest date is {early}")

def load_config(config_file = "config.yaml"):
    """
    Loads the config file for the reddit pipeline

    parameters
    ----------
    config_file: str
        Name of the config file. Defaults config.ymal

    returns
    -------
    Dictionary of config


    """
    config_yml = open(config_file)
    config = yaml.load(config_yml)
    return config
