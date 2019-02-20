# coding: utf-8

import configparser

config = configparser.ConfigParser()

config["host"] = {
    "1": "10.100.100.20",
    "2": "10.100.100.22"
}

# config["host"] = {
#     "1": "localhost:6000"
# }


with open("config.ini", "w") as file:
    config.write(file)
