from pydub import AudioSegment
from io import BytesIO
from pydub.silence import split_on_silence
import base64
import os
import sys

sys.stderr.write("Starting Python Function\n")

name = "World"

try:
  if not os.isatty(sys.stdin.fileno()):
    try:
      obj = json.loads(sys.stdin.read())
      if obj["name"] != "":
        name = obj["name"]
    except ValueError:
      # ignore it
      sys.stderr.write("no input, but that's ok\n")
except:
  pass

print "Hello", name, "!"