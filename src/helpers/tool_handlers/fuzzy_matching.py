import unicodedata
from rapidfuzz import process

def normalize_txt(txt):
    return "".join(
        c for c in unicodedata.normalize("NFD", txt.lower())
        if unicodedata.category(c) != "Mn"
    )

def format_course_results(matches: list[tuple[dict, float]]) -> list[dict]:
    """
    Formata os resultados da busca de cursos.
    
    - Se houver mais de um candidato, retorna lista resumida com apenas código, descrição, turno, modalidade e similaridade.
    - Se houver apenas um candidato, retorna lista com o curso completo (sem incluir a similaridade).

    Args:
        matches (list[tuple[dict, float]]): Lista de tuplas contendo (curso_dict, score_de_similaridade).

    Returns:
        list[dict]: Lista formatada conforme regra descrita acima.
    """

    if not matches:
        return []
    
    if len(matches) > 1:
        return [
            {
                "codigo_do_curso": c["codigo_do_curso"],
                "descricao": c["descricao"],
                "turno": c.get("turno"),
                "modalidade_academica": c.get("modalidade_academica"),
                "similaridade": score
            }
            for c, score in matches
        ]
    curso, _ = matches[0]
    return [curso]

def extract_most_similar(
        query_text: str,
        items: list[dict],
        field: str,
        tie_break_threshold: float = 2.0,
        top_k: int = 5
) -> list[tuple[dict, float]]:
    """
    Retorna os itens mais semelhantes a um texto de consulta com base em comparação aproximada de strings (fuzzy matching).

    Args:
        query_text (str): Texto de entrada a ser comparado.
        items (list[dict]): Lista de objetos (dicionários) a serem buscados.
        field (str): Nome do atributo (chave do dicionário) usado para comparação.
        tie_break_threshold (float, optional): Diferença máxima de score em relação ao melhor resultado para considerar empate.
        top_k (int, optional): Número máximo de candidatos a retornar antes da aplicação do critério de desempate.
    
    Returns:
        list[tuple[dict, float]]: Lista de tuplas contendo:
            - O objeto original (dict) correspondente
            - O score de similaridade (float)
    """

    query = normalize_txt(query_text)
    list_norm = [normalize_txt(obj[field]) for obj in items]
    
    matches = process.extract(query, list_norm, limit=top_k)

    if not matches:
        return []
    
    best_score = matches[0][1]
    possibles = [m for m in matches if best_score - m[1] <= tie_break_threshold]

    results = [(items[idx], score) for _, score, idx in possibles]

    return results