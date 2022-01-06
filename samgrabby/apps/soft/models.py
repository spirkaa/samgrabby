from django.db import models
from .decorators import async_f
from .samparser import parser


class Soft(models.Model):
    name = models.CharField('app name', max_length=100)
    version = models.CharField('app version', max_length=100)
    upd_date = models.DateField('date updated')
    url_key = models.SlugField('url slug', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Soft entry'
        verbose_name_plural = 'Soft enries'
        ordering = ["-upd_date"]


class DownLink(models.Model):
    soft = models.ForeignKey(Soft, related_name='links', on_delete=models.CASCADE)
    dl_url = models.URLField('download url')
    dl_url_text = models.CharField('text for download url', max_length=100)

    def __str__(self):
        return self.dl_url_text


def add_links(links, itempk):
    for link in links:
        DownLink(dl_url=link[1], dl_url_text=link[0], soft_id=itempk).save()


def db_operations(results, operation):
    for r in results:
        if operation == 'populate':
            try:
                item = Soft(name=r['name'],
                            version=r['version'],
                            upd_date=r['upd_date'],
                            url_key=r['url_key'])
                item.save()
                if item.pk:
                    add_links(r['links'], item.pk)
            except:
                pass
        elif operation == 'update':
            item, created = Soft.objects.get_or_create(
                url_key=r['url_key'],
                defaults={'name': r['name'],
                          'version': r['version'],
                          'upd_date': r['upd_date']})
            if created:
                add_links(r['links'], item.pk)
            elif item.upd_date < r['upd_date']:
                item.version = r['version']
                item.upd_date = r['upd_date']
                item.save()
                DownLink.objects.filter(soft_id=item.id).delete()
                add_links(r['links'], item.pk)


@async_f
def run_db_oper(operation):
    results = parser()
    db_operations(results, operation)
