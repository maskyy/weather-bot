from datetime import datetime

from peewee import BigIntegerField, IdentityField, Model, TextField
from playhouse.postgres_ext import DateTimeTZField, PostgresqlExtDatabase

from .config import CONFIG
from .logger import logger


db = PostgresqlExtDatabase(CONFIG["DB_URI"])


class Record(Model):
    record_id = IdentityField(generate_always=True)
    message_id = BigIntegerField(null=False)
    message_date = DateTimeTZField(null=False)
    request_text = TextField(null=False)
    response_text = TextField(null=False)

    class Meta:
        database = db
        table_name = "records"


db.connect()


def create_tables():
    db.create_tables([Record])


def add_record(msg_id: int, msg_epoch: int, msg_text: str, response: str) -> int | None:
    try:
        record = Record.create(
            message_id=msg_id,
            message_date=datetime.fromtimestamp(msg_epoch),
            request_text=msg_text,
            response_text=response,
        )
        logger.debug("Added record %s", record.record_id)
        return record.record_id
    except Exception as e:
        logger.warning("Error adding message: %s", e)
        return None
