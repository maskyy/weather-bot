from datetime import datetime

from peewee import BigIntegerField, IdentityField, Model, TextField
from playhouse.postgres_ext import DateTimeTZField, PostgresqlExtDatabase

from .config import CONFIG
from .logger import log


db = PostgresqlExtDatabase(CONFIG["DB_URI"])


class Record(Model):
    record_id = IdentityField(generate_always=True)
    message_id = BigIntegerField()
    from_id = BigIntegerField(null=True)
    chat_id = BigIntegerField(null=True)
    message_date = DateTimeTZField()
    request = TextField()
    response = TextField()

    class Meta:
        database = db
        table_name = "records"


db.connect()


def create_tables():
    db.create_tables([Record])


def add_record(
    msg_id: int,
    from_id: int,
    chat_id: int,
    msg_epoch: int,
    msg_text: str,
    response: str,
) -> int | None:
    try:
        record = Record.create(
            message_id=msg_id,
            from_id=from_id,
            chat_id=chat_id,
            message_date=datetime.fromtimestamp(msg_epoch),
            request=msg_text,
            response=response,
        )
        log.debug("Added record %s", record.record_id)
        return record.record_id
    except Exception as e:
        log.warning("Error adding message: %s", e)
        return None
