
from nintendo.nex import backend, authentication, datastore
from nintendo.games import ACNL
from nintendo import account
import requests

import logging
logging.basicConfig(level=logging.INFO)

#Device id can be retrieved with a call to MCP_GetDeviceId on the Wii U
#Serial number can be found on the back of the Wii U
DEVICE_ID = 12345678
SERIAL_NUMBER = "..."
SYSTEM_VERSION = 0x220
REGION_ID = 4
COUNTRY_ID = 94
REGION_NAME = "EUR"
COUNTRY_NAME = "NL"

USERNAME = "..." #Nintendo network id
PASSWORD = "..." #Nintendo network password


api = account.AccountAPI()
api.set_device(DEVICE_ID, SERIAL_NUMBER, SYSTEM_VERSION, REGION_ID, COUNTRY_NAME)
api.set_title(ACNL.TITLE_ID_EUR, ACNL.LATEST_VERSION)
api.login(USERNAME, PASSWORD)

nex_token = api.get_nex_token(ACNL.GAME_SERVER_ID)
backend = backend.BackEndClient(ACNL.ACCESS_KEY, ACNL.NEX_VERSION)
backend.connect(nex_token.host, nex_token.port)
backend.login(nex_token.username, nex_token.password)
	
#Let's download the replay file of whoever is in 500th place
store = datastore.DataStoreClient(backend.secure_client)

get_param = datastore.DataStorePrepareGetParam()
# TODO: What goes here?
#get_param.persistence_target.owner_id = rankdata.pid
#get_param.persistence_target.persistence_id = TRACK_ID - 16
#get_param.extra_data = ["WUP", str(REGION_ID), REGION_NAME, str(COUNTRY_ID), COUNTRY_NAME, ""]

req_info = store.prepare_get_object(get_param)
headers = {header.key: header.value for header in req_info.headers}
replay_data = requests.get("http://" + req_info.url, headers=headers).content

#with open("replay.bin", "wb") as f:
	#f.write(replay_data)

#Close connection
backend.close()
