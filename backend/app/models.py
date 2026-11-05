from sqlalchemy import Column, BigInteger, Text, Date, DateTime
from app.database import Base


class Camp(Base):
    __tablename__ = "camp"
    id = Column(BigInteger, primary_key = True)
    name = Column(Text, nullable = False)
    join_code = Column(Text, nullable = False, unique = True)
    start_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = False)
    deleted_at = Column(DateTime(timezone = True))
    
    