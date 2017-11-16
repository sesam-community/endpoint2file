# xml-exporter
[![Build Status](https://travis-ci.org/sesam-community/xml-exporter.svg?branch=master)](https://travis-ci.org/sesam-community/xml-exporter)

xml-exporter is a microservice for exporting an XML byte stream from a sesam xml_endpoint to disk.

##### Example System Config
```
{
  "_id": "xml-exporter-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "LINES": "B01 B02 B03",
      "XML-EXPORTER_ENDPOINT": "/api/publishers/railml/xml",
      "XML-EXPORTER_TARGET_FILENAME": "railml2.3nor",
      "XML-EXPORTER_TARGET_FILENAME_EXT": "xml",
      "XML-EXPORTER_TARGET_PATH": "railml/"
    },
    "image": "sesamcommunity/xml-exporter:latest",
    "port": 5000
  }
}
```
