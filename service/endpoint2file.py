#!/usr/bin/env python3

import requests
import os
import logging
import datetime
import time
import json

__author__ = "Geir Atle Hegsvold"

"""
A micro-service for reading a byte stream from a sesam node endpoint and writing it to a file.
"""

# fetch env vars
jwt = os.environ.get('JWT')
node = os.environ.get('NODE')  # ex: "https://abcd1234.sesam.cloud"
config_endpoint = os.environ.get('CONFIG_ENDPOINT')  # ex: "/api/publishers/config_endpoint/entities"
schedule = os.environ.get('SCHEDULE')  # seconds between each run

headers = {'Authorization': "bearer " + jwt}

logging.basicConfig(level=logging.INFO)  # dump log to stdout

logging.debug(datetime.datetime.now())
logging.debug("Node instance  : %s" % node)
logging.debug("Config endpoint: %s" % config_endpoint)
logging.debug("Headers        : %s\n" % headers)


def endpoint_to_file(cfg):
    """ This is where the magic happens """

    logging.debug("-> endpoint_to_file()")

    entities = json.loads(cfg)
    logging.debug(entities)

    # loop over all config entities
    for entity in entities:
        logging.debug("config entity: %s" % entity)

        # extract relevant parameters
        endpoint = entity["ENDPOINT"]
        target_path = entity["TARGET_PATH"]
        target_filename = entity["TARGET_FILENAME"]
        target_file_ext = entity["TARGET_FILE_EXT"]

        logging.debug("endpoint: %s" % endpoint)
        logging.debug("target_path: %s" % target_path)
        logging.debug("target_filename: %s" % target_filename)
        logging.debug("target_file_ext: %s" % target_file_ext)

        url = node + endpoint

        logging.debug(url)

        # fetch byte stream
        result = fetch_endpoint_stream(url)
        logging.debug("result: %s" % result.content)

        # dump byte stream to disk
        dump_byte_stream_to_file(result.content, target_path, target_filename + "." + target_file_ext)

    logging.debug("<- endpoint_to_file()")


def fetch_endpoint_stream(url, params=None):
    """Fetch byte stream from an endpoint"""

    logging.info(datetime.datetime.now())
    logging.debug("-> fetch_endpoint_stream()")
    logging.debug("url   : %s" % url)

    result = requests.get(url, params=params, headers=headers)

    logging.info(result.url)
    logging.debug("Response content: %s" % result.content)
    logging.debug("<- fetch_endpoint_stream()")

    return result


def dump_byte_stream_to_file(byte_stream, path, file):
    """Write byte stream to path/file"""

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


# if __name__ == "__main__()":
while True:
    # TODO:
    # - DONE: fetch env vars
    # - DONE: keep alive in docker
    # - DONE: expose exported files from docker container to host file share (docker cmd)
    # - graceful exit
    # - integrate in sesam
    # - DONE: consider putting endpoint- & target path/filename-config in separate dataset to be read before executing this service;

    # first fetch config
    config = fetch_endpoint_stream(node + config_endpoint)

    # then do stuff for each config entity
    endpoint_to_file(config.content.decode('utf-8'))  # byte stream -> string

    # sleep for a while
    time.sleep(int(schedule))
