import re

def clean_text(text: str) -> str:
    """
    Cleans extracted text based on notebook logic.
    - Strips leading/trailing whitespace.
    - Condenses multiple newlines into a single newline.
    - Condenses multiple spaces into a single space.
    """
    if not text:
        return ""
    
    # Condense multiple newlines into a single newline
    text = re.sub(r'\n{2,}', '\n', text)
    
    # Condense multiple spaces into a single space
    text = re.sub(r' +', ' ', text)
    
    # Split by newline, strip each line, and drop empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    return "\n".join(lines)
