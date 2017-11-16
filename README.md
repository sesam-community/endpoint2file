# xml-exporter
[![Build Status](https://travis-ci.org/sesam-community/xml-exporter.svg?branch=master)](https://travis-ci.org/sesam-community/xml-exporter)

xml-exporter is a microservice for exporting an XML byte stream from a sesam xml_endpoint to disk.

## Environment variables

`BANENOR_LINES` - a space seprarated list of all lines to be exported (ex: "B01 B02...")

`XML_EXPORTER_ENDPOINT` - relative url to the sesam node xml_endpoint

`XML_EXPORTER_SCHEDULE` - seconds between each run of the micro service

`XML_EXPORTER_TARGET_FILENAME` - target filename of exported xml

`XML_EXPORTER_TARGET_FILENAME_EXT` - target file extension

`XML_EXPORTER_TARGET_PATH` - target fileshare path

## Example System Config
```
{
  "_id": "xml-exporter-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "BANENOR_LINES": "B01 B02 B03",
      "XML_EXPORTER_ENDPOINT": "/api/publishers/railml/xml",
      "XML_EXPORTER_SCHEDULE": 1209600
      "XML_EXPORTER_TARGET_FILENAME": "railml2.3nor",
      "XML_EXPORTER_TARGET_FILENAME_EXT": "xml",
      "XML_EXPORTER_TARGET_PATH": "railml/"
    },
    "image": "sesamcommunity/xml-exporter:latest",
    "port": 5000
  }
}
```
