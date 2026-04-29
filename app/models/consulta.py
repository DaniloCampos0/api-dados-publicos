from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Consulta(Base):
    
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(String)
    score = Column(Integer)
    insight = Column(String)