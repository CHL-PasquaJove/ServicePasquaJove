# Let's get this party started
import falcon
import resources


def cors_middleware(request, response, params):
    response.set_header(
        'Access-Control-Allow-Origin',
        '*'
    )
    response.set_header(
        'Access-Control-Allow-Headers',
        'Content-Type, Api-Token'
    )
    # This could be overridden in the resource level
    response.set_header(
        'Access-Control-Expose-Headers',
        'Location'
    )


# falcon.API instances are callable WSGI apps
app = falcon.API(before=[cors_middleware])
resources.init(app)
