# summarization_project/views.py

import os
import nest_asyncio
import logging
import tempfile

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# nest_asyncio.apply()

# Set your Groq API key (ideally, keep this in environment variables or Django settings)
GROQ_API_KEY = "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"  # Replace with your Groq API key
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Import modules from LlamaIndex, Groq, and Hugging Face embeddings
from llama_index.core import SimpleDirectoryReader, SummaryIndex
from llama_index.llms.groq import Groq
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def home(request):
    """A simple home view."""
    return HttpResponse("Welcome to the Summarization Project!")

@csrf_exempt
def summarize_view(request):
    """
    Single endpoint that handles both text-only and file-based summarization.
    
    - If no files are uploaded: Summarize the provided text.
    - If files are uploaded: Use SimpleDirectoryReader to load documents from the files,
      and treat the text as an extra instruction in the prompt.
    """
    if request.method == "POST":
        try:
            # Retrieve user instruction (text)
            message_text = request.POST.get("message", "")
            # Retrieve uploaded files (if any)
            uploaded_files = request.FILES.getlist("files")

            # Initialize the Groq Llama-3 model and Hugging Face embeddings.
            llm = Groq(model="llama-3.1-8b-instant")
            Settings.llm = llm
            Settings.embed_model = HuggingFaceEmbedding()

            # ---------------------------
            # CASE 1: Files are uploaded.
            # ---------------------------
            if uploaded_files:
                # Save each uploaded file temporarily and collect file paths.
                file_paths = []
                for f in uploaded_files:
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    for chunk in f.chunks():
                        tmp.write(chunk)
                    tmp.close()
                    file_paths.append(tmp.name)

                # Load documents from the temporary file paths.
                documents = SimpleDirectoryReader(input_files=file_paths).load_data()

                # Clean up temporary files.
                for path in file_paths:
                    if os.path.exists(path):
                        os.remove(path)

                # Split the loaded documents into nodes.
                splitter = SentenceSplitter(chunk_size=16384)
                nodes = splitter.get_nodes_from_documents(documents)

                # Build the SummaryIndex and query engine.
                summary_index = SummaryIndex(nodes)
                summary_query_engine = summary_index.as_query_engine(
                    response_mode="tree_summarize",
                    use_async=True,
                )

                # Create a prompt that includes the user instruction along with file content.
                prompt = f"""Please summarize the content of the provided document(s) as if it were a test paper.
User Instruction: {message_text}

Summary Template:
Essay Title:
Author:
Author's Salient Points (quote up to the top 5 quotes and describe them):
Author's Weak Points (quote up to the bottom 5 quotes and describe them):
Points for Improvement:
Score out of 10 (?/10):
"""
                summary = summary_query_engine.query(prompt)

            # ------------------------------
            # CASE 2: No file is uploaded.
            # ------------------------------
            else:
                # Instead of creating a Document, we use the provided text directly as the node.
                nodes = [message_text]
                summary_index = SummaryIndex(nodes)
                summary_query_engine = summary_index.as_query_engine(
                    response_mode="tree_summarize",
                    use_async=True,
                )

                prompt = f"""Please summarize the following text as if it were a test paper:

{message_text}

Essay Title:
Author:
Author's Salient Points (quote up to the top 5 quotes and describe them):
Author's Weak Points (quote up to the bottom 5 quotes and describe them):
Points for Improvement:
Score out of 10 (?/10):
"""
                summary = summary_query_engine.query(prompt)

            return HttpResponse(summary)

        except Exception as e:
            logging.exception("Error during summarization:")
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return HttpResponse("Method not allowed", status=405)
