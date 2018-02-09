from django.conf.urls import url
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from netAngels.models import Link


class CodeLinkResource(ModelResource):
    class Meta:
        authorization = Authorization()
        queryset = Link.objects.all()
        resource_name = 'code'

    def prepend_urls(self):
        """
        bind "process" to url
        :return:
        """
        return [url(r'^code/$', self.wrap_view('process'))]

    def process(self, request, **kwargs):
        """
        Got request with param 'url' or 'hash'.
        If param is 'hash' - return full url, hash for url would be returned otherwise
        :param request:
        :param kwargs:
        :return: example: {"hash": "799001133"} or {"url": "http://123.ru"}
        """
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        param_url = data.get('url', None)

        if param_url:
            try:
                l = Link.objects.get(url=data.get('url', ''))
            except Link.DoesNotExist:
                l = Link(click_count=0, url=param_url, hash=hash(param_url))
                l.save()
                return self.create_response(request, {'hash': l.hash})
            return self.create_response(request, {'hash': l.hash})
        else:
            try:
                l = Link.objects.get(hash=data.get('hash', ''))
            except Link.DoesNotExist:
                return self.create_response(request, {'error': 'DoesNotExist'})
            l.inc_clicks()
            return self.create_response(request, {'url': l.url})
