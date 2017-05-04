import uuid
from datetime import datetime

from cassandra.cqlengine.columns import (UUID,
                                         Text,
                                         Float,
                                         DateTime)
from cassandra.cqlengine.models import Model


class Parameter(Model):
    __table_name__ = 'parameters'

    id = UUID(primary_key=True,
              default=uuid.uuid4)
    group_id = UUID(required=True,
                    index=True)
    name = Text(required=True)
    value = Float(required=True)
    created_timestamp = DateTime(default=datetime.now)
