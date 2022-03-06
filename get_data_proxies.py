import json


class GettingData:

    @staticmethod
    def get_json_proxies():
        with open('proxies.json', 'r') as file:
            data = json.load(file)

        return data

