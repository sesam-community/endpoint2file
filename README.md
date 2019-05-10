# endpoint2file (experimental)
[![Build Status](https://travis-ci.org/sesam-community/endpoint2file.svg?branch=master)](https://travis-ci.org/sesam-community/endpoint2file)

endpoint2file is a micro service that reads a byte stream from a sesam node endpoint and writes it to a file.

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

The endpoint2file service expects to receive a JSON list of configs at
http://localhost:5555/config defining which endpoint to fetch the byte stream from
and where to write it.

A JSON push sink can be used for this purpose.

## Example System Config
```
{
  "_id": "endpoint2file-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "JWT": "$SECRET(JWT)",
      "LOG_LEVEL": "INFO",
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
    "system": "endpoint2file-service",
    "url": "/config"
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