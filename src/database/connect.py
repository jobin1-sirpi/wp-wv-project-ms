import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..core.config import settings


#####################
# Database Connection
#####################
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


##################
# Redis Connection
##################
def init_redis_pool():
    redis_host = settings.REDIS_HOST
    redis_port = settings.REDIS_PORT
    redis_user = settings.REDIS_USERNAME
    redis_pass = settings.REDIS_PASSWORD
    pool = redis.ConnectionPool(
        host=redis_host, port=redis_port, username=redis_user, password=redis_pass, db=0
    )
    return pool


redis_client = redis.Redis(connection_pool=init_redis_pool())
