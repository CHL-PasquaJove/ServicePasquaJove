# Let's get this party started
import falcon
import resources

# falcon.API instances are callable WSGI apps
app = falcon.API()
resources.init(app)
