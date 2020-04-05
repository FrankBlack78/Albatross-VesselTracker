# Albatross / VesselTracker
This program is for retrieving ship positions and showing them on a map. The program is written in Python 3.

## Requirements
- Python 3 Standard Library
- Marine Traffic Client API (https://github.com/amphinicy/marine-traffic-client-api)
- Matplotlib
- Numpy
- Basemap
- OWSLib (for Basemap)
- Pillow (for Basemap)
- pyproj (for Basemap)
- pyshp (for Basemap)

### Basemap installation
Because all requirements besides Basemap are pretty standard and should lead to no problems, I would like to say some
words about the installation process for Basemap with which I struggled really hard.

If you are using conda, you should have no troubles. But I useed pip and therefore I can't say for sure.

1. Install the following libraries with `pip install <library>`
    - Numpy
    - Matplotlib
    - OWSLib
    - Pillow
    - pyproj
    - pyshp
    
2. Download Basemap...  
...but not from the official website (because in that case you have to compile the whole stuff by yourself, which I 
didn't manage to do). Instead download it from this website
(https://www.lfd.uci.edu/~gohlke/pythonlibs/). Choose the right version for your system
(e. g. basemap‑1.2.1‑cp38‑cp38‑win_amd64.whl when you are running Python 3.8 in the 64-bit version).

3. Install Basemap  
Install the downloaded file with `pip install basemap-1.2.1-cp38-cp38-win_amd64.whl`

Maybe you manage to install the stuff from the original (https://matplotlib.org/basemap/index.html). Good luck!

## API
The app uses AIS data from ships. These are accessed via an API from MarineTraffic (www.marinetraffic.com). 
At the moment the API PS07 "Single Vessel Positions" is used
(https://www.marinetraffic.com/en/ais-api-services/detail/ps07/single-vessel-positions/).
See the website for pricing information (the first 100 Credits are free for testing). Remember, that if you want to
access AIS-data collected via satellite (and not by terrestrial stations), you have to upgrade the API. A simple E-Mail
to the support should do the trick. But it is not activated by default.

## Functions
The file functions.py contains all the key-functions of the app. They can be imported with `from functions import 
<function>`.

### default_config()
To store configuration information (e. g. the MarineTraffic API) the program uses a config.ini. The function creates a
default config.ini.  
On success, the function returns `int(1)`.  
On error, the function returns `int(2)` (meaning config.ini already exists).

### alter_config(section, key, value)
Sometimes the config.ini has to be altered (e. g. to store the actual API of the user). The function alters the value
of a specific key in a specific section.  
On success, the function returns `int(1)`.  
On error, the function returns `int(2)` (meaning config.ini not found) or `int(3)` (meaning section/key not 
found in config.ini).

### read_config(section, key)
For use in the program, contents of the config.ini have to be read. The function returns specific section/key values.  
On success, the function returns `str(value)`.  
On error, the function returns `int(2)` (meaning config.ini not found) or `int(3)` (meaning section/key not 
found in config.ini).

### svp(ship_id)
Now we are talking... This function queries a single vessel position from MarineTraffic and writes the information to a 
JSON-file in the /data directory.  
The file naming-syntax is (MMSI_YYYYMMDD-HHMMSS.json). The timestamp-information is from the retrieved data in
UTC-format.  
As function-input a valid ship-MMSI is needed. Ships are identified via the Maritime Mobile Service Identity (MMSI) a 
unique 9-digit number.  
On success, the function returns `int(1)`.  
On error, the function returns `int(2)` (meaning invalid MMSI) or `int(3)` (meaning invalid API-Key).

### find_json_files(ship_id, date)
The function queries JSON-files in the /data-folder (retrieved data from the function svp). You have to provide a MMSI
and a date (in the format YYYYMMDD).  
On success, the function returns `list(JSON-files)`. If no files are found, an empty list is returned.  
On error, the function returns `int(2)` (meaning data-folder not found).

### load_json_data(filename)
For showing position data on a map, firstly the data has to be retrieved from JSON-files. Normally the function
find_json_files is the input for this function load_json_data. Therefore, the input for the function is the filename
from which the data should be retrieved.  
On success, the function returns `dict(LON,LAT,LABEL)`.  
On error, the function returns `int(2)` (meaning data-folder not found) or `int(3)` (meaning file not found).

### show_json_data(ship_id, date)
This is the second main function of the program besides svp(). It plots a Basemap and on it the retrieved ship
positions. You have to provide a MMSI and a date (in the format YYYYMMDD).  
On success, the function plots a Basemap with the positional data of the ship you are trying to track.  
On error, the function returns `int(2)` (meaning data-folder not found) or `int(3)` (meaning no files found).

## Main
The file main.py contains the user-interface and calls the functions described above. To start the program, just type
`python main.py` on your command line.

