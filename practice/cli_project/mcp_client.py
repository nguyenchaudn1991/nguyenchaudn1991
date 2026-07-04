import sys
import json
import asyncio
from typing import Optional, Any
from contextlib import AsyncExitStack
from pydantic import AnyUrl
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(
        self,
        command: str,
        args: list[str],
        env: Optional[dict] = None,
    ):
        self._command = command
        self._args = args
        self._env = env
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(
            command=self._command,
            args=self._args,
            env=self._env,
        )
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        _stdio, _write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_stdio, _write)
        )
        await self._session.initialize()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized or cache not populated. Call connect_to_server first."
            )
        return self._session

    async def list_tools(self) -> list[types.Tool]:
        result = await self.session().list_tools()
        return result.tools

    async def call_tool(
        self, tool_name: str, tool_input: dict
    ) -> types.CallToolResult | None:
        return await self.session().call_tool(tool_name, tool_input)

    async def list_prompts(self) -> list[types.Prompt]:
        result = await self.session().list_prompts()
        return result.prompts

    async def get_prompt(self, prompt_name, args: dict[str, str]):
        result = await self.session().get_prompt(prompt_name, args)
        return result.messages

    async def read_resource(self, uri: str) -> Any:
        result = await self.session().read_resource(AnyUrl(uri))
        resource = result.contents[0]

        if isinstance(resource, types.TextResourceContents):
            if resource.mimeType == "application/json":
                return json.loads(resource.text)

            return resource.text

    async def cleanup(self):
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()


# For testing
async def main():
    async with MCPClient(
        # Python without UV: command='python', args=['mcp_server.py'].
        command="python",
        args=["mcp_server.py"],
    ) as client:
        session = client.session()

        # --- Tools ---
        tools = await client.list_tools()
        print(f"Server exposes {len(tools)} tool(s):")
        for t in tools:
            print(f"  - {t.name}: {t.description}")

        # --- Direct resources ---
        res = await session.list_resources()
        print(f"\nDirect resources ({len(res.resources)}):")
        for r in res.resources:
            print(f"  - {r.uri}  (mime: {r.mimeType})")

        # --- Resource templates ---
        tmpl = await session.list_resource_templates()
        print(f"\nResource templates ({len(tmpl.resourceTemplates)}):")
        for r in tmpl.resourceTemplates:
            print(f"  - {r.uriTemplate}")

        # --- Read a DIRECT resource via our read_resource() wrapper ---
        # application/json -> parsed into a Python list
        doc_ids = await client.read_resource("docs://documents")
        print("\nread_resource('docs://documents') ->")
        print(f"  type={type(doc_ids).__name__}  value={doc_ids}")

        # --- Read a TEMPLATED resource via our read_resource() wrapper ---
        # text/plain -> returned as a string
        doc = await client.read_resource("docs://documents/deposition.md")
        print("\nread_resource('docs://documents/deposition.md') ->")
        print(f"  type={type(doc).__name__}  value={doc}")

        # --- Prompts (3rd primitive) via our wrappers ---
        prompts = await client.list_prompts()
        print(f"\nPrompts ({len(prompts)}):")
        for p in prompts:
            print(f"  - {p.name}: {p.description}")

        # get_prompt returns a list of messages (a conversation) ready for Claude
        messages = await client.get_prompt("format", {"doc_id": "report.pdf"})
        print("\nget_prompt('format', doc_id='report.pdf') -> messages:")
        for m in messages:
            text = m.content.text if hasattr(m.content, "text") else m.content
            print(f"  [{m.role}] {text.strip()[:80]}...")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
