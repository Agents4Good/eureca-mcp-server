from typing import Any, Optional

from ...data.campi import campi
from ...data.config import BASE_URL

from ...helpers.request_utils import make_request
from ...helpers.tool_handlers.fuzzy_matching import extract_most_similar, format_course_results

async def buscar_curso_por_nome_ou_codigo(curso: Any, campus: Any) -> tuple[list[dict], dict]:
    """
    Busca cursos da UFCG por nome ou código, com base no campus especificado.

    - Se o curso for um número, é tratado como código direto.
    - Se for nome, será aplicada correspondência aproximada via `extract_most_similar`.
    - Caso mais de um curso seja semelhante, será retornada uma lista resumida com os candidatos.
    - Caso haja apenas um curso, os dados completos desse curso são retornados.

    Args:
        curso (Any): Nome ou código do curso a ser buscado.
        campus (Any): Código numérico ou nome do campus.

    Returns:
        tuple[list[dict], dict]: 
            - Lista de cursos (completa ou resumida).
            - Parâmetros usados na requisição à API.
    """

    curso = str(curso)
    campus = str(campus)

    url = f"{BASE_URL}/cursos"

    params = {
        "status": "ATIVOS",
        "campus": campus if (campus.isdigit() or campus == "") else extract_most_similar(campus, campi, "campus")[0][0]['codigo']
    }

    if curso.isdigit():
        params["curso"] = curso
        data = await make_request(url, params)
        if not data:
            raise ValueError("Nenhum curso encontrado com esse código.")
        return data, params

    data = await make_request(url, params)
    if not data:
        raise ValueError("Nenhum curso encontrado com esse nome.")
    matches = extract_most_similar(curso, data, "descricao")
    return format_course_results(matches), params