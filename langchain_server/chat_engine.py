from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import START, END
from inventory import InventoryManager
import asyncio


class ChatEngine:
    def __init__(self):
        self.inventory_manager = InventoryManager()
        self.tools = [self.get_product_list]  # Use instance method
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.conversations: Dict[str, List[HumanMessage]] = {}
        self.system_message = SystemMessage(
            content="""You are AIda, a friendly AI assistant managing our computer inventory system.
    First, ALWAYS get the product list using the get_product_list tool to ensure you have the latest information.
    Then, based on the user's question:

    1. For counting: Simply state the number of computers available
    2. For specific products: Provide details about that product only
    3. For comparisons: Compare the requested products focusing on their key differences
    4. For prices: State the exact price of the requested product(s)

    Keep responses concise and direct. Responde solely to the user's question in a single paragraph
    Ask if they want more information.
    AVOID any formatting, be conversational and write your answers without break points properly.
    Respond in the same language as the user's query (English or Spanish)

Remember:
- Keep responses concise and clear
- Use proper formatting with line breaks
- Maintain a helpful, professional tone
"""
        )
        self.graph = self._create_graph()

    def get_product_list(self) -> str:
        """Wrapper for async get_product_list"""
        return asyncio.run(self.inventory_manager.get_product_list())

    def _create_graph(self) -> StateGraph:
        """Create the LangChain graph for processing messages"""
        builder = StateGraph(MessagesState)

        def assistant(state: MessagesState):
            messages = [self.system_message] + state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}

        builder.add_node("assistant", assistant)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")
        builder.add_edge("assistant", END)

        return builder.compile()

    async def process_message(self, message: str, session_id: str = "default") -> str:
        """Process a message and return the response"""
        try:
            # Initialize conversation history if needed
            if session_id not in self.conversations:
                self.conversations[session_id] = []

            # Add new message to conversation
            self.conversations[session_id].append(HumanMessage(content=message))

            # Get response using conversation history
            result = self.graph.invoke(
                {
                    "messages": self.conversations[session_id][
                        -5:
                    ]  # Keep last 5 messages for context
                }
            )

            # Extract and store AI response
            ai_messages = [m for m in result["messages"] if isinstance(m, AIMessage)]
            if ai_messages:
                response = ai_messages[-1].content
                self.conversations[session_id].append(AIMessage(content=response))
                return response

            return "I'm sorry, I couldn't process that message."
        except Exception as e:
            print(f"Error processing message: {e}")
            return "I apologize, there was an error processing your message."
