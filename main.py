import os
import uvicorn
import sys
from dotenv import load_dotenv

from platform import python_version
print("Current Python Version", python_version())

sys.dont_write_bytecode = True

load_dotenv()

APP_PORT = os.getenv("APP_PORT") or 80

root_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    uvicorn.run('server.app:app', host="0.0.0.0", port=int(APP_PORT), reload=True, proxy_headers=True)