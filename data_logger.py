# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:20:12 2026

@author: Majdo
"""

import datetime
import tzlocal


def save_data(filename, timestamp, temp, hum, lum):
    date = datetime.datetime.fromtimestamp(timestamp, tzlocal.get_localzone())
    if date.day < 10:
        dateday = '0'+str(date.day)
    else:
        dateday = str(date.day)

    if date.month < 10:
        datemonth = '0'+str(date.month)
    else:
        datemonth = str(date.month)
    dateyear = str(date.year)[2:]
    if date.hour < 10:
        datehour = '0'+str(date.hour)
    else:
        datehour = str(date.hour)
    if date.minute < 10:
        dateminute = '0'+str(date.minute)
    else:
        dateminute = str(date.minute)
    if date.second < 10:
        datesecond = '0'+str(date.second)
    else:
        datesecond = str(date.second)

    with open(filename, 'a', newline='') as f:

        # if not file_exists:
        #     f.write(
        #         "day\tmonth\tyear\thour\tminute\tsecond\tTemperature\tHumidity\tLuminosity\n")
        #     print(
        #         "day\tmonth\tyear\thour\tminute\tsecond\tTemperature\tHumidity\tLuminosity\n")

        f.write(
            f'{dateday}\t{datemonth}\t{dateyear}\t{datehour}\t{dateminute}\t{datesecond}\t{temp}\t{hum}\t{lum}\n')
        print(f'{dateday}\t{datemonth}\t{dateyear}\t{datehour}\t{dateminute}\t{datesecond}\t{temp}\t{hum}\t{lum}\n')
