from fastapi import FastAPI
from app.database.database import SessionLocal, engine, Base
from app.models.consulta import Consulta

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


def calcular_score(dados):
    score = 0
    
    #custo
    if dados["custo"] == "baixo":
        score += 3
    elif dados["custo"] == "medio":
        score += 2
    else: 
        score += 1
        
    #clima
    if dados["clima"] == "ameno":
        score += 3
    else: 
        score +=1
    return score

def gerar_insight(dados, score):
   
    if dados["custo"] == "alto":
        return "custo de vida elevado pode ser um problema"
    
    if dados["clima"] == "quente":
        return "clima quente pode impactar qualidade de vida"
    
    if score >= 5:
        return "cidade com bom custo-benefício"
    
    return "cidade com características medianas"

@app.get("/cidade/{nome}")
def get_cidade(nome : str):
    cidade = fake_db.get(nome.lower())
    
    if not cidade:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Cidade não encontrada")
    
    score = calcular_score(cidade)
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
        "insight": insight
    }
    
@app.get("/historico")
def get_historico():
    db = SessionLocal()
    
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
