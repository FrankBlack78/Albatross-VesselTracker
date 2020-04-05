#!/usr/bin/env python3

from marinetrafficapi import MarineTrafficApi
from marinetrafficapi import MarineTrafficRequestApiException
import json
import os
import re
import configparser
from configparser import NoSectionError
import fnmatch
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


"""
Operation: Create default config.ini
Requirements: none
Input: none
Output:
    Success:
        int(1)
    Error:
        int(
            2 = config.ini already exists
        )
"""


def default_config():
    if os.path.isfile('config.ini') is True:
        return 2
    else:
        config = configparser.ConfigParser()
        config['DEFAULT'] = {}
        config['PATHS'] = {'data': '/data'}
        config['API_KEYS'] = {'MarineTraffic_API': 'None'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return 1


"""
Operation: Alter config.ini
Requirements: none
Input: str(section), str(key), str(value)
Output:
    Success:
        int(1)
    Error:
        int(
            2 = config.ini not found
            3 = Section/Key not found in config.ini
        )
"""


def alter_config(section, key, value):
    if os.path.isfile('config.ini') is True:
        config = configparser.RawConfigParser()
        config.read('config.ini')
        check_section = section in config
        if check_section is True:
            config.set(section, key, value)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            return 1
        else:
            return 3
    else:
        return 2


"""
Operation: Read config.ini
Requirements: none
Input: str(section), str(key), str(value)
Output:
    Success:
        str(value)
    Error:
        int(
            2 = config.ini not found
            3 = Section/Key not found
        )
"""


def read_config(section, key):
    if os.path.isfile('config.ini') is True:
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            return config[section][key]
        except (NoSectionError, KeyError):
            return 3
    else:
        return 2


"""
Operation: Query a single vessel position from MarineTraffic and write information to a JSON-file
Requirements: API from MarineTraffic (www.marinetraffic.com)
Input: MMSI as str(ship_id) 
Output:
    Success:
        int(1)
    Error:
        int(
            2 = Invalid MMSI
            3 = Invalid API-Key
        )
"""


def svp(ship_id='311000608'):  # 311000608 = MS ARTANIA, 211556210 = SY LALUMA
    # Check if input is a valid ship MMSI (9-digit-number between 200000000 and 799999999)
    ship_id = str(ship_id)
    try:
        re.search(r'^([234567])(\d{8})$', ship_id)
        ship_id = int(ship_id)
    except ValueError:
        return 2
    # API-TYPE: (PS07) Single Vessel Positions
    try:
        api = MarineTrafficApi(api_key=read_config('API_KEYS', 'MarineTraffic_API'), debug=False)  # debug=True
        request = api.single_vessel_positions(
            timespan=30,  # The maximum age, in minutes, of the returned positions. Default is 2, maximum value is 2880.
            msg_type='simple',  # simple | extended
            protocol='jsono',  # xml | csv | json | jsono (object)
            mmsi=ship_id,  # MMSI number
        )
    except MarineTrafficRequestApiException:
        # debug_data = api.request.debug.show()
        # print(debug_data)
        return 3
    # Raw data from API call (json, csv or xml)
    raw_data = request.raw_data
    data = json.loads(raw_data)
    # Extract information for file-naming from data
    mmsi = data[0]['MMSI']
    timestamp = data[0]['TIMESTAMP']
    # Transform information for file-naming
    timestamp = re.sub('[-:]', '', timestamp)
    timestamp = re.sub('[T]', '-', timestamp)
    # Create file-name
    filename = mmsi + '_' + timestamp + '.json'
    # Check if data folder is there and if not, create it
    folder = 'data'
    check_folder = os.path.isdir(folder)
    if not check_folder:
        os.makedirs(folder)
    # Save data to file
    path_filename = os.getcwd() + '\\data\\' + filename
    with open(path_filename, 'w') as f:
        json.dump(data, f, indent=4)
    # Return 1 for successful operation
    return 1


"""
Operation: Find JSON-files in data-folder
Requirements: none
Input: int/str(ship_id), int/str(date) / Default = all JSON-files
Output:
    Success:
        list(JSON-files)
    Error:
        int(
            2 = data-folder not found
        )
"""


def find_json_files(ship_id='', date=''):
    # Convert input to string for concatenation
    ship_id = str(ship_id)
    date = str(date)
    # Check if data-folder is there
    if os.path.isdir('data') is True:
        # Find json-files in data-folder
        result = list()
        for file in os.listdir(os.getcwd() + '\\data\\'):
            if fnmatch.fnmatch(file, '*' + ship_id + '*.json'):  # MMSI
                if fnmatch.fnmatch(file, '*' + date + '*.json'):  # Date
                    result.append(str(file))
        return result
    else:
        return 2


"""
Operation: Load data from a JSON-file in the data-folder
Requirements: none
Input: str(filename)
Output:
    Success: dict(LON,LAT,LABEL)
    Error:
        int(
            2 = data-folder not found
            3 = file not found
        )
"""


def load_json_data(filename):
    # Check if data-folder is available
    if os.path.isdir('data') is True:
        # Check if file is available
        if os.path.isfile(os.getcwd() + '\\data\\' + filename) is True:
            result = dict()
            # Load data
            with open(os.getcwd() + '\\data\\' + filename, 'r') as f:
                data = json.load(f)
                result.update({'LON': data[0]['LON']})
                result.update({'LAT': data[0]['LAT']})
                result.update({'LABEL': data[0]['TIMESTAMP']})
            return result
        else:
            return 3
    else:
        return 2


"""
Operation: Show ships position on a Basemap
Requirements: find_json_files(), load_json_data()
Input: str(ship_id, date), Date is in the format YYYYMMDD
Output:
    Success: Basemap projection with ship positions of the chosen date
    Error:
        int(
            2 = data-folder not found
            3 = no data-files found
        )
"""


def show_json_data(ship_id='', date=''):
    # Check if data-folder exists
    if os.path.isdir('data') is True:
        files = find_json_files(ship_id, date)
        # Check if files exists
        if len(files) == 0:
            return 3
        else:
            # Collect and process data
            ship_data = list()
            for file in files:
                ship_data.append(load_json_data(file))
            dataset_count = len(ship_data)
            lons = list()
            lats = list()
            labels = list()
            for i in range(dataset_count):
                lons.append(ship_data[i]['LON'])
                lats.append(ship_data[i]['LAT'])
                labels.append(ship_data[i]['LABEL'])
            lons = list(map(float, lons))
            lats = list(map(float, lats))
            # Plot map
            plt.figure(figsize=(9.8, 5))  # Mapsize (default 6.4, 4.8)
            m = Basemap(projection='robin', lon_0=0, resolution='c')  # (c)rude, (l)ow, (i)ntermediate, (h)igh, (f)ull
            m.drawcoastlines(linewidth=0.5, color='k')  # Draw Coastlines
            m.drawcountries(color='grey')  # Draw Countries
            m.fillcontinents(color='white')
            m.drawmapboundary(color='yellowgreen', linewidth=5)
            m.drawparallels(np.arange(-90, 90, 15), labels=[True, False, False, False], zorder=0)
            m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1], zorder=0)
            plt.suptitle('VesselTracker', fontsize=15)
            plt.title('MMSI: ' + str(ship_id) + ' / DATE: ' + str(date), fontsize=10, pad=15)
            # Plot positions
            for i in range(dataset_count):
                lon, lat = lons[i], lats[i]
                xpt, ypt = m(lon, lat)  # convert to map projection coords.
                m.plot(xpt, ypt, 'ro')  # plot a red dot on position
                plt.text(xpt + 150000, ypt + 150000, labels[i], fontsize=10)  # plot the label with a little offset
            plt.show()
    else:
        return 2
