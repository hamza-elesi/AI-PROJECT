# src/ai/utils/token_counter.py

class TokenCounter:
    """Manages token counting and limits"""
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def within_limits(self, text: str) -> bool:
        """Check if text is within token limits"""
        # Approximate token count (4 chars = 1 token)
        token_count = len(text) // 4
        return token_count <= self.max_tokens

    def get_token_count(self, text: str) -> int:
        """Get approximate token count"""
        return len(text) // 4