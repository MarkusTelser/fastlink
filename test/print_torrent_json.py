from src.backend.metadata.Bencoder import bdecode
from json import dumps

fp = "/home/carlos/.local/share/data/qBittorrent/BT_backup/369fff7674d7cb37ab0cf76a20903df6271cdbfc.fastresume"

with open(fp, "rb") as f:
    raw_data = f.read()
data = bdecode(raw_data)

#print(data["info"]["pieces"][:20])
del data["pieces"]
del data["peers"]
del data["info-hash"]

print(dumps(data, indent=4))
