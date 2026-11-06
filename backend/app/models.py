from sqlalchemy import Column, Integer, BigInteger, Text, Date, DateTime, ForeignKey
from sqlalchemy import func
from app.database import Base


class Camp(Base):
    __tablename__ = "camp"
    id = Column(BigInteger, primary_key = True)
    name = Column(Text, nullable = False)
    join_code = Column(Text, nullable = False, unique = True)
    start_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = False)
    deleted_at = Column(DateTime(timezone = True))

class Calendar(Base):
    __tablename__ = "calendar"
    id = Column(BigInteger, primary_key = True)
    camp_id = Column(BigInteger, ForeignKey("camp.id"), nullable = False)
    name = Column(Text, nullable = False)

class Leader(Base):
    __tablename__ = "leader"
    id = Column(BigInteger, primary_key = True)
    full_name = Column(Text, nullable = False)
    

class TimeBlock(Base):
    __tablename__ = "time_block"
    id = Column(BigInteger, primary_key = True)
    calendar_id = Column(BigInteger, ForeignKey("calendar.id"), nullable = False)
    title = Column(Text, nullable = False)
    starts_at = Column(DateTime(timezone = True), nullable = False)
    ends_at = Column(DateTime(timezone = True), nullable = False)
    responsible_leader_id = Column(BigInteger, ForeignKey("leader.id"))
    description = Column(Text)
 
class CampClass(Base):
    __tablename__ = "camp_class"
    id = Column(BigInteger, primary_key = True)
    camp_id = Column(BigInteger, ForeignKey("camp.id"), nullable = False)
    name = Column(Text, nullable = False)

class Station(Base):
    __tablename__ = "station"
    id = Column(BigInteger, primary_key = True)
    camp_id = Column(BigInteger, ForeignKey("camp.id"), nullable = False)
    name = Column(Text, nullable = False)
    
class Team(Base):
    __tablename__ = "team"
    id = Column(BigInteger, primary_key = True)
    camp_id = Column(BigInteger, ForeignKey("camp.id"), nullable = False)
    name = Column(Text, nullable = False)
    class_id = Column(BigInteger, ForeignKey("camp_class.id"))
    station_id = Column(BigInteger, ForeignKey("station.id"))
  
class CampMembership(Base):
    __tablename__ = "camp_membership"
    camp_id = Column(BigInteger, ForeignKey("camp.id"), primary_key = True)
    leader_id = Column(BigInteger, ForeignKey("leader.id"), primary_key = True)
    role = Column(Text, nullable = False)
    team_id = Column(BigInteger, ForeignKey("team.id"))

class BlockAssignment(Base):
    __tablename__ = "block_assignment"
    time_block_id = Column(BigInteger, ForeignKey("time_block.id"), primary_key = True)
    class_id = Column(BigInteger, ForeignKey("camp_class.id"), primary_key = True)
    station_id = Column(BigInteger, ForeignKey("station.id"), nullable = False)
    
class Resource(Base):
    __tablename__ = "resource"
    id = Column(BigInteger, primary_key = True)
    time_block_id = Column(BigInteger, ForeignKey("time_block.id"), nullable = False)
    kind = Column(Text, nullable = False)
    label = Column(Text, nullable = False)
    url = Column(Text, nullable = False)
    
class PointEvent(Base):
    __tablename__ = "point_event"
    id = Column(BigInteger, primary_key = True)
    class_id = Column(BigInteger, ForeignKey("camp_class.id"), nullable = False)
    awarded_by = Column(BigInteger, ForeignKey("leader.id"), nullable = False)
    time_block_id = Column(BigInteger, ForeignKey("time_block.id"))
    amount = Column(Integer, nullable = False)
    reason = Column(Text, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    
class Account(Base):
    __tablename__ = "account"
    id = Column(BigInteger, primary_key = True)
    leader_id = Column(BigInteger, ForeignKey("leader.id"), nullable = False)
    google_sub = Column(Text, nullable = False, unique = True)
    email = Column(Text, nullable = False, unique = True)
    
class LeaderOverride(Base):
    __tablename__ = "leader_override"
    time_block_id = Column(BigInteger, ForeignKey("time_block.id"), primary_key = True)
    leader_id = Column(BigInteger, ForeignKey("leader.id"), primary_key = True)
    station_id = Column(BigInteger, ForeignKey("station.id"))
    note = Column(Text)