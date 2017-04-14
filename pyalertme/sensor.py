import logging
from pyalertme import *
import struct
import time
import binascii
import threading


class Sensor(Device):

    def __init__(self, callback=None):
        """
        Sensor Constructor

        """
        Device.__init__(self, callback)

        # Type Info
        self.manu = 'PyAlertMe'
        self.type = 'Button Device'
        self.date = '2010-11-15'
        self.version = 59435

        # Relay State
        self.tamper = 0
        self.triggered = 0

    def process_message(self, message):
        """
        Process incoming message

        :param message: Dict of message
        :return:
        """
        super(Sensor, self).process_message(message)

        # Zigbee Explicit Packets
        if (message['id'] == 'rx_explicit'):
            profile_id = message['profile']
            cluster_id = message['cluster']

            source_addr_long = message['source_addr_long']
            source_addr_short = message['source_addr']

            if (profile_id == self.ALERTME_PROFILE_ID):
                # AlertMe Profile ID

                # Python 2 / 3 hack
                if (hasattr(bytes(), 'encode')):
                    cluster_cmd = message['rf_data'][2]
                else:
                    cluster_cmd = bytes([message['rf_data'][2]])

                if (cluster_id == b'\x05\x00'):
                    # Security Initialization
                    self._logger.info('Security Initialization')

                else:
                    self._logger.error('Unrecognised Cluster ID: %r', cluster_id)

            else:
                self._logger.error('Unrecognised Profile ID: %r', profile_id)
