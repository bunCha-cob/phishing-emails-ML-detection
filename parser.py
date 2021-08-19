import datetime
import json
import eml_parser


def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial

filename = 'D:\Y3\Securing Network\Project\phishing_email\{}.eml'.format(str(2019))
with open(filename, 'rb') as fhdl:
  raw_email = fhdl.read()

ep = eml_parser.EmlParser()
parsed_eml = ep.decode_email_bytes(raw_email)

print(json.dumps(parsed_eml, default=json_serial))

