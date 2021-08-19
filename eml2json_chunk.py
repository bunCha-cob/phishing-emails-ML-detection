import datetime
import json, sys
#import eml_parser
from email import policy
import email

names = [2019, 2018, 2017]
file_format = 'D:\Y3\Securing Network\Project\phishing_email\{}.txt'


def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


for name in names:
    filename = file_format.format(name)
    json_opt = open('{}.json'.format(name), 'a')
    with open(filename, 'r', encoding='utf8') as f:
        data = f.read()
        emails = data.split('From jose@monkey.org')
        for email_str in emails:
            email_str = 'From jose@monkey.org' + email_str
            e = email.message_from_string(email_str, policy=policy.default)
            received_time = email_str.split('\n')[0].split('From jose@monkey.org')[1]
            send_time = e['Date']
            total_size_EmailMessage_in_bytes = sys.getsizeof(e)
            email_eml_string_total_size_in_bytes = sys.getsizeof(e.as_string())
            body_plain_text_length = 0
            for part in e.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_payload()
                    body_plain_text_length += len(str(body))

            eml_opt = open('email.eml', 'w', encoding='utf8')
            eml_opt.write(email_str)
            eml_opt.close()
            with open('email.eml', 'rb') as f1:
                raw_email = f1.read()
                ep = eml_parser.EmlParser()
                parsed_eml = ep.decode_email_bytes(raw_email)
                parsed_eml['attached']= {
                        "total_size_EmailMessage_in_bytes": total_size_EmailMessage_in_bytes,
                        "email_eml_string_total_size_in_bytes": email_eml_string_total_size_in_bytes,
                        "body_plain_text_length": body_plain_text_length,
                        "received_time": received_time,
                        "send_time": send_time
                }
                json_opt.write(json.dumps(parsed_eml, default=json_serial))
                json_opt.write('\n')
                f1.close()
    json_opt.close()
    print('{} Done'.format(name))
