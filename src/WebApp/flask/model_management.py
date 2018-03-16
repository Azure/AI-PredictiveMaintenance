import re
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
        
    def get(self, resource):        
        endpoint = self.api_base_url + resource + self.api_version_query
        response = requests.get(endpoint, headers = self.get_auth_header())
        return response.text
        #return json.dumps(response.json())
         
if __name__ == '__main__':
    pass
