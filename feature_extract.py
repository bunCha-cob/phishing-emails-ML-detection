import email
from email import policy

def make_EmailMessage(f):
    """Factory to create EmailMessage objects instead of Message objects"""
    return email.message_from_binary_file(f, policy=policy.default)

names = [2019]
file_format = 'D:\Y3\Securing Network\Project\phishing_email\{}.txt'

for name in names:
    file_path = file_format.format(name)
    with open(file_path, 'r', encoding='utf8') as f:
        data = f.read()
    emails = data.split('From ')

    for email_str in emails:
        email_str = 'From ' + email_str
        e = email.message_from_string(email_str, policy=policy.default)
        body_plain_text_length = 0
        for part in e.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                body = part.get_payload()
                body_plain_text_length += len(str(body))
