from struct import unpack
from time import sleep
import traceback

from .PeerMessages import *
from ..exceptions import *

class PeerStreamIterator:
    BUFFER_SIZE = 10000
    
    def __init__(self, socket, extension_protocol):
        super().__init__()
        self.socket = socket
        self.extension_protocol = extension_protocol
        self.data = b''
    
    def recv(self):
        """
        even though select was triggered and noted a new message, 
        there is nothing to recv on socket, this is the way of the OS
        to tell us, that we should wait because the socket is temporary unavailable
        and we will try after a short delay again
        """
        while True:
            try:
                recv = self.socket.recv(self.BUFFER_SIZE)
                self.data += recv
                parsed = self.parse()
                if parsed != None:
                    return parsed
            except BlockingIOError as e:
                sleep(1)
            except Exception as e:
                return None
    
    def parse(self):
        HEADER_LENGTH = 4
        if len(self.data) > HEADER_LENGTH:
            length = unpack("!I", self.data[:4])[0]
            if length == 0:
                self.data = self.data[HEADER_LENGTH:]
                return None
            
            if len(self.data) >= length + HEADER_LENGTH:
                mid = unpack("!B", self.data[4:5])[0]

                ret = None
                msg = self.data[:HEADER_LENGTH + length]

                if mid == 0:
                    ret = PeerMessageStructures.Choke()
                elif mid == 1:
                    ret = PeerMessageStructures.Unchoke()
                elif mid == 2:
                    ret = PeerMessageStructures.Interested()
                elif mid == 3:
                    ret = PeerMessageStructures.NotInterested()
                elif mid == 4:
                    ret = val_have(msg)
                elif mid == 5:
                    ret = val_bitfield(msg)
                elif mid == 6:
                    ret = val_request(msg)
                elif mid == 7:
                    ret = val_piece(msg)
                elif mid == 8:
                    ret = val_cancel(msg)
                elif mid == 9:
                    ret = val_port(msg)
                # libtorrent extension protocol 
                elif mid == 20:
                    print("6"*100)
                    ret = self.extension_protocol.val_handshake(msg)
                    print("finally", ret)
                else:
                    raise MessageExceptions("Unknown message id", mid)
                
                # clean up data and return parsed data
                self.data = self.data[HEADER_LENGTH + length:]
                return ret
            else:
                pass
                #print("Info: don't have all parts of message")
        else:
            pass
            #print("Info: message too small")
        return None
