import logging, httpx

from typing import Any, Optional

from ...server import mcp

from ...data.config import BASE_URL
from ...helpers.func_utils import get_func_info
from ...helpers.request_utils import make_request

from ...helpers.tool_handlers.fuzzy_matching import extract_most_similar, format_subject_results
from ...helpers.tool_handlers.tools_requests import buscar_curso_por_nome_ou_codigo

@mcp.tool(annotations={"domain": "disciplina"})
async def buscar_disciplina_curso(disciplina: Any, curso: Any, campus: Optional[Any] = "") -> list[dict]:
    """
    Busca informações sobre uma disciplina específica de um curso específico.

    Args:
        disciplina (Any): Pode ser o nome da disciplina ou o código numérico dela. 
        curso (Any): Pode ser o nome do curso por escrito ou o código numérico dele.
        campus (Optional[Any], optional): Pode ser o nome do campus ou o código numérico dele (opcional).
    
    Returns:
        list[dict]: Lista com uma única disciplina no formato:
                {
                    "codigo_da_disciplina": int,                 # Código da disciplina
                    "nome": str,                                 # Nome da disciplina
                    "carga_horaria_teorica_semanal": int,        # CH teórica semanal
                    "carga_horaria_pratica_semanal": int,        # CH prática semanal
                    "quantidade_de_creditos": int,               # Número de créditos
                    "horas_totais": int,                         # Carga horária total
                    "media_de_aprovacao": int,                   # Média necessária para aprovação
                    "carga_horaria_teorica_minima": int,         # CH teórica mínima
                    "carga_horaria_pratica_minima": int,         # CH prática mínima
                    "carga_horaria_teorica_maxima": int,         # CH teórica máxima
                    "carga_horaria_pratica_maxima": int,         # CH prática máxima
                    "numero_de_semanas": int,                    # Número de semanas da disciplina
                    "codigo_do_setor": int,                      # Código do setor responsável
                    "nome_do_setor": str,                        # Nome do setor responsável
                    "campus": int,                               # Código do campus
                    "nome_do_campus": str,                       # Nome do campus
                    "status": str,                               # Status da disciplina (ex.: ATIVO)
                    "contabiliza_creditos": str,                 # Indica se conta para créditos ("S" ou "N")
                    "tipo_de_componente_curricular": str,        # Tipo do componente (ex.: Atividade Complementar)
                    "carga_horaria_extensao": int                 # CH de extensão, se houver
                }
    """

    curso = str(curso)
    campus = str(campus)

    func_name, parametros_str = get_func_info()
    url_disciplina = f"{BASE_URL}/disciplinas"

    try:
        logging.info(f"🔍 Chamando {func_name}({parametros_str})")

        cursos_encontrados, params = await buscar_curso_por_nome_ou_codigo(curso, campus)

        if len(cursos_encontrados) > 1:
            raise ValueError(
                "Foram encontrados múltiplos cursos semelhantes ao informado. "
                "\nCursos encontrados:\n" +
                "\n".join([f"- {c['descricao']} (Código: {c['codigo_do_curso']})" for c in cursos_encontrados])
            )
        
        curso_escolhido = cursos_encontrados[0]
        params["curso"] = str(curso_escolhido["codigo_do_curso"])

        if str(disciplina).isdigit():
            params["disciplina"] = str(disciplina)
            data = await make_request(url_disciplina, params)
            if not data:
                raise ValueError("Nenhuma disciplina encontrada com esse código.")
            return data
        
        data = await make_request(url_disciplina, params)
        if not data:
            raise ValueError("Nenhuma disciplina encontrada com esse nome.")
        data = extract_most_similar(str(disciplina), data, "nome")
        return format_subject_results(data)
    
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