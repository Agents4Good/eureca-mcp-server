import logging, sys, asyncio
from dotenv import load_dotenv

from .helpers.args_utils import *
from .server import mcp

# carregar tools
from .tools.curso import buscar_curso, buscar_todos_cursos_por_campus
from .tools.disciplina import buscar_disciplina_curso

load_dotenv()

async def listar_tools():
    """
    Lista todas as tools registradas no servidor
    """
    tools = await mcp.list_tools()
    print("\n🔧 TOOLS REGISTRADAS:")
    print("=" * 50)
    #print(tools)
    
    if not tools:
        print("Nenhuma tool registrada")
        return
    
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool.name}")
        print(f"   Descrição: {tool.description}")
        if hasattr(tool, 'input_schema') and tool.input_schema:
            if 'properties' in tool.input_schema:
                params = list(tool.input_schema['properties'].keys())
                print(f"   Parâmetros: {', '.join(params)}")
        print()

if __name__ == "__main__":
    args = parse()
    config = args_config(args)

    #asyncio.run(listar_tools()) # apenas para visualização

    try:
        if args.transport == "http":
            mcp.settings.host = config["host"]
            mcp.settings.port = config["port"]
            logging.info(f"Starting server on http://{config['host']}:{config['port']}")
            mcp.run(transport="streamable-http")
        else:
            logging.info("Starting server with stdio transport...")
            mcp.run(transport="stdio")
    except Exception as e:
        logging.error(f"Error starting the MCP Server: {e}")
        sys.exit(1)