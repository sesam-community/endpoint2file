from smb.SMBConnection import SMBConnection
import io
import logging

# http://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html


def write(bytestream, smb_share, target_file, user, password, client_machine_name, server_name, server_ip):
    """ Writes bytestream to server_name/smb_share/target_file """

    logging.debug("-> bytestream2smb.write()")

    logging.debug("   smb_share: %s" % smb_share)
    logging.debug("   target_file: %s" % target_file)
    logging.debug("   user: %s" % user)
    logging.debug("   client_machine_name: %s" % client_machine_name)
    logging.debug("   server_name: %s" % server_name)
    logging.debug("   server_ip: %s" % server_ip)

    stream = io.BytesIO(bytestream)  # byte stream -> binary stream

    # open smb share connection
    conn = SMBConnection(user, password, client_machine_name, server_name, use_ntlm_v2=True)
    assert conn.connect(server_ip, 139)

    # write binary stream to smb share
    conn.storeFile(smb_share, target_file, stream)
    conn.close()

    logging.debug("<- bytestream2smb.write()")


if __name__ == '__main__':

    import os

    logging.basicConfig(level=logging.DEBUG)  # dump log to stdout

    bytestream = b"test"
    smb_share = os.environ.get('SMB_SHARE')
    target_file = "railml/test.dat"
    smb_user = os.environ.get('SMB_USER')
    smb_pwd = os.environ.get('SMB_PWD')
    client_machine_name = "endpoint2file"
    smb_server = os.environ.get('SMB_SERVER')
    smb_ip = os.environ.get('SMB_IP')

    write(bytestream, smb_share, target_file, smb_user, smb_pwd, client_machine_name, smb_server, smb_ip)