import sys
import os
import locale

# Configuração para Windows
if sys.platform.startswith('win'):
    # Força UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    
    # Define locale para UTF-8
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        except:
            pass

# Server FastMCP
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EurecaMCPServer")