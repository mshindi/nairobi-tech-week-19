import json
from nameko.web.handlers import http
from nameko.rpc import rpc


class ScheduleHttpService:
    name = "http_schedule_service"

    @http('GET', '/schedule')
    def get_schedule(self, request):
        with open('data.json') as file:
            data = json.load(file)
        return json.dumps(data)

    @rpc
    def get_schedule_rpc(self):
        with open('data.json') as file:
            data = json.load(file)
        return json.dumps(data)

    @http('GET', '/location/<int:value>')
    def get_schedule_id(self, request, value):
        with open('data.json') as file:
            data = json.load(file)
        for item in data:
            if item["movie_id"] == str(value):
                return json.dumps(item)
            else:
                return json.dumps({404: "Not found"})

    @rpc
    def get_schedule_by_movie_id_rpc(self, value):
        with open('data.json') as file:
            data = json.load(file)
        for item in data:
            if item["movie_id"] == str(value):
                return json.dumps(item)
            else:
                return json.dumps({404: "Not found"})
