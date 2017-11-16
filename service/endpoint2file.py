#!/usr/bin/env python3

import requests
import os
import logging
import datetime
import time

__author__ = "Geir Atle Hegsvold"

"""
A micro-service for reading a byte stream from a sesam node endpoint and writing it to a file.
"""

# fetch env vars
jwt = os.environ.get('JWT')
node = os.environ.get('NODE') # ex: "ac6f6566.sesam.cloud"
lines = os.environ.get('BANENOR_LINES') # expects a space separated list of lines ("B01 B02 B03 ...")
endpoint = os.environ.get('SESAM_ENDPOINT2FILE_ENDPOINT') # ex: "/api/publishers/railml/xml"
target_path = os.environ.get('SESAM_ENDPOINT2FILE_TARGET_PATH') # ex: "railml/"
target_filename = os.environ.get('SESAM_ENDPOINT2FILE_TARGET_FILENAME') # ex: "railml2.3nor"
target_filename_ext = os.environ.get('SESAM_ENDPOINT2FILE_TARGET_FILE_EXT') # ex: "xml"
schedule = os.environ.get('SESAM_ENDPOINT2FILE_SCHEDULE') # seconds between each run

headers = {'Authorization': "bearer " + jwt}
protocol = "https://"  # FIXME: include protocol in 'NODE' env.var

logging.basicConfig(level=logging.INFO)  # dump log to stdout
logging.debug(datetime.datetime.now())
logging.debug("Node instance: %s" % node)
logging.debug("Endpoint     : %s" % endpoint)
logging.debug("Headers      : %s\n" % headers)


def fetch_endpoint_stream(url, params):
    """Fetch byte stream from an endpoint"""

    logging.info(datetime.datetime.now())
    logging.debug("-> fetch_endpoint_stream()")
    logging.debug("url   : %s" % url)
    logging.debug("params: %s" % params)

    result = requests.get(url, params=params, headers=headers)

    logging.info(result.url)
    logging.debug("Response content: %s" % result.content)
    logging.debug("<- fetch_endpoint_stream()")

    return result


def dump_byte_stream_to_file(byte_stream, path, file):
    """Write byte stream to a file"""

    logging.debug("-> dump_byte_stream_to_file()")
    logging.debug("target_path: %s" % path)
    logging.debug("target_file: %s" % file)
    logging.info(" --> %s%s" % (path, file))

    # make sure target path exists
    if not os.path.exists(path):
        os.mkdir(path)

    logging.debug("byte_stream: %s" % byte_stream)

    # write to file
    with open(path + file, 'wb') as output:
        output.write(byte_stream)

    logging.debug("<- dump_byte_stream_to_file()")


def endpoint_to_file():
    """The main loop"""

    for line in lines.split(' '):
        logging.debug("-> main loop")

        # for railml exports, target file names must be prefixed with 'line'
        # and we currently only want segmented lines
        # FIXME: how can these in-params be made more generic?
        params = {'bane': line, 'segmented': 'true'}
        url = protocol + node + endpoint

        # fetch byte stream
        result = fetch_endpoint_stream(url, params)

        # dump byte stream to disk
        target_file = line + "-" + target_filename + "." + target_filename_ext
        dump_byte_stream_to_file(result.content, target_path, target_file)

        logging.debug("<- main loop\n")


# if __name__ == "__main__()":
while True:
    # TODO:
    # - DONE: fetch env vars
    # - DONE: keep alive in docker
    # - DONE: expose exported files from docker container to host file share (docker cmd)
    # - graceful exit
    # - integrate in sesam
    # - consider moving loop out to a wrapper service
    endpoint_to_file()
    time.sleep(int(schedule))
