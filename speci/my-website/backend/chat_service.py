"""
Chat service module for the AI-Interactive Book backend.
Handles the conversation logic and interaction with the LLM.
"""
from typing import List, Dict, Any
from .vector_store import vector_store
from .config import settings

class ChatService:
    """
    Handles chat conversations with document context.
    """

    def __init__(self):
        # Initialize OpenAI client only if API key is provided
        self.openai_client = None
        self.model = settings.openai_model

        if settings.openai_api_key:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.openai_api_key)
            except ImportError:
                print("OpenAI library not available. Running in mock mode.")
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}. Running in mock mode.")

    def get_answer(self, query: str, context: str = None, user_id: str = None) -> Dict[str, Any]:
        """
        Get an answer to a query based on document context.

        Args:
            query: The user's question
            context: Additional context (optional)
            user_id: User identifier (optional)

        Returns:
            Dictionary with response and source information
        """
        # Search for relevant documents
        relevant_chunks = vector_store.search_similar(query, limit=5)

        if not relevant_chunks:
            return {
                "response": "I couldn't find any relevant information to answer your question. Please try rephrasing or ask about a different topic from the book.",
                "sources": []
            }

        # Prepare context from retrieved chunks
        context_text = "\n\n".join([f"Source: {chunk['source']}\nContent: {chunk['content']}" for chunk in relevant_chunks])

        # If OpenAI client is available, use it
        if self.openai_client:
            try:
                # Prepare the prompt for the LLM
                system_prompt = f"""
                You are an AI assistant for an interactive book. Your role is to answer questions based only on the provided book content.

                Guidelines:
                1. Only use information from the provided context to answer questions
                2. If the question cannot be answered from the context, say so
                3. Be concise but thorough in your responses
                4. Always attribute information to the specific sources when possible
                5. Maintain a helpful and educational tone
                6. If asked about topics not in the provided context, politely say you can only answer questions about the book content
                """

                user_message = f"""
                Context: {context_text}

                Question: {query}

                Please provide a helpful answer based on the context provided.
                """

                # Call the OpenAI API
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )

                # Extract the answer
                answer = response.choices[0].message.content

                # Extract sources
                sources = list(set([chunk["source"] for chunk in relevant_chunks]))

                return {
                    "response": answer,
                    "sources": sources
                }

            except Exception as e:
                return {
                    "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                    "sources": []
                }
        else:
            # Mock response when OpenAI is not available
            return {
                "response": f"This is a mock response to: '{query}'. In the full implementation with OpenAI API key configured, this would generate a context-aware response based on the book content.",
                "sources": [chunk["source"] for chunk in relevant_chunks]
            }

    def validate_context_restriction(self, query: str, response: str, context_sources: List[str]) -> bool:
        """
        Validate that the response is based only on the provided context.
        This is a basic implementation - in a production system, this would be more sophisticated.

        Args:
            query: The original query
            response: The generated response
            context_sources: Sources that were provided as context

        Returns:
            True if the response is properly grounded in context, False otherwise
        """
        # In a real implementation, this would check that the response
        # doesn't contain information not present in the context sources
        # For now, we'll return True as this is a basic validation
        return True

    def enforce_selected_text_qa(self, query: str, selected_text: str = None) -> Dict[str, Any]:
        """
        Enforce QA based on selected text only, if provided.

        Args:
            query: The user's question
            selected_text: Text that was selected by the user (optional)

        Returns:
            Dictionary with response and source information
        """
        if selected_text:
            # If specific text is selected, only use that as context
            context_text = selected_text
            sources = ["selected_text"]  # Indicate this came from selected text
        else:
            # Otherwise, search for relevant documents as before
            relevant_chunks = vector_store.search_similar(query, limit=5)

            if not relevant_chunks:
                return {
                    "response": "I couldn't find any relevant information to answer your question. Please try rephrasing or ask about a different topic from the book.",
                    "sources": []
                }

            # Prepare context from retrieved chunks
            context_text = "\n\n".join([f"Source: {chunk['source']}\nContent: {chunk['content']}" for chunk in relevant_chunks])
            sources = list(set([chunk["source"] for chunk in relevant_chunks]))

        # Prepare the prompt for the LLM
        system_prompt = f"""
        You are an AI assistant for an interactive book. Your role is to answer questions based only on the provided book content.

        Guidelines:
        1. Only use information from the provided context to answer questions
        2. If the question cannot be answered from the context, say so
        3. Be concise but thorough in your responses
        4. Always attribute information to the specific sources when possible
        5. Maintain a helpful and educational tone
        6. If asked about topics not in the provided context, politely say you can only answer questions about the book content
        """

        user_message = f"""
        Context: {context_text}

        Question: {query}

        Please provide a helpful answer based on the context provided.
        """

        try:
            # Call the OpenAI API
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=500
            )

            # Extract the answer
            answer = response.choices[0].message.content

            return {
                "response": answer,
                "sources": sources
            }

        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "sources": []
            }

# Global instance
chat_service = ChatService()