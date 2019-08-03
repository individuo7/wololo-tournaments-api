from elasticsearch_dsl import Document, Integer, Text


class UserDocument(Document):
    username = Text()
    gold = Integer()

    class Index:
        name = "user"
