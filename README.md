# 1C:Enterprise OData MCP Bridge (Model Context Protocol)

[![GitHub Pages](https://img.shields.io/badge/Docs-GitHub%20Pages-blue.svg)](https://vlad-voro.github.io/1c-odata-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Open-source Model Context Protocol (MCP) server for connecting AI agents (Claude, Cursor, Windsurf, Roo Code) to **1C:Enterprise 8.3** (1C:ERP, 1C:УНФ, 1C:УТ, 1C:Комплексная Автоматизация) via standard OData REST interface.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+ (Standard Library, zero external dependencies)
- 1C:Enterprise 8.3.14+ with published OData standard interface (`/odata/standard.odata/`)

### 2. Inspect MCP Manifest
```bash
python mcp_server.py --manifest
```

### 3. Claude Desktop / Cursor MCP Configuration
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "1c-odata": {
      "command": "python",
      "args": ["/path/to/1c-odata-mcp/mcp_server.py"],
      "env": {
        "ONEC_ODATA_URL": "http://1c-server/base",
        "ONEC_AUTH_BASE64": "dXNlcjpwYXNzd29yZA=="
      }
    }
  }
}
```

---

## 📖 Documentation & Enterprise Production Support

- **Interactive Documentation**: [https://vlad-voro.github.io/1c-odata-mcp/](https://vlad-voro.github.io/1c-odata-mcp/)
- **Turnkey Enterprise Deployment**: For production on-premise AI-agent deployments, high-load Event Bus streaming, and 152-FZ compliance audits, explore [Интеграция ИИ-агентов в 1С от АвтоПилот](https://ai-avtopilot.ru/services/system-integration/).

## 📄 License
MIT License. Maintained by open-source community contributors.
