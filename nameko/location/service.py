import json
from nameko.web.handlers import http
from nameko.rpc import rpc

class HttpService:
    name = "http_location_service"

    @http('GET', '/location')
    def get_location(self, request):
        with open('data.json') as file:
            data = json.load(file)
        return json.dumps(data)

    @rpc
    def get_location_rpc(self, request):
        with open('data.json') as file:
            data = json.load(file)
        return json.dumps(data)

    @http('GET', '/location/<int:value>')
    def get_location_id(self, request, value):
        with open('data.json') as file:
            data = json.load(file)
        for item in data:
            if item["location_id"] == str(value):
                return json.dumps(item)
            else:
                return json.dumps({404: "Not found"})

    @rpc
    def get_location_id_rpc(self, request, value):
        with open('data.json') as file:
            data = json.load(file)
        for item in data:
            if item["location_id"] == str(value):
                return json.dumps(item)
            else:
                return json.dumps({404: "Not found"})



