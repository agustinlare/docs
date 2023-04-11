from sys import argv
from fabric import Connection
from dotenv import load_dotenv
from pathlib import Path
import logging, os, sys

logging.getLogger().setLevel(logging.INFO)

# Acepto como argumento un archivo de env
if len(sys.argv) > 1:
  dotenv_path = Path(sys.argv[1])
  load_dotenv(dotenv_path=dotenv_path)

# Variables requeridas
REMOTE_HOST = os.getenv("REMOTE_HOST")
EC2_SSH_USER = os.getenv("EC2_SSH_USER")
EC2_SSH_KEY = os.getenv("EC2_SSH_KEY")

c = Connection(
  host=REMOTE_HOST,

  user=EC2_SSH_USER,
  connect_kwargs={
      "key_filename": EC2_SSH_KEY,
  }
)

logging.info("Checking status on remote server")
resp = c.run("echo Hello World!")
