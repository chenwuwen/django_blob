from datetime import datetime, date
import json
from json import JSONEncoder
from decimal import Decimal

from django.core.exceptions import ValidationError

'''自定义json解析器'''


class JsonCustomEncoder(JSONEncoder):
    def default(self, field):
        if isinstance(field, ValidationError):
            return {'code': field.code, 'message': field.message}
        elif isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        # 如果是小数类型
        elif isinstance(field, Decimal):
            return str(field)
        else:
            return json.JSONEncoder.default(self, field)
