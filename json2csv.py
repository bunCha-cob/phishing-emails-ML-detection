import json, csv
from dateutil.parser import parse

names = [2019, 2018, 2017]
file_format = '{}.json'

opt_f = open('ML_data.csv', 'a', newline='')
writer = csv.writer(opt_f)
writer.writerow(["attachments_num", "email_subject_length", "content_transfer_encoding_base64_num",
                 "content_disposition_attachment_num", "content_disposition_num",
                 "content_disposition_unique_num", "attachments_total_size",
                 "content_type_multipart_mixed_num", "content_type_total_num", "content_type_unique_num",
                 "content_transfer_encoding_unique_num", "content_transfer_encoding_total_num",
                 "email_span_time", "total_size_EmailMessage_in_bytes",
                 "email_eml_string_total_size_in_bytes", "body_plain_text_length", "Classification"])

for name in names:
    with open(file_format.format(name), 'r') as f:
        for line in f:
            data = json.loads(line)
            attachments_num = 0
            email_subject_length = 0
            content_transfer_encoding_base64_num = 0
            content_disposition_attachment_num = 0
            content_disposition_num = 0
            content_disposition_set = list()
            attachments_total_size = 0
            content_type_multipart_mixed_num = 0
            content_type_total_num = 0
            content_type_set = list()
            content_transfer_encoding_set = list()
            content_transfer_encoding_total_num = 0
            email_span_time = 0
            total_size_EmailMessage_in_bytes = data['attached']['total_size_EmailMessage_in_bytes']
            email_eml_string_total_size_in_bytes = data['attached']['email_eml_string_total_size_in_bytes']
            body_plain_text_length = data['attached']['body_plain_text_length']

            # Scan attachment
            if 'attachment' in data.keys():
                attachments_num = len(data['attachment'])
                for at in data['attachment']:
                    if 'content-transfer-encoding' in at['content_header'].keys():
                        content_transfer_encoding_total_num += 1
                        content_transfer_encoding_set.append(
                            at['content_header']['content-transfer-encoding'][0])
                        if at['content_header']['content-transfer-encoding'][0] == 'base64':
                            content_transfer_encoding_base64_num += 1
                    if 'content-type' in at['content_header'].keys():
                        content_type_total_num += 1
                        content_type_set.append(at['content_header']['content-type'][0])
                    if 'size' in at.keys():
                        attachments_total_size += at['size']
                    if 'content-disposition' in at['content_header'].keys():
                        content_disposition_num += 1
                        for val in at['content_header']['content-disposition']:
                            content_disposition_type = val.split(';')[0]
                            content_disposition_set.append(content_disposition_type)
                            if content_disposition_type == 'attachment':
                                content_disposition_attachment_num += 1
            content_disposition_unique_num = len(set(content_disposition_set))

            # Scan body
            for idx in range(len(data['body'])):
                if 'content_type' in data['body'][idx].keys():
                    content_type_total_num += 1
                    content_type_set.append(data['body'][idx]['content_type'])
                    if data['body'][idx]['content_type'] == 'multipart/mixed':
                        content_type_multipart_mixed_num += 1
                if 'content-transfer-encoding' in data['body'][idx]['content_header'].keys():
                    content_transfer_encoding_total_num += 1
                    content_transfer_encoding_set.append(
                        data['body'][idx]['content_header']['content-transfer-encoding'][0])
                    if data['body'][idx]['content_header']['content-transfer-encoding'][0] == 'base64':
                        content_transfer_encoding_base64_num += 1

            content_transfer_encoding_unique_num = len(set(content_transfer_encoding_set))  # add to csv
            content_type_unique_num = len(set(content_type_set))  # add to csv

            # Scan header
            if 'subject' in data['header']:
                email_subject_length = len(data['header']['subject'])

            send_time_str = data['attached']['send_time']
            received_time_str = data['attached']['received_time']

            if received_time_str is not '' and send_time_str is not None:
                received_time = parse(received_time_str)
                send_time = parse(send_time_str)
                email_span_time = received_time - send_time
                email_span_time = email_span_time.total_seconds()

            if received_time_str is not '' and send_time_str is not None and email_span_time >= 0:             
                # write to .csv file
                writer.writerow([attachments_num, email_subject_length, content_transfer_encoding_base64_num,
                                 content_disposition_attachment_num, content_disposition_num,
                                 content_disposition_unique_num, attachments_total_size,
                                 content_type_multipart_mixed_num, content_type_total_num, content_type_unique_num,
                                 content_transfer_encoding_unique_num, content_transfer_encoding_total_num,
                                 email_span_time, total_size_EmailMessage_in_bytes,
                                 email_eml_string_total_size_in_bytes, body_plain_text_length, "Phishing"])
f.close()
opt_f.close()
