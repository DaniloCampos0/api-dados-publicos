import httpx

BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios"

async def buscar_cidade(nome : str):
    
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL)
        
    if response.status_code != 200:
        print("Erro IBGE:", response.text)
        return None
    
    cidades = response.json()
    
    for cidade in cidades:
        if cidade["nome"].lower() == nome.lower():
            return {
                "id": cidade["id"],
                "nome": cidade["nome"],
                "uf": "SP"
    }