# MCP Client

> Para usar o Eureca MCP Server, é preciso de um Client. Abaixo estão **algumas** formas de utilizá-lo.

---
## Eureca MCP Client

Há uma classe e exemplo de uso do Eureca MCP Client. Este é um Client desenvolvido em Python para acessar as tools fornecidas pelo Eureca MCP Server e executá-las.

Para executar, certifique-se de estar no diretório base e rode o comando:

```
python .\client\client.py
```

---
## Claude for Desktop

Para usar o Eureca MCP Server com o Claude Desktop é preciso configurar um arquivo fornecido, abaixo estão os passos.

**Configurar**
1. Abra o Claude Desktop
2. Navegue para: `Configurações → Desenvolvedor → Editar Config`
3. Atualize o arquivo `claude_desktop_config.json`

Para mais informações [acesse a documentação oficial](https://modelcontextprotocol.io/quickstart/user).

**Para uso local (stdio transport)**:

**Windows**
```
{
  "mcpServers": {
    "eureca-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        ""C:\\CAMINHO\\ABSOLUTO\\PARA\\DIRETORIO\\BASE\\eureca-mcp-server",
        "run",
        "-m",
        "src.main"
      ]
    }
  }
}
```

**MacOS**
```
{
  "mcpServers": {
    "eureca-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/CAMINHO/ABSOLUTO/PARA/DIRETORIO/BASE/eureca-mcp-server",
        "run",
        "-m",
        "src.main"
      ]
    }
  }
}
```