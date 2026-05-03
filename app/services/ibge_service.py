import httpx

async def get_populacao(cidade: str):
    url =  f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{cidade}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
    if response.status_code != 200:
        print ("Erro IBGE:", response.text)
        return None
    
    data = response.json()
    
    return {
        "nome": data.get("nome"),
        "uf": data.get("microrregiao", {}).get("mesorregiao",{}).get("UF", {}).get("sigla")
    }