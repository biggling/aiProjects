from tools.shared.config import ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY

_anthropic_client = None
_openai_client = None
_gemini_client = None


def get_anthropic():
    """Return a singleton Anthropic client."""
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic
        _anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _anthropic_client


def get_openai():
    """Return a singleton OpenAI client."""
    global _openai_client
    if _openai_client is None:
        import openai
        _openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client


def get_gemini():
    """Return a singleton Google Gemini client (google-genai SDK)."""
    global _gemini_client
    if _gemini_client is None:
        from google import genai
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    return _gemini_client
