import re
from marshmallow import fields, ValidationError


class FieldValidator:
    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        validator_list = (self._get_min_length_validator(min_length) +
                          self._get_max_length_validator(max_length) +
                          kwargs.pop('validate', []))

        super().__init__(
            validate=validator_list,
            *args,
            **kwargs,
        )

    @staticmethod
    def _get_min_length_validator(min_length):
        def _validator(data):
            if len(data) < min_length:
                raise ValidationError(
                    message=serialization_error['min_length_error'].format(
                        min_length))

        return [_validator] if min_length else []

    @staticmethod
    def _get_max_length_validator(max_length):
        def _validator(data):
            if len(data) > max_length:
                raise ValidationError(
                    message=f'Must not exceed {max_length}'
                )

        return [_validator] if max_length else []


class StringField(FieldValidator, fields.String):
    def __init__(self, *args, capitalize=False, **kwargs):
        self.capitalize = capitalize
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        """This method is called when data is being loaded to python

        It removes the all surrounding spaces and changes double spaces to one space

b
        Args:
            value: value send from user
            attr: the field name
            data:  The raw input data passed to the Schema.load.
            **kwargs: Field-specific keyword arguments.

        Returns:
            (str):  A deserialized value with no double-space

        """
        des_value = super()._deserialize(value, attr, data, **kwargs)

        des_value = re.sub("\\s{2,}", " ", des_value.strip())
        if self.capitalize:
            des_value = des_value.capitalize()
        return des_value
