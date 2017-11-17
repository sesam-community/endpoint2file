# endpoint2file (experimental)
[![Build Status](https://travis-ci.org/sesam-community/endpoint2file.svg?branch=master)](https://travis-ci.org/sesam-community/endpoint2file)

A micro-service for reading a byte stream from a sesam node endpoint and writing it to a file.

## Environment variables

`CONFIG_ENDPOINT` - relative url to the sesam node configuration endpoint

`JWT` - JSON Web Token granting access to CONFIG_ENDPOINT and all ENDPOINTs defined in CONFIG_ENDPOINT

`NODE` - base url to the sesam node instance api (ex: "https://abcd1234.sesam.cloud/api")

`SCHEDULE` - seconds between each run of the micro service

## Example Sesam System Config
```
{
  "_id": "endpoint2file-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "CONFIG_ENDPOINT": "/publishers/config_endpoint/entities",
      "JWT": "$SERCRET(JWT)",
      "NODE": "https://abcd1234.sesam.cloud/api",
      "SCHEDULE": 1209600
    },
    "image": "sesamcommunity/endpoint2file:latest",
    "port": 5000
  }
}
```

## Example CONFIG_ENDPOINT config
```
[
    {
      "ENDPOINT": "/publishers/railml/xml?bane=B01&segmented=true",
      "TARGET_FILENAME": "B01-railml2.3nor",
      "TARGET_FILE_EXT": "xml",
      "TARGET_PATH": "railml/"
    },
    {
      "ENDPOINT": "/publishers/railml/xml?bane=B02&&segmented=true",
      "TARGET_FILENAME": "B02-railml2.3nor",
      "TARGET_FILE_EXT": "xml",
      "TARGET_PATH": "railml/"
    }
]
```
