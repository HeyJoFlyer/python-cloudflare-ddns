#Updates CLoudflare DNS using Cloudflare API and AWS checkip to get current ip
#Essentially creating a dynDNS
#Docker Tag: cloudflare-ddns
import time
import httpx
import json
import os.path
import datetime as dt
from scheduler import Scheduler
## You can edit the following variables
FOLDER = "/usr/dyndns"
DELAY = 30 #Delay between getting current ip address in minutes
log_file = "dynDNS.log" #This file only gets updated when the ip address changes
sec_log_file = "ip.log" #This file gets updated with every poll of ip address
HOSTNAME = "@"
zone_identifier = "your-zone-identifier" #you can get the zone id from the cloudflare dashboard overview for your domain
record_identifier = "your-dns-record-identifier" #you can use verify.py to get a dns record id
record_type = "A"
ip_old = "0.0.0.0"


with open(os.path.join(FOLDER, "token.txt"), "r") as token_file:
    TOKEN = token_file.read()
schedule = Scheduler()


def getIP():
    ip = client.get('https://checkip.amazonaws.com').text.strip()
    print(ip)
    return ip

def updateIP(ip):
    data = json.dumps({"content": ip, "name": HOSTNAME, "proxied": True, "type": "A", "comment": "Main record", "ttl": 1})
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    answer = client.put(f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{record_identifier}", data=data, headers=headers)
    return answer
client = httpx.Client()


def run():
    ip = getIP()
    global ip_old
    with open(os.path.join(FOLDER, sec_log_file), "a") as sec_log:
        sec_log_dict = json.dumps({"IP": ip, "date": dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        sec_log.write(f"{sec_log_dict}\n")
    print(sec_log_dict)
    if ip != ip_old:
        answer = updateIP(ip)
        with open(os.path.join(FOLDER, log_file), "a") as log:
            log_dict = json.dumps({"oldIP": ip_old, "newIP": ip, "date": dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "answer": f"{answer.text}" })
            log.write(f"{log_dict}\n")
        ip_old = ip

schedule.cyclic(dt.timedelta(minutes=DELAY), run)
while True:
    schedule.exec_jobs()
    time.sleep(1)

client.close() # I know this doesn't do anything, but better than nothing