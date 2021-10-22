# novramon

## _InfluxDB 2 Monitoring for Novra S300 Satellite Receiver_

_This is quick and dirty but seems to work..._

Tested on Fedora 34 and CentOS 7.

## Configuration
Create a `config.py` file that contains site specific configuration such as hostnames, passwords etc.

This is simplifed by renaming `config.py.example` to `config.py` and updating the configuration.

The CMCS Linux Executable is also required, this can be downloaded from https://novra.com/product/s300n-receiver and extract the executable binary file to the `novra` folder once this repo is cloned.

## Usage
It's a Python script, probably best to run it as a service, ideally within a virtual environment.

## Reported Data
The status information reported by the `--xmlstatus` CMCS command is mostly included in this data. Can be easily expanded or modified.
