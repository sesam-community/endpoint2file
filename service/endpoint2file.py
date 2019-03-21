#!/usr/bin/env python3

import requests
import os
import logging
import datetime
import json
import bytestream2smb
from flask import Flask, request
import cherrypy


__author__ = "Geir Atle Hegsvold"

"""
A micro-service for reading a byte stream from a sesam node endpoint and writing it to a file.
"""

# fetch env vars
jwt = os.environ.get('JWT')
node = os.environ.get('NODE')  # ex: "https://abcd1234.sesam.cloud/api"
verify_cert = (os.environ.get('VERIFY_CERT') == 'True')  # Only 'True' is considered True; everything else is False

smb_ip = os.environ.get('SMB_IP')
smb_server = os.environ.get('SMB_SERVER')
smb_share = os.environ.get('SMB_SHARE')
smb_user = os.environ.get('SMB_USER')
smb_pwd = os.environ.get('SMB_PWD')

headers = {'Authorization': 'bearer ' + jwt}

# initialize web service
app = Flask(__name__)

# set logging
log_level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))  # default log level = INFO
logging.basicConfig(format='[%(levelname)s] %(name)s: %(message)s', level=log_level)
logger = logging.getLogger("endpoint2file.py")

logger.debug("Node instance  : %s" % node)
logger.debug("Headers        : %s" % headers)


def endpoint_to_file(cfg):
    """ This is where the magic happens """

    logger.debug("-> endpoint_to_file()")

#    entities = json.loads(cfg)
    entities = cfg

    # loop over all config entities
    for entity in entities:
        logger.debug("   config entity  : %s" % entity)

        # extract relevant parameters
        endpoint = entity["ENDPOINT"]
        target_path = entity["TARGET_PATH"]
        target_filename = entity["TARGET_FILENAME"]
        target_file_ext = entity["TARGET_FILE_EXT"]

        logger.debug("   endpoint       : %s" % endpoint)
        logger.debug("   target_path    : %s" % target_path)
        logger.debug("   target_filename: %s" % target_filename)
        logger.debug("   target_file_ext: %s" % target_file_ext)

        url = node + endpoint

        logger.info("Fetching bytestream from %s" % url)
        logger.info("Writing to %s (%s):%s/%s%s" % (smb_server, smb_ip, smb_share, target_path, target_filename))

        # fetch byte stream
        result = fetch_endpoint_stream(url)

        # dump byte stream to disk
        dump_byte_stream_to_file(result.content, target_path, target_filename + "." + target_file_ext)
        logger.info("Done writing %s (%s):%s/%s%s\n" % (smb_server, smb_ip, smb_share, target_filename, target_filename))

    logger.debug("<- endpoint_to_file()")


def fetch_endpoint_stream(url, params=None):
    """Fetch byte stream from an endpoint"""

    logger.info(datetime.datetime.now())
    logger.debug("-> fetch_endpoint_stream()")
    logger.debug("   verify_cert     : %s" % verify_cert)
    logger.debug("source url: %s" % url)

    result = requests.get(url, params=params, headers=headers, verify=verify_cert)

#    logger.debug("   Response content: %s" % result.content)
    logger.debug("<- fetch_endpoint_stream()")

    return result


def dump_byte_stream_to_file(byte_stream, path, file):
    """Write byte stream to path/file"""

    logger.debug("-> dump_byte_stream_to_file()")
    logger.debug("target_path: %s" % path)
    logger.debug("target_file: %s" % file)
#    logger.info(" --> %s%s" % (path, file))

    # make sure target path exists
#    if not os.path.exists(path):
#        os.mkdir(path)

#    logger.debug("byte_stream: %s" % byte_stream)

    # write to file
#    with open(path + file, 'wb') as output:
#        output.write(byte_stream)

    logger.debug("  smb_server : %s" % smb_server)
    logger.debug("  smb_ip     : %s" % smb_ip)
    logger.debug("  smb_share  : %s" % smb_share)
    logger.debug("  target_path: %s" % path)
    logger.debug("  target_file: %s" % file)
#    logger.debug("   byte_stream: %s" % byte_stream)

    # write to samba share
    bytestream2smb.write(byte_stream, smb_share, path + file, smb_user, smb_pwd, "endpoint2file", smb_server, smb_ip)
    logger.debug("<- dump_byte_stream_to_file()")


@app.route('/config', methods=['POST'])
def config():
    # POST JSON formatted config to this endpoint

    # make sure we have a POST request ...
    if request.method == 'POST':

        # ... and JSON data
        if request.headers['Content-Type'] == 'application/json':

            cfg = request.json

            logger.debug("cfg: %s" % cfg)

            # then do stuff for each config entity
            endpoint_to_file(cfg)

            return "JSON Message: " + json.dumps(request.json) + "\n"
        else:
            return "415 Unsupported Media Type"


if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0', port=5555)  # port must match the port exposed in the Dockerfile
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5555,  # port must match the port exposed in the Dockerfile
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
