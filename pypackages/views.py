import datetime
from django.shortcuts import render
from django.http import HttpResponse

from django.views import View
from django.views.generic import TemplateView

from users.mixins import LoggedInOnlyView


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class CurrentTimeClassView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        template_path = 'index.html'
        now = datetime.datetime.now()
        return render(request, template_path, {'time': now})


class UTCClassView(LoggedInOnlyView, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(UTCClassView, self).get_context_data(**kwargs)
        utc_now = datetime.datetime.now(datetime.UTC)
        context.update(
            {
                'time': utc_now,
            }
        )
        return context