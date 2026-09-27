"""Interactive demo client to call initialize, tools/list, resources/list, and prompts/list."""

import json
import httpx

MCP_URL = "http://localhost:8000/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def parse_mcp_response(response: httpx.Response) -> dict:
    """Parse SSE / JSON response from MCP server."""
    text = response.text
    for line in text.splitlines():
        if line.startswith("data:"):
            data_str = line[len("data:") :].strip()
            return json.loads(data_str)
    try:
        return response.json()
    except Exception:
        return {"raw": text}


def main():
    print(f"Connecting to MCP Server at {MCP_URL}...\n")

    with httpx.Client(timeout=10.0) as client:
        # ==========================================
        # 1. INITIALIZE CALL
        # ==========================================
        print("=" * 60)
        print("1. CALLING 'initialize' API")
        print("=" * 60)
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "demo-client", "version": "1.0.0"},
            },
        }

        init_res = client.post(MCP_URL, json=init_payload, headers=HEADERS)
        session_id = init_res.headers.get("mcp-session-id")
        init_data = parse_mcp_response(init_res)

        print(f"Status Code : {init_res.status_code}")
        print(f"Session ID  : {session_id}")
        print("Server Info :", json.dumps(init_data.get("result", {}).get("serverInfo", {}), indent=2))

        # Send initialized notification
        session_headers = {**HEADERS, "mcp-session-id": session_id}
        client.post(
            MCP_URL,
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
            headers=session_headers,
        )

        # ==========================================
        # 2. TOOLS / LIST CALL
        # ==========================================
        print("\n" + "=" * 60)
        print("2. CALLING 'tools/list' API")
        print("=" * 60)
        tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }
        tools_res = client.post(MCP_URL, json=tools_payload, headers=session_headers)
        tools_data = parse_mcp_response(tools_res)
        tools_list = tools_data.get("result", {}).get("tools", [])

        print(f"Total Tools Found: {len(tools_list)}")
        for idx, tool in enumerate(tools_list, 1):
            print(f"  {idx:2d}. {tool['name']:<22} -> {tool['description']}")

        # ==========================================
        # 3. RESOURCES / LIST CALL
        # ==========================================
        print("\n" + "=" * 60)
        print("3. CALLING 'resources/list' API")
        print("=" * 60)
        res_payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {},
        }
        res_response = client.post(MCP_URL, json=res_payload, headers=session_headers)
        res_data = parse_mcp_response(res_response)
        resources_list = res_data.get("result", {}).get("resources", [])

        print(f"Total Resources Found: {len(resources_list)}")
        for idx, r in enumerate(resources_list, 1):
            print(f"  {idx:2d}. {r['uri']:<20} ({r.get('mimeType', 'unknown')}) -> {r['name']}")

        # ==========================================
        # 4. PROMPTS / LIST CALL
        # ==========================================
        print("\n" + "=" * 60)
        print("4. CALLING 'prompts/list' API")
        print("=" * 60)
        prompts_payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "prompts/list",
            "params": {},
        }
        prompts_res = client.post(MCP_URL, json=prompts_payload, headers=session_headers)
        prompts_data = parse_mcp_response(prompts_res)
        prompts_list = prompts_data.get("result", {}).get("prompts", [])

        print(f"Total Prompts Found: {len(prompts_list)}")
        for idx, p in enumerate(prompts_list, 1):
            args = ", ".join(a["name"] for a in p.get("arguments", []))
            print(f"  {idx:2d}. {p['name']:<20} (args: {args}) -> {p['description']}")

        # ==========================================
        # 5. BONUS: CALL A TOOL
        # ==========================================
        print("\n" + "=" * 60)
        print("5. BONUS: CALLING 'tools/call' (add_numbers)")
        print("=" * 60)
        call_payload = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "add_numbers",
                "arguments": {"a": 10, "b": 20},
            },
        }
        call_res = client.post(MCP_URL, json=call_payload, headers=session_headers)
        call_data = parse_mcp_response(call_res)
        print("Result of add_numbers(10, 20):", json.dumps(call_data.get("result", {}), indent=2))


if __name__ == "__main__":
    main()
