import re
import json
import requests

class ModelManagement:
    def __init__(self, swagger_url, access_token):
        self.swagger_url = swagger_url
        self.access_token = access_token		

        p = re.compile('(.+)swagger\.json(.+)')
        m = p.match(swagger_url)
        
        self.api_base_url = m.group(1)
        self.api_version_query = m.group(2)
                
    def get_auth_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        
    def get_api_endpoint(self, resource):
        parts = resource.split('?')
        endpoint = self.api_base_url + parts[0] + self.api_version_query + ('&' + parts[1] if len(parts) == 2 else '')
        return endpoint   
        
    def get(self, resource):
        endpoint = self.get_api_endpoint(resource)
        response = requests.get(endpoint, headers = self.get_auth_header())
        return response
        
    def post(self, resource, payload):
        data = json.dumps(payload)
        endpoint = self.get_api_endpoint(resource)
        response = requests.post(endpoint, headers = self.get_auth_header(), data = data)
        return response        
         
if __name__ == '__main__':
    pass
