from fastapi import APIRouter, HTTPException
from app.services.cidade_service import calcular_score, gerar_insight
from app.services.clima_service import get_clima
from app.services.ibge_service import buscar_cidade
from app.database.database import SessionLocal
from app.models.consulta import Consulta

router = APIRouter()

fake_db = {
    "sao paulo": {
        "populacao": 12300000,
        "clima": "quente",
        "custo": "alto"
    },
    "campinas": {
        "populacao": 111000,
        "clima": "ameno",
        "custo": "medio"
    }
}

@router.get("/cidade/{nome}")
async def get_cidade(nome : str):
    cidade = fake_db.get(nome.lower())
    
    if not cidade:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Cidade não encontrada")
    
    clima_real = await get_clima(nome)
    dados_ibge = await buscar_cidade(nome)
    score = calcular_score(cidade, clima_real, dados_ibge)
    insight = gerar_insight(cidade, score)
    
    #salvar no Banco
    db = SessionLocal()
    
    nova_consulta = Consulta(
        cidade= nome,
        score= score,
        insight= insight
    )

    db.add(nova_consulta)
    db.commit()
    db.close()
    
    return {
        "cidade": nome,
        "dados": cidade,
        "score": score,
        "insight": insight,
        "clima_real": clima_real,
        "ibge": dados_ibge
    }
    
@router.get("/historico")
def get_historico(cidade: str = None):
    db = SessionLocal()
    
    if cidade: 
        consultas = db.query(Consulta).filter(Consulta.cidade == cidade).all()
    else:
        consultas = db.query(Consulta).all()
        
    resultado = []
    
    for c in consultas:
        resultado.append({
            "cidade": c.cidade,
            "score": c.score,
            "insight": c.insight
        })
    
    db.close()
    
    return resultado

@router.get("/Comparar")
async def comparar(cidades: str):
    lista_cidades = cidades.split(",")
    
    resultado = []
    
    for nome in lista_cidades:
        cidade = fake_db.get(nome.lower())
        
        if not cidade:
            continue #ignora se não existir
        
        clima_real = await get_clima(nome)
        dados_ibge = await buscar_cidade(nome)
        
        score = calcular_score(cidade, clima_real, dados_ibge)
        insight = gerar_insight(cidade, score)
        
        resultado.append({
            "cidade": nome,
            "score": score,
            "temperatura": clima_real["temperatura"] if clima_real else None,
            "insight": gerar_insight(cidade, score)
        })
        
    #ordenar por score (maior primeiro)
    resultado.sort(key=lambda x: x["score"], reverse=True)
    
    #adicionar posição
    for i, item in enumerate(resultado):
        item["posicao"] = i+ 1
    
    return resultado
    
@router.get("/recomendar")
async def recomendar(cidades: str):
    lista_cidades = cidades.split(",")
    
    melhor = None
    
    for nome in lista_cidades:
        cidade = fake_db.get(nome.lower())
        
        if not cidade:
            continue
        
        clima_real = await get_clima(nome)
        dados_ibge = await buscar_cidade(nome)
        score = calcular_score(cidade,clima_real, dados_ibge)
        
        if not melhor or score > melhor ["score"]:
            melhor = {
                "cidade":nome,
                "score":score,
                "temperatura": clima_real["temperatura"] if clima_real else None,
                "insight": gerar_insight(cidade, score)
            }
    return melhor
