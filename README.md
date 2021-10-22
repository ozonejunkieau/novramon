# novramon

## _InfluxDB 2 Monitoring for Novra S300 Satellite Receiver_

_This is quick and dirty but seems to work..._

## Configuration
Create a `config.py` file that contains site specific configuration such as hostnames, passwords etc.

This is simplifed by renaming `config.py.example` to `config.py` and updating the configuration.

## Usage
It's a Python script, probably best to run it as a service, ideally within a virtual environment.

## Reported Data
The status information reported by the `--xmlstatus` CMCS command is mostly included in this data. Can be easily expanded or modified.
