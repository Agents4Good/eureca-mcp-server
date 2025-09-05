import logging, httpx

from typing import Any, Optional

from ...server import mcp
from ...helpers.func_utils import get_func_info
from ...helpers.tool_handlers.tools_requests import buscar_curso_por_nome_ou_codigo

@mcp.tool(annotations={'domain': 'curso'})
async def buscar_curso(curso: Any, campus: Optional[Any] = "") -> list[dict]:
    """
    Retorna um curso específico oferecido em um campus específico da UFCG.

    Args:
        curso (Any): Pode ser o nome do curso por escrito ou o código numérico dele.
        campus (Optional[Any], optional): Pode ser o nome do campus ou o código numérico dele (opcional).
    
    Returns:
        list[dict]: Lista com curso no formato:
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

    func_name, parametros_str = get_func_info()

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")
        data, _ = await buscar_curso_por_nome_ou_codigo(curso, campus)
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
        logging.warning(f"Erro interno na tool {func_name}: {e}")
        raise Exception(f"Erro interno na tool {func_name}: {e}")