from pydantic import BaseModel
from typing import Optional

class ClimaResponse(BaseModel):
    temperatura: float
    descricao: str
    
class IBGEResponse(BaseModel):
    id: int
    nome: str
    uf: str
    
class CidadeDados(BaseModel):
    populacao: Optional[int] = None
    clima : str
    custo: str
    
class CidadeResponse(BaseModel):
    cidade: str
    dados: CidadeDados
    score: int
    insight: str
    clima_real: Optional[ClimaResponse] = None
    ibge: Optional[IBGEResponse] = None