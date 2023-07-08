import motor.motor_asyncio
from ssl import CERT_NONE

uri = "mongodb+srv://<username>:<password>@cluster0.uikhei9.mongodb.net"

# client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])

client = motor.motor_asyncio.AsyncIOMotorClient(uri, ssl_cert_reqs=CERT_NONE)

try:
    client.admin.command('ping')
    print("Connected to MongoDB")
except Exception as e:
    print(e)
