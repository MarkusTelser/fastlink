from hashlib import sha1
from base64 import b32encode
from urllib.parse import quote_plus 
from random import choice
from string import ascii_letters
from .Bencoder import encode

class TorrentFile:
    def __init__(self, name="", length=0, encoding=None, checksum=None):
        self.name = name
        self.length = length
        self.encoding = encoding
        self.checksum = checksum
        
        self.children = list()
        
    def add_children(self, children: list):
        self.children.append(children)

class TorrentData:
    def __init__(self):
        self.announces = list()
        self.created_by = ""
        self.creation_date = ""
        self.comment = ""
        self.encoding = ""
        self.nodes = set()
        self.httpseeds = list()

        self.pieces = bytes()
        self.pieces_count = 0
        self.piece_length = 0

        self.has_multi_file = False
        self.files = {}
        self.info_hash = ""
        self.info_hash_hex = ""
        self.private = False

    def check_piece_hash(self, index, hash):
        true_hash = self.pieces[index * 20: (index + 1) * 20]
        return true_hash == hash

    @staticmethod
    def gen_info_hash(info):
        encoded = encode(info)
        hash = sha1(encoded).digest()   
        return hash
            
    @staticmethod
    def gen_info_hash_hex(info):
        encoded = encode(info)
        hex_hash = sha1(encoded).hexdigest()
        return hex_hash.upper()

    @property 
    def info_hash_quoted(self):
        return quote_plus(self.info_hash)

    @property
    def info_hash_base32(self):
        base32 = b32encode(self.info_hash).decode('utf-8')
        return base32
    
    @staticmethod
    def gen_peer_id():
        return ''.join(choice(ascii_letters) for _ in range(20))
   

def gen_tree_chain(filepath: list[str], end_node: TorrentFile):
    if len(filepath) > 1:
        folder_node = TorrentFile(filepath[0])
        folder_node.add_children(gen_tree_chain(filepath[1:], end_node))
        return folder_node
    elif len(filepath) == 1:
        end_node.name = filepath[0]
        return end_node
    else:
        return []
    

# methods to recursively convert info["files"]  to node tree
def add_node(root_node: TorrentFile, path_list: list[str], end_node: TorrentFile):
    if len(path_list) > 0:
        for child in root_node.children:
            # iterate deeper, until we can add node
            if child.name == path_list[0]:
                add_node(child, path_list[1:], end_node)
                return root_node
    
    # add child node to root node
    child = gen_tree_chain(path_list, end_node)
    root_node.add_children(child)


# recursively calculate size for folder from children for all child nodes
def calc_folder_size(root_node: TorrentFile):
    if root_node.children:
        sum = 0
        for child in root_node.children:
            sum += calc_folder_size(child)
        root_node.length = sum
        return sum
    else:
        return root_node.length