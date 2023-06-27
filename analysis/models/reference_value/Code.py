from django.db.models import Model, CharField, PositiveIntegerField


class Code(Model):
    alphabetic_code = CharField(max_length=3)
    numeric_code = PositiveIntegerField()

    @staticmethod
    def create_next_code(prefix):
        q = Code.objects.filter(alphabetic_code=prefix).order_by('numeric_code')
        if q.count() == 0:
            nc = 1
        else:
            nc = q.reverse()[0].numeric_code + 1
        c = Code.objects.create(alphabetic_code=prefix, numeric_code = nc)
        return c
    
    @staticmethod
    def next_program_code():
        prefix = "P"
        return Code.create_next_code(prefix)
    
    @staticmethod
    def next_layer_code():
        prefix = "L"
        return Code.create_next_code(prefix)
    
    @staticmethod
    def next_contract_code():
        prefix = "C"
        return Code.create_next_code(prefix)

    @staticmethod
    def next_analysis_code():
        prefix = "A"
        return Code.create_next_code(prefix)
    
    @staticmethod
    def next_risk_profile_code():
        prefix = "R"
        return Code.create_next_code(prefix)
    
    @staticmethod
    def next_loss_profile_code():
        prefix = "S"
        return Code.create_next_code(prefix)
    
    @staticmethod
    def get_code(code_string):
        return Code.objects.filter(alphabetic_code=code_string[0]).get(numeric_code=int(code_string[1:]))
    
    def __str__(self):
        return f"{self.alphabetic_code}{str(self.numeric_code).zfill(5)}"
    
    class Meta:
        unique_together = [('alphabetic_code', 'numeric_code')]
