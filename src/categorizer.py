"""
Video categorization engine for intelligent content organization.
"""

from typing import Optional, Dict, Any, List
from fastmcp import Context
import re
from utils import get_default_categories


async def categorize_videos_impl(
    recategorize: bool = False,
    custom_rules: Optional[Dict[str, Any]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Implementation for auto-categorizing videos using intelligent analysis.
    
    Args:
        recategorize: Force re-categorization of existing videos
        custom_rules: User-defined categorization rules
        ctx: FastMCP context for logging
        
    Returns:
        Updated video list with categories and confidence scores
    """
    if ctx:
        await ctx.info("Starting video categorization...")
    
    # Get default categories
    categories = get_default_categories()
    
    # TODO: Implement real categorization logic in Task 1.3
    # For now, return mock categorization results
    mock_result = {
        "status": "stub_implementation",
        "recategorize": recategorize,
        "custom_rules": custom_rules,
        "categorized_count": 224,
        "categories": {
            "Education": {"count": 89, "confidence": 0.92},
            "Tech": {"count": 67, "confidence": 0.88},
            "Entertainment": {"count": 45, "confidence": 0.85},
            "Productivity": {"count": 32, "confidence": 0.91},
            "Conference": {"count": 14, "confidence": 0.96}
        },
        "rules_applied": get_categorization_rules()
    }
    
    if ctx:
        await ctx.info(f"Categorization completed (stub) - {mock_result['categorized_count']} videos")
    
    return mock_result


def get_categorization_rules() -> Dict[str, Dict[str, Any]]:
    """Get the built-in categorization rules.
    
    Returns:
        Dictionary of categorization rules by category
    """
    return {
        "Education": {
            "keywords": ["tutorial", "how to", "learn", "course", "lesson", "guide", "explained"],
            "channels": ["khan academy", "coursera", "udemy", "edx"],
            "weight": 1.0
        },
        "Tech": {
            "keywords": ["programming", "coding", "software", "tech", "development", "javascript", "python"],
            "channels": ["tech lead", "fireship", "traversy media", "the coding train"],
            "weight": 1.0
        },
        "Entertainment": {
            "keywords": ["funny", "comedy", "gaming", "vlog", "entertainment", "reaction"],
            "channels": ["pewdiepie", "markiplier", "jacksepticeye"],
            "weight": 0.8
        },
        "Productivity": {
            "keywords": ["productivity", "business", "entrepreneur", "success", "self improvement"],
            "channels": ["thomas frank", "matt d'avella"],
            "weight": 0.9
        },
        "Conference": {
            "keywords": ["conference", "talk", "presentation", "keynote", "summit"],
            "channels": ["google developers", "microsoft developer"],
            "weight": 1.2
        }
    }


def categorize_single_video(
    title: str,
    channel: str,
    description: str = "",
    duration_seconds: int = 0,
    custom_rules: Optional[Dict] = None
) -> Dict[str, Any]:
    """Categorize a single video based on its metadata.
    
    Args:
        title: Video title
        channel: Channel name
        description: Video description
        duration_seconds: Video duration in seconds
        custom_rules: User-defined categorization rules
        
    Returns:
        Categorization result with category and confidence score
    """
    rules = get_categorization_rules()
    if custom_rules:
        rules.update(custom_rules)
    
    scores = {}
    text_content = f"{title} {channel} {description}".lower()
    
    # Score each category
    for category, rule in rules.items():
        score = 0.0
        
        # Keyword matching
        for keyword in rule.get("keywords", []):
            if keyword.lower() in text_content:
                score += rule.get("weight", 1.0)
        
        # Channel matching
        for channel_pattern in rule.get("channels", []):
            if channel_pattern.lower() in channel.lower():
                score += rule.get("weight", 1.0) * 1.5  # Channel match is stronger
        
        # Duration-based scoring
        if category == "Short" and duration_seconds < 600:  # < 10 minutes
            score += 1.0
        elif category == "Long" and duration_seconds > 3600:  # > 1 hour
            score += 1.0
        
        scores[category] = score
    
    # Find best category
    if not scores or max(scores.values()) == 0:
        return {
            "category": "Uncategorized",
            "confidence": 0.0,
            "scores": scores
        }
    
    best_category = max(scores, key=scores.get)
    max_score = scores[best_category]
    confidence = min(max_score / 3.0, 1.0)  # Normalize to 0-1 range
    
    return {
        "category": best_category,
        "confidence": round(confidence, 2),
        "scores": scores
    }


def extract_keywords_from_title(title: str) -> List[str]:
    """Extract meaningful keywords from video title.
    
    Args:
        title: Video title
        
    Returns:
        List of extracted keywords
    """
    # Remove common words and extract meaningful terms
    common_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
        "of", "with", "by", "how", "what", "why", "when", "where", "is", "are"
    }
    
    # Clean and split title
    clean_title = re.sub(r'[^\w\s]', ' ', title.lower())
    words = clean_title.split()
    
    # Filter out common words and short words
    keywords = [
        word for word in words 
        if len(word) > 2 and word not in common_words
    ]
    
    return keywords[:10]  # Return top 10 keywords


class VideoCategorizer:
    """Advanced video categorization engine (for future enhancement)."""
    
    def __init__(self, custom_rules: Optional[Dict] = None):
        self.rules = get_categorization_rules()
        if custom_rules:
            self.rules.update(custom_rules)
    
    def add_rule(self, category: str, keywords: List[str], weight: float = 1.0):
        """Add a custom categorization rule."""
        if category not in self.rules:
            self.rules[category] = {"keywords": [], "channels": [], "weight": weight}
        
        self.rules[category]["keywords"].extend(keywords)
        self.rules[category]["weight"] = weight
    
    def categorize_batch(self, videos: List[Dict]) -> List[Dict]:
        """Categorize multiple videos efficiently."""
        results = []
        for video in videos:
            result = categorize_single_video(
                title=video.get("title", ""),
                channel=video.get("channel", ""),
                description=video.get("description", ""),
                duration_seconds=video.get("duration", 0),
                custom_rules=self.rules
            )
            results.append({**video, **result})
        
        return results 