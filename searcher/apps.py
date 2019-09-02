from django.apps import AppConfig


class SearcherConfig(AppConfig):
    name = 'searcher'

    def ready(self):
        import searcher.signals
