import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("waha")

# Predefined contacts mapping
registered_contacts: dict[str, str] = {
    "Rafaello": "+556292930437",
    "Lucas": "+556291324281",
    "Tallyta": "+556492956187"
}

# Resource: list all registered contacts
@mcp.resource(
    uri="contacts://list",
    name="Lista de Contatos",
    description="Mapeamento de nomes para números internacionais (+<código-país><DDD><número>)",
    mime_type="application/json",
)
async def contacts_catalog() -> dict[str, str]:
    """Return all registered contacts as JSON mapping."""
    return registered_contacts

# WAHA API configuration
WAHA_API_URL = "http://localhost:3000/api/sendText"
WAHA_SESSION = "default"

@mcp.tool()
async def send_message(phone_number: str, message: str) -> str:
    """
    Send a WhatsApp message via the WAHA server.
    Args:
        phone_number: The recipient's phone number in international format (e.g., '+5511999999999').
        message: The text message to send.
    Returns:
        A status string indicating success or error details.
    """
    if not phone_number.startswith("+"):
        return f"Error: Phone number {phone_number} must start with '+'."
    chat_id = f"{phone_number[1:]}@c.us"
    payload = {"chatId": chat_id, "text": message, "session": WAHA_SESSION}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(WAHA_API_URL, json=payload, headers=headers, timeout=30.0)
            resp.raise_for_status()
            return f"Message sent to {phone_number}. Response: {resp.json()}"
    except httpx.HTTPError as e:
        err_msg = str(e)
        if e.response is not None:
            err_msg += f" Response: {e.response.text}"
        return f"Error sending message: {err_msg}"

if __name__ == "__main__":
    # Run the MCP server over stdio
    mcp.run(transport="stdio") 