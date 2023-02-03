import mysql.connector
from pathlib import Path

# read the database configuration file
current_path = Path(__file__).resolve().parents[1]
config_file_path = Path(current_path, 'config','db.txt')
config_file = open(config_file_path,'r')
Lines = config_file.readlines()
config_file.close()

config_list = []
for line in Lines:
    processed_info = line.rstrip().split(":")
    config_list.append(processed_info)
config_dict = dict(config_list)

# create database if not exist
try:
    main_db = mysql.connector.connect(  host = config_dict['host'],
                                        port = config_dict['port'],
                                        user = config_dict['user'],
                                        password = config_dict['password']     )
    main_cursor = main_db.cursor()
    query_string = "CREATE DATABASE IF NOT EXISTS " + config_dict['database']
    main_cursor.execute(query_string)
    main_cursor.close()
    main_db.close()
except Exception as Ex:
    print("Error: %s"%(Ex))

# create tables if not exist
try:
    main_db = mysql.connector.connect(  host = config_dict['host'],
                                        port = config_dict['port'],
                                        user = config_dict['user'],
                                        password = config_dict['password'],
                                        database = config_dict['database'])
    main_cursor = main_db.cursor()
    # create registered_devices
    query_string = "CREATE TABLE IF NOT EXISTS registered_devices (" \
                    "device_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"\
                    "registered_time DATETIME DEFAULT CURRENT_TIMESTAMP,"\
                    "mac_address VARCHAR(17),"\
                    "device_name VARCHAR(100),"\
                    "status BOOL DEFAULT 1)"
    main_cursor.execute(query_string)
    # create logging_messages
    query_string = "CREATE TABLE IF NOT EXISTS logging_rs485_message (" \
                    "message_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"\
                    "logging_time DATETIME DEFAULT CURRENT_TIMESTAMP,"\
                    "device_id INTEGER,"\
                    "bus_number INTEGER,"\
                    "message VARCHAR(256))"
    main_cursor.execute(query_string)
 
    main_cursor.close()
    main_db.close()
except Exception as Ex:
    print("Error: %s"%(Ex))