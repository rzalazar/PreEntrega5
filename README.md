# Agente de Razonamiento Cíclico con Memoria Persistente (LangGraph + SQLite)

Proyecto desarrollado para la Pre-entrega 5 del curso de AI Engineering en Coderhouse. Implementa un agente autónomo bajo la arquitectura ReAct que utiliza razonamiento multi-paso, persistencia de estado mediante hilos (`thread_id`) y SQLite asíncrono.

## 🛠️ Características del Agente

1. **Autonomía y Ciclo ReAct**: El agente utiliza `tools_condition` para decidir de forma dinámica cuándo invocar herramientas o responder al usuario, sin bifurcaciones rígidas `if/else`.
2. **Razonamiento Multi-paso**: Para responder preguntas compuestas, realiza llamadas secuenciales a múltiples herramientas (`buscar_pedidos_cliente` -> `obtener_detalle_pedido`).
3. **Persistencia de Estado**: Utiliza `AsyncSqliteSaver` guardando la traza en `state_checkpoints.db`. Al usar el mismo `thread_id`, recuerda el contexto de conversaciones pasadas.
4. **Resiliencia**: Configuración de `recursion_limit: 10` para prevenir bucles infinitos.

## 🚀 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd cyclic-agent-memory