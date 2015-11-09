
from .. import ValidationStatus, FieldValidationInfo
from .observable import ObservableValidationInfo
import re


class DomainNameValidationInfo(ObservableValidationInfo):

    TYPE = 'DomainNameObjectType'

    FQDN_TYPE = 'FQDN'
    TLD_TYPE = 'TLD'

    FQDN_MATCHER = re.compile(r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', re.IGNORECASE)
    TLD_MATCHER = re.compile(r'^\.?[a-z]{2,63}$', re.IGNORECASE)

    def __init__(self, **field_validation):
        super(DomainNameValidationInfo, self).__init__(DomainNameValidationInfo.TYPE, **field_validation)
        self.value = field_validation.get('value')
        self.type = field_validation.get('type')

    @classmethod
    def validate(cls, **observable_data):
        domain_type = observable_data.get('type')
        value = observable_data.get('value')

        value_validation = None
        type_validation = None

        domain_matcher = None
        if domain_type == cls.FQDN_TYPE:
            domain_matcher = cls.FQDN_MATCHER
        elif domain_type == cls.TLD_TYPE:
            domain_matcher = cls.TLD_MATCHER

        if domain_matcher:
            if value:
                if not domain_matcher.match(value):
                    value_validation = FieldValidationInfo(ValidationStatus.WARN,
                                                           'Domain value is invalid %s' % domain_type)
            else:
                value_validation = FieldValidationInfo(ValidationStatus.ERROR, 'Domain value is missing')
        else:
            type_validation = FieldValidationInfo(
                ValidationStatus.ERROR, 'Domain type is missing' if domain_type else 'Unrecognizable domain type')

        return cls(type=type_validation, value=value_validation, description=observable_data.get('description'))

    @classmethod
    def get_domain_type_from_value(cls, value):
        if cls.FQDN_MATCHER.match(value):
            return cls.FQDN_MATCHER
        if cls.TLD_MATCHER.match(value):
            return cls.TLD_TYPE

        return None
