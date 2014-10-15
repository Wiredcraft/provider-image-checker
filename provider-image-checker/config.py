import json

class Config:
    """
    Handles the config.json file
    """
    def __init__(self):
        self.config = json.load(open("config.json"))

    def get_providers(self):
        return [provider for provider in self.config['providers']]

    def get_provider_config(self, provider):
        return self.config['providers'][provider]

    def get_client_id(self, provider):
        return self.get_provider_config(provider)['client_id']

    def get_api_key(self, provider):
        return self.get_provider_config(provider)['api_key']

    def get_filters(self, provider):
        return self.get_provider_config(provider)['filters']

    def get_filename(self):
        return self.config['filename']


_config = Config()

def get_config():
    return _config

