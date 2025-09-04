import httpx, traceback
from typing import Any

async def make_request(url: str, params: dict = {}) -> dict[str, Any] | None:
    """
    Faz uma requisição GET com tratamento de erros.
    """
    
    headers = {
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
            print("🟢 Status Code:", response.status_code)
            print("🟢 Content-Type:", response.headers.get("Content-Type"))
            print("🟢 Response Text:", response.text[:300])  # Mostra parte da resposta pra debug
            return response.json()
        
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            try:
                mensagem = e.response.json()
            except Exception:
                mensagem = e.response.text

            print("❌ Erro HTTP:")
            print("Código:", status_code)
            print("Mensagem:", mensagem)
            traceback.print_exc()
            raise

        except Exception as e:
            print("❌ Erro inesperado:")
            print("Tipo:", type(e).__name__)
            print("Mensagem:", str(e))
            traceback.print_exc()
            raise