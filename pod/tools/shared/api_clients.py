from tools.shared.config import ANTHROPIC_API_KEY, OPENAI_API_KEY

_anthropic_client = None
_openai_client = None


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
