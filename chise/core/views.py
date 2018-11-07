from django.shortcuts import render
from django.views import generic
from chise import settings

class VNCView(generic.RedirectView):
    permanent = False
    url = None

    def get_redirect_url(self, *args, **kwargs):
        scheme = 'https' if self.request.is_secure() else 'http'        
        self.url = scheme + '://' + settings.DOMAIN + ':6080/vnc_lite.html'

        return super().get_redirect_url(self, *args, **kwargs)



