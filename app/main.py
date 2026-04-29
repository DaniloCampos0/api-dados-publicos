from fastapi import FastAPI
from app.database.database import SessionLocal, engine, Base
from app.models.consulta import Consulta
from app.services.cidade_service import calcular_score, gerar_insight
from app.services.clima_service import get_clima

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/")
def home():
    
    return {"mensagem": "API funcionando"}

@app.get("/cidade/{nome}")
async def get_cidade(nome : str):
    cidade = fake_db.get(nome.lower())
    
    if not cidade:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Cidade não encontrada")
    
    score = calcular_score(cidade)
    insight = gerar_insight(cidade, score)
    clima_real = await get_clima(nome)
    
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
        "clima_real": clima_real
    }
    
@app.get("/historico")
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

@app.get("/Comparar")
def comparar(cidades: str):
    lista_cidades = cidades.split(",")
    
    resultado = []
    
    for nome in lista_cidades:
        cidade = fake_db.get(nome.lower())
        
        if not cidade:
            continue #ignora se não existir
        
        score = calcular_score(cidade)
        
        resultado.append({
            "cidade": nome,
            "score": score,
            "insight": gerar_insight(cidade, score)
        })
        
    #ordenar por score (maior primeiro)
    resultado.sort(key=lambda x: x["score"], reverse=True)
    
    for i, item in enumerate(resultado):
        item["posicao"] = i+ 1
    
    return resultado
    
