import datetime
import imaplib
from email.message import Message
import csv

from config import config

username = config["username"]
password = config["password"]
phone_name = config["phonename"]
sms_csv = config["sms_csv"]

svr = imaplib.IMAP4_SSL("imap.gmail.com", 993)
svr.login(username, password)

with open(sms_csv, 'rt') as f:
    cr = csv.DictReader(f)
    for i, row in enumerate(cr):
        sender = "Me" if row["类型"] == "发出" else "{}@{}".format(row["聊天会话"], phone_name)
        receiver = "{}@{}".format(row["聊天会话"], phone_name) if row["类型"] == "发出" else "Me"
        subject = "SMS with {} on {}".format(row["聊天会话"], phone_name)
        content = row["文本"]

        msg = Message()
        msg['Subject'] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_payload(content)

        t = datetime.datetime.strptime(row["信息日期"], "%Y-%m-%d %H:%M:%S")
        timestamp = datetime.datetime.timestamp(t)

        svr.append('SMS', '', imaplib.Time2Internaldate(timestamp), str(msg).encode('utf-8'))

        print(i)
