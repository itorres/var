import json
from datetime import timedelta

from flask import Flask, make_response, redirect, request, send_from_directory
from kubernetes import client


client.configuration.host = 'http://localhost:8080'
supper_options = dict(
    pizza='https://www.yelp.com/map/al-taglio-bcn-barcelona-4',
    frankfurt='https://www.yelp.com/map/frankfurts-barcelona-2'
)
wat = 'https://www.destroyallsoftware.com/talks/wat'
api = client.ApisApi()
app = Flask(__name__)
app.send_file_max_age_default = timedelta(0)


@app.route('/')
def send_index():
    return send_file('index.html')


@app.route('/<path:path>')
def send_file(path):
    return send_from_directory('/usr/src/app', path)


@app.route('/nodeport')
def get_node_port():
    c = client.CoreV1Api()
    services = c.list_service_for_all_namespaces()
    return json.dumps([{'name': s.metadata.name,'port': s.spec.ports[0].node_port}
                       for s in  services.items if s.spec.type == 'NodePort'])


@app.route('/deployment', methods=['GET'])
def get_deployment():
    c = client.ExtensionsV1beta1Api()
    services = c.read_namespaced_deployment
    deployment = c.read_namespaced_deployment('hello', 'default')
    return deployment.to_str()


@app.route('/supper', methods=['GET'])
def get_supper():
    c = client.ExtensionsV1beta1Api()
    deployment = c.read_namespaced_deployment('hello', 'default')
    supper = get_env(deployment.spec.template.spec.containers[0].env, "SUPPER")
    return redirect(supper_options.get(supper.lower(), wat))


@app.route('/supper', methods=['POST', 'PUT'])
def set_supper():
    c = client.ExtensionsV1beta1Api()
    supper = request.form.get('supper', 'frankfurt')
    patch = {
        "spec":{"template":{"spec":{"containers":[
            {"name": 'hello',  # We must provide the container name as the merge key
             "env": [
                 {'name': 'SUPPER',
                  'value': supper}
             ]
            }
        ]}}}}
    deployment = c.patch_namespaced_deployment('hello', 'default', patch)
    return make_response(supper)


def get_env(env, var):
    for i in env:
        if i.name == var:
            return i.value
    return None


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='9080')
