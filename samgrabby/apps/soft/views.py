from django.views.generic import ListView

from .models import Soft

drv = "samdrivers"


class IndexView(ListView):
    model = Soft
    template_name = "soft/index.html"

    def get_queryset(self):
        return self.model.objects.prefetch_related("links").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = list(self.object_list)
        context["soft_list"] = [i for i in qs if i.url_key != drv]
        context["drv_list"] = [i for i in qs if i.url_key == drv]
        return context
