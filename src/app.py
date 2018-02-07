# Let's get this party started
import falcon
import pascua

# falcon.API instances are callable WSGI apps
app = falcon.API()
pascua.init(app)
