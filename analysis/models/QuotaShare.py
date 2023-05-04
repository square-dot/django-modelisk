from analysis.models.Coverage import Coverage
from django.db.models import FloatField


class QuotaShare(Coverage):
    share = FloatField(default=1)

    def type_name(self) -> str:
        return "Quota Share"

    def __repr__(self):
        return self.type_name()

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str]]:
        return [("Share", "{:.0f}%".format(self.share * 100))]