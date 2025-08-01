import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from kasflow.conf import settings


echo = True if getattr(logging, settings.log_level.upper()) < logging.INFO else False
engine = create_async_engine(settings.database_url, echo=echo)
sessionmaker = async_sessionmaker(engine)
