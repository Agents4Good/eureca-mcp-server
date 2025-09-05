import logging
from contextlib import AsyncExitStack

from typing import Optional, TypedDict, Literal

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client

class StdioConfig(TypedDict):
    """Connection configuration for stdio transport."""
    command: str
    args: list[str]
    transport: Literal["stdio"]

class StreamableHTTPConfig(TypedDict):
    """Connection configuration for Streamable HTTP transport."""
    url: str
    transport: Literal["streamable_http"]

TransportConfig = StdioConfig | StreamableHTTPConfig

class EurecaMCPClient():
    def __init__(self, config: dict[TransportConfig]):
        """
        Basic Client to acesss the Eureca MCP Server.

        Args:
            config: A dictionary representation of the eureca mcp server used to map to a transport configuration.
        
        Example (has to be in a async environment):

        ```python
        client = EurecaMCPClient(
            {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable_http"
            }
        )
        ```
        """

        self.session: Optional[ClientSession] = None
        self.config: dict[TransportConfig] = config
        self.exit_stack = AsyncExitStack()
        self._initialized = False
    
    async def create_session(self):
        """
        Connects to the Eureca MCP Server and creates a session.
        """

        if self.session is not None and self._initialized:
            return
        
        try:
            if self.config["transport"] == "stdio":
                stdio_params = StdioServerParameters(
                    command=self.config["command"],
                    args=self.config["args"],
                )
                stdio_client_context = stdio_client(stdio_params)
                read, write = await self.exit_stack.enter_async_context(stdio_client_context)
                self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            elif self.config["transport"] == "streamable_http":
                read, write, _ = await self.exit_stack.enter_async_context(streamablehttp_client(self.config["url"]))
                self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            else:
                raise ValueError("Transport must either be 'stdio' or 'streamable_http'")
            await self.session.initialize()
            self._initialized = True
        except Exception as e:
            await self.close()
            raise e

    async def list_tools(self):
        """
        Lists all tools from the server.
        """

        if self.session is None:
            await self.create_session()
        
        response = await self.session.list_tools()
        return response
    

    async def execute_tool(self, tool_name: str, args: dict = {}):
        """
        Calls a tool.
        """

        if self.session is None:
            await self.create_session()
        
        response = await self.session.call_tool(tool_name, args)
        return response
    
    async def close(self):
        """
        Closes server connection. Must always close it.
        """

        try:
            if self.exit_stack:
                await self.exit_stack.aclose()
        except Exception as e:
            logging.error(f"Error to close the session: {e}")
        finally:
            self.session = None
            self._initialized = False
            self.exit_stack = AsyncExitStack()