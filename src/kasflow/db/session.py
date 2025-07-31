from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from kasflow.conf import settings


engine = create_async_engine(settings.database_url, echo=True)
sessionmaker = async_sessionmaker(engine)
