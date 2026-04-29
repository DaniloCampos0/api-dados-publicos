
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
