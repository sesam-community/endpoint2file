# endpoint2file (experimental)
[![Build Status](https://travis-ci.org/sesam-community/endpoint2file.svg?branch=master)](https://travis-ci.org/sesam-community/endpoint2file)

A micro-service for reading a byte stream from a sesam node endpoint and writing it to a file.

## Environment variables

`BANENOR_LINES` - a space seprarated list of all lines to be exported (ex: "B01 B02...")

`SESAM_ENDPOINT2FILE_ENDPOINT` - relative url to the sesam node endpoint

`SESAM_ENDPOINT2FILE_SCHEDULE` - seconds between each run of the micro service

`SESAM_ENDPOINT2FILE_TARGET_FILENAME` - target filename

`SESAM_ENDPOINT2FILE_TARGET_FILE_EXT` - target file extension

`SESAM_ENDPOINT2FILE_TARGET_PATH` - target path

## Example System Config
```
{
  "_id": "xml-endpoint2file-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "BANENOR_LINES": "B01 B02 B03",
      "SESAM_ENDPOINT2FILE_ENDPOINT": "/api/publishers/railml/xml",
      "SESAM_ENDPOINT2FILE_SCHEDULE": 1209600
      "SESAM_ENDPOINT2FILE_TARGET_FILENAME": "railml2.3nor",
      "SESAM_ENDPOINT2FILE_TARGET_FILE_EXT": "xml",
      "SESAM_ENDPOINT2FILE_TARGET_PATH": "railml/"
    },
    "image": "sesamcommunity/endpoint2file:latest",
    "port": 5000
  }
}
```

