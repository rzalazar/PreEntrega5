import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, BaseMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from tools import tools

load_dotenv()

# Instanciar LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = SystemMessage(
    content=(
        "Eres un agente técnico de atención al cliente con capacidad de razonamiento cíclico.\n"
        "REGLAS:\n"
        "1. Para responder preguntas sobre montos o ítems de clientes, PRIMERO debes buscar la lista de pedidos del cliente, "
        "y LUEGO consultar el detalle específico de cada pedido relevante.\n"
        "2. Responde de manera clara, precisa y profesional basándote ÚNICAMENTE en la información devuelta por tus herramientas.\n"
        "3. Recuerda el contexto previo si el usuario hace preguntas de seguimiento."
    )
)

async def call_model(state: MessagesState) -> Dict[str, List[BaseMessage]]:
    """Nodo principal del agente que procesa el historial y decide la siguiente acción."""
    messages = state["messages"]
    if not any(isinstance(msg, SystemMessage) for msg in messages):
        messages = [SYSTEM_PROMPT] + messages
        
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}


def build_graph() -> StateGraph:
    """Construye el StateGraph sin compilar (para vincular el checkpointer asíncrono en main)."""
    builder = StateGraph(MessagesState)

    # Nodos
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode(tools))

    # Aristas
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder