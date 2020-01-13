from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from elasticsearch_dsl.connections import connections


class ElasticsearchDSLConfig(AppConfig):
    name = "elasticsearch"
    verbose_name = _("Elasticsearch")

    def ready(self):
        try:
            connections.get_connection()
        except KeyError:
            connections.create_connection(hosts=[settings.ES_HOST])
