# python-cloudflare-ddns

A simple (dockerized) python script that updates the ip address of cloudflare DNS record to current IP address, creating a dynDNS.

## Install
Before building the docker image or using the script otherwhise you need to write your cloudflare token to `token.txt` and edit the zone id and record id in `dyndns.py`. If you want to update multiple records you can `mv -f "dyndns multiple records.py" "dyndns.py"` and edit the new `dyndns.py`.
*Do not share your token with anyone!!!*
<>
```bash
git clone https://github.com/HeyJoFlyer/python-cloudflare-ddns.git
cd python-cloudflare-ddns
docker build -t cloudflare-ddns .
docker-compose up -d #To start the container
```
## If you have found any bugs, please raise an [issue](https://github.com/HeyJoFlyer/python-cloudflare-ddns/issues)