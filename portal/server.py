from distutils.util import strtobool
from flask import Flask, Response, jsonify, request, render_template
from flask_swagger_ui import get_swaggerui_blueprint

from portal.metric_data_controller import MetricDataController

import argparse
import requests
import sys
import time
import json

# swagger specific
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "VE-Proxy"
    }
)



class ServiceAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)
        self.app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

    def run(self):
        # Start the process bound to the default adapter on inbound port
        self.app.run(host="0.0.0.0", port=EndpointAction.IN_PORT)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None, Jsonfify=True):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler, Jsonify=Jsonfify), methods=methods)

        # return Response(value, status=200, mimetype='application/json');
        # return self.response


class EndpointAction(object):
    IN_PORT = 5280

    def __init__(self, action, Jsonify=True):
        self.action = action
        self.Jsonify=Jsonify
        self.response = Response(status=200, headers={})
        # self.response = Response(value, status=200, headers={}, mimetype='Text')

    def __call__(self, *args):
        value = self.action()
        return jsonify(value) if self.Jsonify else value
        #return value


class BridgeController:
    """
    Class BridgeController is responsible for accepting REST calls and invoking the proper objects
    """

    DEFAULT_INSTANCE = "DEFAULT_INSTANCE"

    def __init__(self):
        self.initialized = int(round(time.time() * 1000))

    def get_main_page(self):
        return render_template("dbreport.html")

    def get_other_page(self):
        return render_template("other.html")

    def srv_shutdown_server(self):
        """
        SHUTDOWN SERVER TO BE USED IN COMMAND LINE
        """
        ret_value = {'status': 'success'}
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return ret_value


    ##########################################################
    ##  TEST CALL
    ##
    def srv_action_test(self):
        ret_value = {'status': 'success', 'metrics': '', 'actions': ''}


        print(f"CURRENT_STATUS == Metrics qty {ret_value['metrics']} AND Actions qty {ret_value['actions']} ")
        return ret_value
        # return "{'ret_value':'12345'}"


def start_server():
    server = ServiceAppWrapper('RQTA_PORTAL_SRV')
    srv_controller = BridgeController()
    data_controller = MetricDataController()

    # Create the REST endpoints of the exposed services
    server.add_endpoint(endpoint='/',  endpoint_name='main', handler=srv_controller.get_main_page, methods=['GET'], Jsonfify=False)
    server.add_endpoint(endpoint='/testruns/get', endpoint_name='get_testruns', handler=data_controller.srv_get_testruns, methods=['GET'])
    server.add_endpoint(endpoint='/products/get', endpoint_name='get_prodcuts', handler=data_controller.srv_get_products, methods=['GET'])
    server.add_endpoint(endpoint='/metrics/get', endpoint_name='get_metrics', handler=data_controller.srv_get_metrics, methods=['GET'])


    server.add_endpoint(endpoint='/metrics/get/by_build_number', endpoint_name='get_metrics_by_build_number',
                        handler=data_controller.srv_get_metric_by_Build_number, methods=['GET'])

    server.add_endpoint(endpoint='/metrics/get/by_build_number_graph', endpoint_name='get_metrics_by_build_number_graph',
                        handler=data_controller.srv_get_metric_by_Build_number_graph, methods=['GET'])




    server.add_endpoint(endpoint='/other/main',  endpoint_name='other', handler=srv_controller.get_other_page, methods=['GET'], Jsonfify=False)

    server.add_endpoint(endpoint='/shutdown_server', endpoint_name='shutdown_server',
                        handler=srv_controller.srv_shutdown_server, methods=['POST'])

    # TEMPORARY SERVICE
    server.add_endpoint(endpoint='/test_Call', endpoint_name='test_Call', handler=srv_controller.srv_action_test, methods=['GET'])

    # Start the server and loop on action
    server.run()

class TestRuns_Obj:
    def __init__(self, name, date, type):
        self.name = name
        self.date = date
        self.type = type

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_port", type=int, help="Port for REST request.")
    parser.add_argument("-s", "--shutdown", type=strtobool, nargs='?', const=True, default=False,
                        help="Shutdown server.")
    args = parser.parse_args()

    try:
        # accept port configuration from command line or assume defaults
        if args.in_port and 0 < args.in_port < 65535:
            EndpointAction.IN_PORT = args.in_port

        if args.shutdown:
            url_verb = f'http://127.0.0.1:{EndpointAction.IN_PORT}/shutdown_server'
            requests.post(url_verb)
            sys.exit(0)

        # Create Flask class wrapper
        start_server()

        sys.exit(0)
    except Exception as e:
        print("***** ACTION MAIN: FATAL EXCEPTION = " + str(e))
        sys.exit(-1)