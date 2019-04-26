import json
import newrelic.agent
from app.entrypoints import http
from nameko_sqlalchemy import Database

from app.auth import ContextData, authorize
from app.exceptions import BadRequest
from app.database import Base, create_session
from app.processing.pipelines import Pipeline
from app.graphql.query import graphql_query, parse_body
from app.health_check import HealthCheck
from nameko.events import EventDispatcher


newrelic.agent.initialize()


class HTTPProcessingService:
    name = "http_processing_service"
    db = Database(Base)
    context = ContextData()
    dispatch = EventDispatcher()

    def __init__(self):
        pass

    @http('GET', '/processing/initdb')
    def initdb(self, request):
        '''
        Allow for manual initialization of the database.
        '''
        create_session()
        return json.dumps({"success": True})

    @http('GET', '/processing/health')
    def health_check(self, request):
        # pylint: disable=unused-argument
        session = self.db.get_session()
        return HealthCheck(session).service_health_check()

    ######################################################################
    #  STOCK AVAILABILITY
    ######################################################################

    @http('GET', '/stock_availability')
    @authorize('can-view-stock_availability')
    def list_stocks(self, request):
        session = self.db.get_session()
        per_page = request.args.get('per_page')
        page = request.args.get('page')
        return Pipeline(session).list_stock(per_page, page)

    @http('GET', '/stock_availability/<uuid:stock_availability_id>')
    @authorize('can-view-stock_availability')
    def product_details(self, request, stock_availability_id):
        session = self.db.get_session()
        return Pipeline(session).get_stock_by_id(stock_availability_id)

    @http('POST', '/stock_availability')
    @authorize('can-add-stock_availability')
    def add_stock(self, request):
        session = self.db.get_session()
        try:
            data = json.loads(request.data)
        except ValueError as e:
            raise BadRequest("Invalid json: {}".format(e))
        created_by = request.headers.get("X-Authenticated-Userid", "Unknown")
        data["created_by"] = created_by
        data["updated_by"] = created_by
        return Pipeline(session, dispatch=self.dispatch).add_stock(data)

    @http('PUT', '/stock_availability/<uuid:stock_availability_id>')
    @authorize('can-update-stock_availability')
    def edit_stock(self, request, stock_availability_id):
        session = self.db.get_session()
        try:
            data = json.loads(request.data)
        except ValueError as e:
            raise BadRequest("Invalid json: {}".format(e))
        data["updated_by"] = request.headers.get(
            "X-Authenticated-Userid", "Unknown")
        data["stock_availability_id"] = stock_availability_id
        return Pipeline(session, dispatch=self.dispatch).update_stock(data)

    @http('DELETE', '/stock_availability/<uuid:stock_availability_id>')
    @authorize('can-update-stock_availability')
    def delete_stock(self, request, stock_availability_id):
        session = self.db.get_session()
        done_by = request.headers.get("X-Authenticated-Userid", "Unknown")
        return Pipeline(session).delete_stock(stock_availability_id, done_by)

    ######################################################################
    #  GRAPHQL
    ######################################################################

    @http('POST', '/graphql')
    def query(self, request):
        return graphql_query(parse_body(request), self.db.get_session())
