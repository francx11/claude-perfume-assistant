"""
Script de prueba para Día 4: PerfumeTools + Function Calling con Claude
"""
import os
from dotenv import load_dotenv
from src.api.claude_client import ClaudeClient
from src.data.loader import DataLoader
from src.tools.perfume_tools import PerfumeTools

load_dotenv()

loader = DataLoader("data/raw/fragrantica.csv")
tools = PerfumeTools(data_loader=loader)
client = ClaudeClient(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 1. Probar tools directamente
print("=== Prueba directa de tools ===\n")

resultados = tools.search_perfumes(season="spring-summer", gender="feminine")
print(f"search_perfumes(season=spring-summer, gender=feminine): {len(resultados)} resultados")
for p in resultados:
    print(f"  - {p['name']}")

print()
detalle = tools.get_perfume_details("dior-sauvage")
print(f"get_perfume_details(dior-sauvage): {detalle.get('name')} - {detalle.get('brand')}")

print()
similar = tools.recommend_similar("dior-sauvage")
print(f"recommend_similar sin RAG: {similar}")

# 2. Probar execute_tool (dispatcher)
print("\n=== Prueba execute_tool ===\n")
resultado = tools.execute_tool("search_perfumes", {"brand": "Dior"})
print(f"execute_tool search_perfumes brand=Dior: {[p['name'] for p in resultado]}")

resultado = tools.execute_tool("tool_inexistente", {})
print(f"execute_tool inexistente: {resultado}")

# 3. Probar function calling con Claude
print("\n=== Prueba Function Calling con Claude ===\n")

messages = [{"role": "user", "content": "Busca perfumes frescos para el verano"}]
tools_definitions = tools.get_tools_definitions()

response = client.send_message(messages, tools=tools_definitions)

print(f"stop_reason: {response['stop_reason']}")

# Si Claude quiere usar una tool
if response["stop_reason"] == "tool_use":
    tool_use_block = next(b for b in response["content"] if b["type"] == "tool_use")
    print(f"Claude quiere usar: {tool_use_block['name']}")
    print(f"Con parámetros: {tool_use_block['input']}")

    # Ejecutar la tool
    tool_result = tools.execute_tool(tool_use_block["name"], tool_use_block["input"])
    print(f"Resultado: {len(tool_result)} perfumes encontrados")

    # Enviar resultado a Claude
    messages.append({"role": "assistant", "content": response["content"]})
    messages.append(client.create_tool_result(tool_use_block["id"], tool_result))

    final_response = client.send_message(messages, tools=tools_definitions)
    print(f"\nRespuesta final de Claude:\n{final_response['content'][0]['text']}")
else:
    print(f"Claude respondió directamente:\n{response['content'][0]['text']}")
