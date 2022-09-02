import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from fetch import fetch, fetch_all

REQUIRED_ENVIONMENT=["IMAP_SERVER", "IMAP_USER", "IMAP_PASS", "LMTP_HOST", "LMTP_PORT", "LDAP_ENABLED"]
REQUIRED_LDAP_ENVIRONMENT=["LDAP_SERVER", "LDAP_BIND_DN", "LDAP_BIND_PW", "LDAP_BASE_DN", "LDAP_USER_DN"]

load_dotenv()

for env in REQUIRED_ENVIONMENT:
  if env not in os.environ:
    raise Exception(f"Missing required environment variable {env}")

if os.getenv("LDAP_ENABLED").lower() == "true":
  for env in REQUIRED_LDAP_ENVIRONMENT:
    if env not in os.environ:
      raise Exception(f"Missing required environment variable {env}")

app = FastAPI()

@app.get("/fetch")
async def app_fetch_all():
  fetch_all()
  return {"result": True}

@app.get("/fetch/{email}")
async def app_fetch(email: str):
  fetch(email)
  return {"result": True}

if __name__ == '__main__':
  uvicorn.run(app, host="0.0.0.0")
