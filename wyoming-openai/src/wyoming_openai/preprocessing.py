"""Text preprocessing for TTS optimization."""

import re
import logging
from typing import Dict

_LOGGER = logging.getLogger(__name__)


def remove_emojis(text: str) -> str:
    """
    Remove emojis from text, adding period if emoji was before newline.
    
    Uses a comprehensive Unicode emoji pattern to detect and remove
    emoji characters that would sound awkward in TTS.
    
    If an emoji is found before a newline and there's no punctuation,
    a period is added to maintain proper sentence flow.
    
    Args:
        text: Input text possibly containing emojis
        
    Returns:
        Text with emojis removed and proper punctuation
    """
    # Comprehensive emoji pattern (Unicode ranges for emoji)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "]+",
        flags=re.UNICODE
    )
    
    # Two-pass approach:
    # 1. Handle emojis before newlines (add period if no punctuation before emoji)
    # 2. Remove all remaining emojis
    
    # Pass 1: Emoji + optional whitespace before newline, WITHOUT punctuation before emoji → add period
    # Lookahead (?=\n) matches position before newline without consuming it
    text = re.sub(
        r'(?<![.!?,;:])' + emoji_pattern.pattern + r'\s*(?=\n)',
        '.',
        text,
        flags=re.UNICODE
    )
    
    # Pass 2: Remove ALL remaining emojis (including those with punctuation, or not at line end)
    return emoji_pattern.sub('', text)


def remove_brackets_and_quotes(text: str) -> str:
    """
    Remove all types of brackets and quotation marks.
    
    Removes:
    - Parentheses: ( )
    - Square brackets: [ ]
    - Curly braces: { }
    - Angle brackets: < >
    - Double quotes: " " " "
    - Single quotes: ' ' ' '
    - Backticks: `
    - Guillemets: « »
    
    Args:
        text: Input text with brackets/quotes
        
    Returns:
        Text with brackets and quotes removed
    """
    # Remove all types of brackets (keep content)
    text = re.sub(r'[\(\)\[\]\{\}<>]', '', text)
    
    # Remove all types of quotation marks
    text = re.sub(r'["""\'\'\'`«»]', '', text)
    
    return text


def remove_markdown(text: str) -> str:
    """
    Remove common markdown formatting.
    
    Removes:
    - **bold** → bold
    - *italic* → italic
    - ~~strikethrough~~ → strikethrough
    - `code` → code
    - # headers → headers
    - [links](url) → links
    
    Args:
        text: Input text with markdown
        
    Returns:
        Plain text without markdown
    """
    # Remove bold/italic/strikethrough
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
    text = re.sub(r'~~([^~]+)~~', r'\1', text)      # ~~strikethrough~~
    text = re.sub(r'`([^`]+)`', r'\1', text)        # `code`
    
    # Remove headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove links [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    return text


def apply_custom_replacements(text: str, replacements: Dict[str, str]) -> str:
    """
    Apply custom text replacements.
    
    Useful for:
    - Fixing pronunciation: "API" → "A P I"
    - Removing unwanted markers: "~" → ""
    - Expanding abbreviations: "EUR" → "Euro"
    
    Args:
        text: Input text
        replacements: Dictionary of {old: new} replacements
        
    Returns:
        Text with replacements applied
    """
    if not replacements:
        return text
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def normalize_pauses(text: str) -> str:
    """
    Normalize pause markers for better TTS flow.
    
    - "..." → "," (shorter pause)
    - Multiple spaces → single space
    - Leading/trailing whitespace removed
    
    Args:
        text: Input text
        
    Returns:
        Text with normalized pauses
    """
    text = text.replace('...', ',')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def preprocess_for_tts(
    text: str,
    *,
    remove_emoji: bool = True,
    remove_md: bool = True,
    remove_brackets_quotes: bool = True,
    custom_replacements: Dict[str, str] | None = None,
    normalize_pause: bool = True
) -> str:
    """
    Complete text preprocessing pipeline for TTS.
    
    Args:
        text: Input text (possibly with emojis, markdown, etc.)
        remove_emoji: Remove emoji characters (and add period before newline if needed)
        remove_md: Remove markdown formatting
        remove_brackets_quotes: Remove all types of brackets and quotation marks
        custom_replacements: Custom string replacements
        normalize_pause: Normalize pause markers
        
    Returns:
        Cleaned text optimized for TTS
        
    Example:
        >>> preprocess_for_tts(
        ...     "**Hello** world! 🐍 Check API docs...",
        ...     custom_replacements={"API": "A P I"}
        ... )
        'Hello world. Check A P I docs,'
    """
    original_text = text
    
    if remove_emoji:
        text = remove_emojis(text)
    
    if remove_md:
        text = remove_markdown(text)
    
    if remove_brackets_quotes:
        text = remove_brackets_and_quotes(text)
    
    if custom_replacements:
        text = apply_custom_replacements(text, custom_replacements)
    
    if normalize_pause:
        text = normalize_pauses(text)
    
    # Log if significant changes were made
    if text != original_text:
        preview_len = 50
        _LOGGER.debug(
            "TTS preprocessing: %s → %s",
            original_text[:preview_len] + ('...' if len(original_text) > preview_len else ''),
            text[:preview_len] + ('...' if len(text) > preview_len else '')
        )
    
    return text


# Default replacements for common issues
DEFAULT_REPLACEMENTS = {
    # Pronunciation fixes
    "API": "A P I",
    "EUR": "Euro",
    "JPY": "Yen",
    "USD": "Dollar",
    "URL": "U R L",
    "PDF": "P D F",
    "CSV": "C S V",
    
    # File extensions
    ".md": " M D",
    ".txt": " T X T",
    ".json": " JSON",
    
    # Remove tilde (often used for cuteness)
    "~": "",
    
    # Common abbreviations
    "etc.": "et cetera",
    "e.g.": "for example",
    "i.e.": "that is",
}
