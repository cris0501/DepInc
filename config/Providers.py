from Providers import *

providers = {
    'DB': dbProvider(),
    'Event': eventProvider()
}

def getProvider(name):
    return providers.get(name)
