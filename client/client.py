# EXEMPLO DE USO DO EURECA MCP CLIENT

import asyncio

from eureca_mcp_client import EurecaMCPClient

async def main():
    # Para o transporte Streamable HTTP 
    client = EurecaMCPClient(
        {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http"
        }
    )

    # Para o transporte stdio
    client = EurecaMCPClient(
        {
            "command": "uv",
            "args": ["run", "-m", "src.main"], # aqui precisa ser o caminho correto do server
            "transport": "stdio"
        }
    )

    try:
        tools = await client.list_tools()

        print(f"Tools carregadas: {tools}")

        if hasattr(tools, 'tools') and tools.tools:
            print(f"Número de ferramentas: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
        else:
            print("Nenhuma ferramenta encontrada. Verifique se o servidor está funcionando e expondo as tools.")
            return
        
        # Exemplo de como chamar uma ferramenta
        # result = await client.call_tool("nome_da_ferramenta", {"param": "value"})
        # print(f"Resultado: {result}")
    
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.close()
    
if __name__ == "__main__":
    asyncio.run(main())