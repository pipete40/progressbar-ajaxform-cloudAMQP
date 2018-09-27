from django.http import HttpResponse


def view_503(request):
    html = "<html><body> There are problems with the internet connection. </body></html>"
    return HttpResponse(html, status=503)
