import json
from nameko.web.handlers import http

class HttpService:
    name = "http_location_service"

    @http('GET', '/location')
    def get_location(self, request):
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



