from datetime import datetime, timezone
from api.utils.messages import TIME_IN_PAST_ERROR
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
                    message=f'Must be more than {min_length}')

        return [_validator] if min_length else []

    @staticmethod
    def _get_max_length_validator(max_length):
        def _validator(data):
            if len(data) > max_length:
                raise ValidationError(message=f'Must not exceed {max_length}')

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


class DateTimeField(fields.DateTime):
    def __init__(self, must_be_in_future=False, tz=None, *args, **kwargs):
        validator_list = (
                self._get_validate_datetime(must_be_in_future) +
                kwargs.pop('validate', [])
        )
        self.tz= None
        if tz:
            self.tz =getattr(timezone, tz)
        super().__init__(*args, validate=validator_list, **kwargs)

    def _get_validate_datetime(self, time_in_future):
        def _validator(data):
            if data < datetime.now(tz=self.tz):
                raise ValidationError(message=TIME_IN_PAST_ERROR)

        return [_validator] if time_in_future else []