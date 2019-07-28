from rest_framework.schemas import AutoSchema


class CustomSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        link = super().get_link(path, method, base_url)
        link._fields += self.get_core_fields()
        return link

    def get_core_fields(self):
        return getattr(self.view, "coreapi_fields", ())
