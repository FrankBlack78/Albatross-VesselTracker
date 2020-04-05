#!/usr/bin/env python3

import time
from os import system, name
# Self build functions
from functions import svp
from functions import show_json_data
from functions import default_config
from functions import alter_config


# Global Variables
title = 'Albatross - VesselTracker'
options = []
info = ''


# UI-Functions

# Clear Screen
def clear_screen():
    time.sleep(1)
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# Head
def head():
    global title
    global options
    global info
    # Title
    print('+-+ +-+ +-+ +-+ +-+   +-+ +-+ +-+ +-+ +-+ +-+')
    print('|B| |L| |A| |C| |K|   |C| |o| |d| |i| |n| |g|')
    print('+-+ +-+ +-+ +-+ +-+   +-+ +-+ +-+ +-+ +-+ +-+')
    print('\n' + '-' * 45)
    print(f'Program: {title}')
    print('-' * 45)
    # Options
    print('Options:')
    for option in options:
        print(option)
    print('-' * 45)
    # Info
    print(f'Info: {info}')
    print('-' * 45)


# Main Menu
def main():
    while True:
        global options
        options = [
            '[1] - Edit MarineTraffic API',  # Not implemented yet
            '[2] - Retrieve ship position',
            '[3] - Show ship position on a map',  # Not implemented yet
            '[q] - Quit'
        ]
        global info
        info = 'Choose an option!'
        # Clear Screen
        clear_screen()
        # Head
        head()
        # User Input
        user_input = input('>>> ')
        if user_input == '1':
            print('\nGoing to Submenu 1 ...')
            sub_1()
        elif user_input == '2':
            print('\nGoing to Submenu 2 ...')
            sub_2()
        elif user_input == '3':
            print('\nGoing to Submenu 3 ...')
            sub_3()
        elif user_input == 'q':
            print('\nQuitting ...')
            clear_screen()
            print('Goodbye!')
            break
        else:
            print('\nNo valid option.')


# Sub Menu 1
def sub_1():
    while True:
        global options
        options = [
            '[1] - Create default config.ini',
            '[2] - Enter a new MarineTraffic API',
            '[r] - Return to Main Menu'
        ]
        global info
        info = 'Choose an option!'
        # Clear Screen
        clear_screen()
        # Head
        head()
        # User Input
        user_input = input('>>> ')
        if user_input == 'r':
            print('\nReturning to Main Menu ...')
            break
        elif user_input == '1':
            operation = default_config()
            if operation == 1:
                print('\nconfig.ini created. Please alter the API key for proper function.')
                continue
            elif operation == 2:
                print('\nconfig.ini already exists.')
                continue
        elif user_input == '2':
            user_input = input('Enter a valid MarineTraffic API >>> ')
            operation = alter_config('API_KEYS', 'MarineTraffic_API', str(user_input))
            if operation == 1:
                print('\nconfig.ini changed.')
                continue
            if operation == 2:
                print('\nconfig.ini not found. Create a default config.ini first.')
                continue
            if operation == 3:
                print('\nSection or key not found in config.ini. Create a default config.ini first.')
                continue
        else:
            print('\nNo valid option.')
            continue


# Sub Menu 2
def sub_2():
    while True:
        global options
        options = [
            '[r] - Return to Main Menu'
        ]
        global info
        info = 'Follow the instructions below!'
        # Clear Screen
        clear_screen()
        # Head
        head()
        # User Input
        user_input = input('Enter MMSI of the ship you want to track! (9-digit-number) >>> ')
        if user_input == 'r':
            print('\nReturning to Main Menu ...')
            break
        else:
            operation = svp(int(user_input))
            if operation == 1:
                print('\nValid ship MMSI. Position retrieved.')
                continue
            elif operation == 2:
                print('\nInvalid ship MMSI.')
                continue
            elif operation == 3:
                print('\nInvalid API-Key')
                continue
            else:
                print('\nAn unknown error occured.')
                continue


# Sub Menu 3
def sub_3():
    while True:
        global options
        options = [
            '[r] - Return to Main Menu'
        ]
        global info
        info = 'Follow the instructions below!'
        # Clear Screen
        clear_screen()
        # Head
        head()
        # User Input
        user_input_1 = input('Do you want to return to the main menu? (Enter r; otherwise enter something else) >>> ')
        if user_input_1.lower() == 'r':
            print('\nReturning to Main Menu ...')
            break
        else:
            user_input_1 = input('Enter MMSI of the ship you want to show! (9-digit-number) >>> ')
            user_input_2 = input('Enter date of data to show! (YYYYMMDD) >>> ')
            operation = show_json_data(str(user_input_1), str(user_input_2))
            if operation == 2:
                print('\nData folder not found.')
                continue
            elif operation == 3:
                print('\nNo data files found.')
                continue
            else:
                print('\nOperation successful.')
                continue


# Execute Program
if __name__ == '__main__':
    main()
