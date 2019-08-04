from elasticsearch_dsl import Document, Integer, Text


class PlayerDocument(Document):
    tournament = Text()
    username = Text()
    gold = Integer()

    class Index:
        name = "player"
