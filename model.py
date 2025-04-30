import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from data_loader import DataLoader
from hybdrid_search import HybridRetriever
from langchain_core.prompts import PromptTemplate
from prompt import template

# Load environment variables from .env file
load_dotenv()

# This class defines the complete Question-Answering system
class QASystem:
    def __init__(self, docs_path: str):
        self.docs_path = docs_path
        # Initialize the Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        # Build the document retriever using hybrid search
        self.retriever = self._init_retriever()
        # Initialize chat history with a system prompt
        self.history = [
            {"role": "system", "content": "You are a helpful assistant for internal company document Q&A."}
        ]

    # Load and chunk documents, then initialize the hybrid retriever
    def _init_retriever(self):
        print("[INFO] Loading and chunking documents...")
        text_chunks = DataLoader(self.docs_path).chunk_docs()
        print("[INFO] Creating hybrid retriever...")
        return HybridRetriever(text_chunks).create_hybrid_search()
    
    # Format the prompt using retrieved context and question
    def _format_prompt(self, context: str, question: str) -> str:
        prompt = PromptTemplate.from_template(template).format_prompt(
            context=context,
            user_question=question
        )
        return prompt.to_string()

    # Main method to ask a question and receive an answer
    def ask(self, question: str) -> str:
        # Retrieve relevant document chunks as context
        context = self.retriever.invoke(question)
        # Format the full prompt using context and question
        formatted_prompt = self._format_prompt(context, question)
        # Update conversation history with user's question
        self.history.append({"role": "user", "content": formatted_prompt})
        print("[INFO] Sending request to OpenAI...")
        # Call Azure OpenAI to generate the answer
        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.0,
            messages=[
                {"role": "system", "content": formatted_prompt},
                {"role": "user", "content": question},
            ]
        )
        # Extract the assistant's response
        answer = response.choices[0].message.content
        # Add answer to conversation history
        self.history.append({"role": "assistant", "content": answer})
        return answer
