from django.shortcuts import render
from django.views import generic
from urllib.parse import urljoin

class VNCView(generic.RedirectView):
    permanent = True
    url = None

    def get_redirect_url(self, *args, **kwargs):
        scheme = 'https' if self.request.is_secure() else 'http'
        base_url = self.request.META.get('SERVER_NAME')
        self.url = scheme + '://' + base_url + ':6080/vnc_lite.html'
        
        return super().get_redirect_url(self, *args, **kwargs)



