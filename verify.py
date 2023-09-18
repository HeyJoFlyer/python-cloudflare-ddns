#A python script to verify Cloudflare APi tokens and check dns record ids for a given zone
VERSION = "0.1.0"
zone_identifier = "2a8751b1e66feasdasdb8f2392160a13c5fcfc"

import httpx
import os.path
import json
import sys
token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")
with open(token_path, "r") as f:
    TOKEN = f.read()
options_dict = {"-h": "help", "-help": "help", "-r" : "dns_records", "-records": "dns_records", "-f": "file", "-file": "file",}
options = {"file": False, "help": False, "dns_records": False}
for i, option in enumerate(sys.argv):
    if option in options_dict.keys():
        if options_dict[option] == "file":
            if len(sys.argv) > i + 1:
                file = os.path.realpath(sys.argv[i + 1])
                if os.path.exists(os.path.dirname(file)):
                    options["file"] = file
                else:
                    print(f"File {file} does not exist")
                    options["file"] = False

        elif options_dict[option] == "dns_records":
            if len(sys.argv) > i + 1 and not sys.argv[i + 1].startswith("-"):
                zone_identifier = sys.argv[i + 1]
            options["dns_records"] = True
        else:
            options[options_dict[option]] = True
            

def verify():
    client = httpx.Client()
    headers = {"Authorization": f"Bearer {TOKEN}"}
    answer = client.get("https://api.cloudflare.com/client/v4/user/tokens/verify", headers=headers)
    print(answer.json())
    if answer.status_code == 200:
        print("Success!\nThe token is valid\n")
        if options["dns_records"] == True:
            answer = client.get(f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records", headers=headers)
            jsonobj = answer.json()
            json_str = json.dumps(jsonobj, indent=2)
            print(json_str)
            if answer.status_code == 200:
                print(f"succesfully got dns records for zone {zone_identifier}")
            if options["file"] != False:
                with open(options["file"], "w") as f:
                    f.write(json_str)
                print(f"Written output to {options['file']}")
       
if __name__ == "__main__":
    if options["help"] == True:
        print(f"A python tool to verify a cloudflare token and get ids of dns records \nVersion = {VERSION}\n\n\
-h -help: prints this dialogue\n\
-r -records <zone_id>: prints the dns records of specified zone (zone id is not mandatory and may be definied in {os.path.realpath(__file__)})\n\
INFO: you can get the zone id from the cloudflare dashboard overview for your domain\n\
-f <file.json> -file <file.json>: write json output to file")
        exit()
    verify()