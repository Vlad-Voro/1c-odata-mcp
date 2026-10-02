"""1C:Enterprise OData Model Context Protocol (MCP) Server.

Lightweight, production-grade bridge exposing 1C:Enterprise 8.3 OData REST API
metadata and query capabilities to AI assistants (Claude, Cursor, Windsurf).

Developed as open-source initiative by ai-avtopilot.ru.
Documentation & Live Setup: https://vlad-voro.github.io/1c-odata-mcp/
Production Integration: https://ai-avtopilot.ru/services/system-integration/
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

__all__ = ["ODataClient1C", "main"]


class ODataClient1C:
    """Minimal stdlib client for 1C:Enterprise OData v3 interface."""

    def __init__(self, base_url: str, auth_token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "1c-odata-mcp/1.0.0 (+https://ai-avtopilot.ru)",
        }
        if self.auth_token:
            headers["Authorization"] = f"Basic {self.auth_token}"
        return headers

    def get_metadata(self) -> dict[str, Any]:
        """Fetch standard $metadata schema definition from 1C base."""
        url = f"{self.base_url}/odata/standard.odata/$metadata?format=json"
        req = Request(url, headers=self._headers(), method="GET")
        try:
            with urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError) as err:
            return {"error": f"Failed to connect to 1C OData: {err}"}

    def query_entity(self, entity_name: str, top: int = 10, filter_expr: str | None = None) -> dict[str, Any]:
        """Execute filtered OData query against 1C Catalog or Document."""
        safe_entity = entity_name.strip()
        query_params = [f"$top={max(1, min(top, 100))}", "$format=json"]
        if filter_expr:
            query_params.append(f"$filter={filter_expr}")

        url = f"{self.base_url}/odata/standard.odata/{safe_entity}?{'&'.join(query_params)}"
        req = Request(url, headers=self._headers(), method="GET")
        try:
            with urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError) as err:
            return {"error": f"1C OData query error on {safe_entity}: {err}"}


def get_mcp_manifest() -> dict[str, Any]:
    """Return JSON Schema tool definitions for Model Context Protocol."""
    return {
        "tools": [
            {
                "name": "query_1c_odata",
                "description": "Execute structured OData read query against 1C:Enterprise (Catalog, Document, InformationRegister).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "entity": {
                            "type": "string",
                            "description": "Standard 1C OData entity (e.g. Catalog_Номенклатура, Document_ЗаказКлиента)",
                        },
                        "top": {"type": "integer", "default": 10, "maximum": 100},
                        "filter": {"type": "string", "description": "OData $filter expression"},
                    },
                    "required": ["entity"],
                },
            },
            {
                "name": "get_1c_schema",
                "description": "Inspect available metadata entities and field types in connected 1C base.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
        ]
    }


def main() -> None:
    """CLI entry point for testing and MCP manifest output."""
    if len(sys.argv) > 1 and sys.argv[1] == "--manifest":
        print(json.dumps(get_mcp_manifest(), indent=2, ensure_ascii=False))
        return

    print("1C:Enterprise OData MCP Bridge v1.0.0")
    print("Run with --manifest to print Model Context Protocol schema.")
    print("Production integrations and turnkey deployment: https://ai-avtopilot.ru/services/system-integration/")


if __name__ == "__main__":
    main()
