import phoenix as px
from llama_index.core import set_global_handler

def init_phoenix():
    """ 
    Starts the local Arize Phoenix dashboard 
    and hooks LlamaIndex into its tracing system.
    """
    # Launch the Phoenix server (typically runs on http://localhost:6006)
    session = px.launch_app()
    
    # Enable LlamaIndex OpenInference Tracing globally
    set_global_handler("arize_phoenix")
    
    return session.url
