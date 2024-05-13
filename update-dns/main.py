import cloudflare
import os
import requests

class ApiClient:
    cloudflare_client = None
    
    def get_client(self):
        if ApiClient.cloudflare_client == None:
            ApiClient.cloudflare_client = cloudflare.Cloudflare(api_key=get_cloudflare_api_token())
        
        return ApiClient.cloudflare_client
        
def get_ip_address():
    ip_request = requests.get('https://ident.me')

    ip_request.raise_for_status()

    return ip_request.text

def get_zone_id():
    return os.environ['CLOUDFLARE_ZONE_ID']

def get_cloudflare_api_token():
    token_file = '{}/api_token'.format(os.environ['CREDENTIALS_DIRECTORY'])

    contents = ''

    with open(token_file, 'r') as fin:
        contents = fin.read()

    return contents.replace('\n', '')
    
def get_dns_records(zone_id):
    client = ApiClient().get_client()

    records = client.dns.records.list(zone_id=zone_id)

    return [{'id': x.id, 'name': x.name} for x in records]

def update_dns_record(zone_id, id, name, ip_addr):
    client = ApiClient().get_client()

    client.dns.records.edit(dns_record_id=id, zone_id=zone_id, content=ip_addr, name=name, type='A')


if __name__ == '__main__':
    ip_addr = get_ip_address()
    api_token = get_cloudflare_api_token()
    zone_id = get_zone_id()

    records = get_dns_records(zone_id)

    for record in records:
        update_dns_record(zone_id=zone_id, id=record['id'], name=record['name'], ip_addr=ip_addr)

