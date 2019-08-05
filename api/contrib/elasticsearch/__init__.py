from elasticsearch import Elasticsearch
from django.conf import settings

default_app_config = "contrib.elasticsearch.apps.ElasticsearchDSLConfig"

client = Elasticsearch(hosts=[{"host": settings.ES_HOST, "port": 9200}])


def Client():
    return client
