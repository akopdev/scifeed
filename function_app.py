import azure.functions as func

import scifeed

app = func.AsgiFunctionApp(app=scifeed.app, http_auth_level=func.AuthLevel.ANONYMOUS)
