# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:17:56 2026

@author: Majdo
"""
import serial

import time
import random
import numpy as np
import datetime


def read_serial(mode="Simulation", port='/dev/ttyACM0', baudrate=9600):

    if mode == "Real":

        try:
            # Open serial port (replace '/dev/ttyACM0' by system port ('/dev/ttyACM0', 'COM7', ...))
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            print(ser)

            print("Lecture en cours... (Ctrl+C pour arrêter)")

            while True:
                line = ser.readline().decode().strip()
                if line:

                    parts = line.split('\t')

                    if len(parts) != 9:
                        print("Format incorrect :", line)
                        continue

                    try:
                        jour, mois, annee, heure, minute, seconde = map(
                            int, parts[:6])
                        temp, hum, lum = map(float, parts[6:])

                        timestamp = datetime.datetime(2000 + annee, mois, jour,
                                                      heure, minute, seconde).timestamp()
                        line = f"{timestamp} {round(temp, 1)} {round(hum)} {round(lum)}"
                        yield line

                    except ValueError:
                        print("Erreur conversion :", line)
                        continue

        except serial.SerialException as e:
            yield e
            print(f"Erreur d'accès au port série : {e}")

        except KeyboardInterrupt:
            print("\nArrêt du programme.")

        finally:
            if 'ser' in locals() and ser.is_open:
                ser.close()

    elif mode == "Simulation":
        t = time.time()
        while True:
            temp = 25 + 3 * np.sin(t/10) + random.uniform(-1, 1)
            hum = 60 + 10 * np.sin(t/15) + random.uniform(-1, 1)
            lum = 50 + 20 * np.sin(t/5) + random.uniform(-1, 1)
            timestamp = int(time.time())
            line = f"{timestamp} {round(temp, 1)} {round(hum)} {round(lum)}"
            t += 1
            time.sleep(1)
            yield line
