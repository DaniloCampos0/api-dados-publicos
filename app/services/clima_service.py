import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

async def get_clima(cidade: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={API_KEY}&lang=pt_br&units=metric"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
    print(response.status_code)
    print(response.text)
        
    data = response.json()
    
    if response.status_code != 200:
        return None
    
    return {
        "temperatura": data["main"]["temp"],
        "descricao": data["weather"][0]["description"]
    }