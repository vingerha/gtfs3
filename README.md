[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

# GTFS3
Copy from HA GTFS, aiming to improve the integration

<h4> Note: uses folder /config/gtfs3 to store the data (zip and sqlite)</h4>

## Updates
- 20231027: reworked gtfs into more modern setup and without configuration.yaml
  
## Installation via HACS :

In  HACS, select the 3-dots and then custom repositories
Add :
- URL : https://github.com/vingerha/gtfs3
- Category : Integration

## Configuration
Example configuration :
```
  - platform: gtfs2
    origin: "STOPPOINT:00812"
    destination: "STOPPOINT:01549"
    name: "Bus 530 outbound"
    data: zou.zip
    include_tomorrow: true
```
## How to find origin/destination
Note that the format of these can be different for each (!) source.
- Option 1: open the zip-file and search in stops.txt
- Option 2: wait for the setup after the initial integration, in /config/gtfs3 open the sqlite db (e.g. DBBrowser for sqlite) and search through the stops table....this is easier to use but requires to know how to browse db's
