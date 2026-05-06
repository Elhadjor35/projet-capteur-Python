#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:56:54 2026

@author: elhadj
"""
import pandas as pd
file = '09021704.TXT'
df = pd.read_table(
    file, sep='\s+',  # Choisir le nom du fichier
    names=['day', 'month', 'year', 'hour',
           'minute', 'second', "temperature", "Humidity", "Luminosity"],
    header=0, parse_dates={'Time': ['day', 'month', 'year', 'hour',
                                    'minute', 'second']},
    date_format={'Time': '%d %m %y %H %M %S'})
df2 = df.drop(df[(df["Temperature"] == 0) & (df["Luminosity"] == 0)
                 & (df["Humidity"] == 0)].index).reset_index()
df3 = df2
df3['Time'] = df2['Time'].dt.tz_localize(tz='Europe/Paris')
df3['Time_unix'] = pd.to_datetime(df3['Time']).astype(int) / 10**9
