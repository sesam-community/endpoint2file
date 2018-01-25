# endpoint2file (experimental)
[![Build Status](https://travis-ci.org/sesam-community/endpoint2file.svg?branch=master)](https://travis-ci.org/sesam-community/endpoint2file)

A micro-service for reading a byte stream from a sesam node endpoint and writing it to a file.

## Environment variables

`JWT` - JSON Web Token granting access to all ENDPOINTs defined in _config_endpoint2file_ (se example below)

`LOG_LEVEL` - Default 'INFO'. Ref: https://docs.python.org/3/howto/logging.html#logging-levels

`NODE` - base url to the sesam node instance api (ex: "https://abcd1234.sesam.cloud/api")

`SMB_IP` - Samba share IP

`SMB_PWD` - Samba share password

`SMB_SERVER` - Samba share server name

`SMB_SHARE` - Samba share to write files into (ex: "agresso")

`SMB_USER` - Samba share user name

`VERIFY_CERT` - If set to 'True', SSL certificate is verified 

## Usage

The endpoint2file service expects to receive a JSON config at
http://localhost:\<port>/config telling it where to fetch and dump the byte stream. 
A JSON push sink with a url system can be used for this purpose.

## Example endpoint2file MicroService System Config
```
{
  "_id": "endpoint2file-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "JWT": "$SECRET(JWT)",
      "LOG_LEVEL": "ERROR",   
      "NODE": "https://abcd1234.sesam.cloud/api",
      "SMB_IP": "12.34.56.78",
      "SMB_PWD": "$SECRET(endpoint2file-smb-pwd)",
      "SMB_SERVER": "some-smb-server",
      "SMB_SHARE": "some-smb-share",
      "SMB_USER": "some-smb-user",
      "VERIFY_CERT": "False"
    },
    "image": "sesamcommunity/endpoint2file:latest",
    "port": 5555
  }
}
```

## Example URL System
```
{
  "_id": "endpoint2file-config-receiver",
  "type": "system:url",
  "name": "endpoint2file-service config receiver",
  "url_pattern": "http://localhost:5555"
}
```

## Example JSON Push Sink
```
{
  "_id": "config_endpoint2file-push-sink",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "config_endpoint2file"
  },
  "sink": {
    "type": "json",
    "system": "endpoint2file-config-receiver",
    "url": "/config"
  },
  "pump": {
    "cron_expression": "0 3 ? * *",
    "rescan_cron_expression": "0 3 ? * *"
  }
}
```

## Example config_endpoint2file Entities
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