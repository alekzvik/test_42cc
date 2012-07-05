from requests_log.models import RequestEntry


class RequestsLogMiddleware(object):
    "Simple Middleware that stores all requests and put them in db"

    def process_request(self, request):
        path = request.path
        method = request.method
        query = request.META.get('QUERY_STRING', '')
        RequestEntry(path=path, method=method, query=query).save()
