# Eureca MCP Server

> Este é um servidor MCP (Model Context Protocol) que expõe ferramentas para acessar a API oficial do Eureca (UFCG), possibilitando que LLMs consultem e manipulem informações acadêmicas por meio de linguagem natural.

---
## Ferramentas Disponíveis

As ferramentas (tools) são funções chamadas que se comunicam com os endpoints fornecidos pela API do Eureca, retornando os resultados de forma estruturada. Elas estão organizadas por domínios, como **Curso**, **Disciplina**, **Estudante**, entre outros.

### Curso:

- *buscar_curso*
    - Trás informações gerais de um curso
        - `curso` (String): Código ou nome do curso
        - `campus` (String): Opcional, código ou nome do campus
- *buscar_todos_cursos_por_campus*
    - Trás informações gerais de todos os cursos filtrados ou não por campi
        - `campus` (String): Opcional, código ou nome do campus

---
## Instalação

Após clonar o repositório, estando no diretório base, é preciso instalar o gerenciador de pacotes `uv`:


**MacOS/Linux**
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Windows**
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Criar ambiente virtual e ativá-lo:

**MacOS/Linux**
```
uv venv
source .venv/bin/activate
```
**Windows**
```
uv venv
.venv\Scripts\activate
```
Por fim, instalar as dependências:
```
uv sync
```

---

## Server

Para iniciar o servidor MCP, abra um terminal no diretório base e execute o seguinte comando:

**Localmente (default: stdio transport)**
```
uv run -m src.main
```
**Remotamente (HTTP transport)**
```
uv run -m src.main --transport http
```
**Opções disponíveis de transporte:**
- `--transport stdio` (default): Comunicação sobre a entrada e saída padrão, para conexões locais.
- `--transport http`: Transporte HTTP para conexões remotas (default: 127.0.0.1:8000)
- `--host HOST`: Host ao qual o servidor será vinculado para o transporte HTTP (default: 127.0.0.1)
- `--port PORT`: Porta à qual o servidor será vinculado para o transporte HTTP (default: 8000)

**Observação**: [Acesse a documentação oficial](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) para mais informações sobre os métodos de transporte fornecidos pelo MCP.

## Client

Para algumas formas de acessar o servidor com um cliente, [veja esses exemplos]().

---
## Contribuição
Contribuições são bem-vindas! 
Siga os passos abaixo para colaborar: 
- Faça um fork do repositório;
- Modifique o que desejar e crie um pull request;
- Detalhe o pull request. Descreva suas alterações.
---

## Licença
Este projeto é licenciado sob a MIT - License