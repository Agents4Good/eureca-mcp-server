import logging, httpx

from typing import Any, Optional

from ...server import mcp

from ...data.campi import campi
from ...data.config import BASE_URL
from ...helpers.request_utils import make_request
from ...helpers.func_utils import get_func_info

from ...helpers.tool_handlers.fuzzy_matching import extract_most_similar

@mcp.tool()
async def buscar_todos_cursos_por_campus(campus: Optional[Any] = "") -> list[dict]:
    """
    Retorna todos os cursos oferecidos em um campus específico da UFCG.

    Args:
        campus (Optional[Any], optional): Código do campus (opcional).

    Returns:
        list[dict]: Lista de cursos no formato:
            {
                "codigo_do_curso": int,         # Código do curso
                "descricao": str,               # Nome e descrição do curso
                "status": str,                  # Status do curso (ex.: "ATIVO")
                "grau_do_curso": str,           # Grau (ex.: "GRADUACAO")
                "codigo_do_setor": int,         # Código do setor
                "nome_do_setor": str,           # Nome do setor responsável
                "campus": int,                  # Código do campus
                "nome_do_campus": str,          # Nome do campus
                "turno": str,                   # Turno de funcionamento (ex.: "Matutino")
                "periodo_de_inicio": str,       # Período letivo de início (ex.: "2017.1")
                "data_de_funcionamento": str,   # Data de início do funcionamento
                "codigo_inep": int,             # Código INEP do curso
                "modalidade_academica": str,    # Modalidade acadêmica (ex.: "BACHARELADO")
                "curriculo_atual": int,         # Ano do currículo vigente
                "area_de_retencao": int,        # Código da área de retenção
                "ciclo_enade": int              # Ciclo do ENADE
            }
    """

    campus = str(campus)
    params = {
        "status": "ATIVOS",
        "campus": campus if (campus.isdigit() or campus == "") else extract_most_similar(campus, campi, "campus")[0][0]['codigo']
    }

    func_name, parametros_str = get_func_info()
    url = f"{BASE_URL}/cursos"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data = await make_request(url, params)

        if not data:
            return ["Não foi possível obter os cursos ou nenhum curso foi encontrado"]
 
        return data
    
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        try:
            msg = e.response.json()
        except Exception:
            msg = e.response.text
        logging.warning(f"Erro HTTP na tool {func_name}: {status} - {msg}")
        raise Exception(f"Erro HTTP na tool {func_name}: {status} - {msg}")
    
    except Exception as e:
        logging.exception(f"Erro interno inesperado na tool {func_name}: {e}")
        raise Exception(f"Erro interno inesperado na tool {func_name}: {e}")