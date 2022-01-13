from django.views.generic import ListView

from .models import Soft
from .samparser import nnmclub_list

torr = ["samdrivers"] + nnmclub_list


class IndexView(ListView):
    model = Soft
    template_name = "soft/index.html"

    def get_queryset(self):
        return self.model.objects.prefetch_related("links").all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        qs = list(self.object_list)
        context["soft_list"] = [i for i in qs if i.url_key not in torr]
        context["torrent_list"] = [i for i in qs if i.url_key in torr[1:]]
        context["drv_list"] = [i for i in qs if i.url_key == torr[0]]
        return context
