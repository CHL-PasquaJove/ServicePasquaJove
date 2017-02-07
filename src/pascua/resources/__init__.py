from error_codes import ErrorCodesResource
from api import load_api


def load_resources(app, base_url):
    # Load api
    load_api(app, base_url + '/api')

    # Login pasqua
    app.add_route(base_url + '/error-codes.js', ErrorCodesResource())
