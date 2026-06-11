import uuid
import json
import traceback
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from google import genai
from google.genai import types

# 1. Initialize Gemini Client (for turning words into numbers)
ai_client = genai.Client()

# 2. Initialize Qdrant Database (We use ":memory:" so it runs instantly without setup)
db_client = QdrantClient(":memory:")
COLLECTION_NAME = "resume_data"

# 3. Create the "Table" for our vectors
# Google's embedding model outputs exactly 768 numbers per word/sentence
db_client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)

def add_text_to_memory(text_chunk: str, metadata: dict):
    """Turns text into an embedding and saves it to Qdrant."""
    print(f"Memorizing: {text_chunk}")
    
    # Ask Gemini to turn the text into an Embedding (Math) compressed to 768
    response = ai_client.models.embed_content(
        model='gemini-embedding-2', 
        contents=text_chunk,
        config=types.EmbedContentConfig(output_dimensionality=768)
    )
    vector_math = response.embeddings[0].values

    # Save the math AND the original text into Qdrant
    point_id = str(uuid.uuid4())
    
    db_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=vector_math,
                payload={"text": text_chunk, **metadata} 
            )
        ]
    )
    print("Saved to long-term memory!")

def search_resume_memory(query: str, limit: int = 20) -> str:
    """
    Searches the vector database. Includes X-Ray error logging.
    """
    print(f"\n--- TOOL START ---")
    print(f"  -> AI is searching for: '{query}'")
    
    try:
        # 1. Turn the user's question into math
        response = ai_client.models.embed_content(
            model='gemini-embedding-2', 
            contents=query,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )
        query_vector = response.embeddings[0].values

        # 2. Search Qdrant (USING THE MODERN QUERY API)
        search_results = db_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector, # Note: Qdrant changed this parameter name to 'query'
            limit=limit
        ).points # We add .points here to get the list of matches!
        
        # 3. Extract the data
        found_memories = [hit.payload for hit in search_results]
            
        print(f"  -> Found {len(found_memories)} results in database!")
        print(f"  -> Sending Data to AI: {found_memories}")
        print(f"--- TOOL END ---\n")
        
        return json.dumps(found_memories)

    except Exception as e:
        # THE X-RAY: If anything breaks, print the exact error to the terminal!
        print(f"  -> [FATAL TOOL ERROR]: {str(e)}")
        traceback.print_exc() 
        return f"Error: {str(e)}"