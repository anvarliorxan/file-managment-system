from django.core.validators import RegexValidator


phone_message = "Phone number must be in this format: 994xxxxxxxxx"
phone_regex = RegexValidator(regex=r"994\s?\d{2}[2-9]\d{6}", message=phone_message)
