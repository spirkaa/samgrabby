import logging

from django.db import models

from .decorators import async_f

logger = logging.getLogger(__name__)


class Soft(models.Model):
    name = models.CharField("app name", max_length=100)
    version = models.CharField("app version", max_length=100)
    upd_date = models.DateField("date updated")
    url_key = models.SlugField("url slug", unique=True)

    class Meta:
        verbose_name = "Soft entry"
        verbose_name_plural = "Soft entries"
        ordering = ["-upd_date"]

    def __str__(self):
        return str(self.name)


class DownLink(models.Model):
    soft = models.ForeignKey(Soft, related_name="links", on_delete=models.CASCADE)
    dl_url = models.URLField("download url")
    dl_url_text = models.CharField("text for download url", max_length=100)

    def __str__(self):
        return str(self.dl_url_text)


@async_f
def update_db():
    from .samparser import get_soft_data

    data = get_soft_data()
    for entry in data:
        obj, _ = Soft.objects.update_or_create(
            url_key=entry.url_key,
            defaults={
                "name": entry.name,
                "version": entry.version,
                "upd_date": entry.upd_date,
            },
        )
        DownLink.objects.filter(soft=obj).delete()
        for link in entry.links:
            DownLink(soft=obj, dl_url=link.dl_url, dl_url_text=link.dl_url_text).save()
