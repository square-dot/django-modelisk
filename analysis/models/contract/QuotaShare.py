from analysis.models.contract.BaseContract import BaseContract, BaseExcessOfLoss
from django.db.models import FloatField, CharField
from django.urls import reverse


class QuotaShare(BaseContract):
    share = FloatField(default=1)


    def type_string(self) -> str:
        return "Quota Share"
    
    def get_absolute_url(self) -> str:
        return reverse("quota-share", args=[str(self.pk)])

    def __repr__(self):
        return f"{self.code}"

    def __str__(self) -> str:
        return self.__repr__()

    def get_fields(self) -> list[tuple[str, str, str]]:
        l = self.get_base_fields()
        l.insert(0, ("Code", "", self.code))
        l.append(("Share", "", "{:.0f}%".format(self.share * 100)))
        return l