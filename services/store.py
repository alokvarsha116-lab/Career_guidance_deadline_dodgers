import json

DATA = json.load(open("data/careers.json", encoding="utf-8"))
CAREERS = {c["id"]: c for c in DATA["careers"]}
CATEGORIES = {c["id"]: c for c in DATA["categories"]}

def categories():
    return DATA["categories"]

def get_category(cid):
    return CATEGORIES.get(cid)

def get_career(cid):
    return CAREERS.get(cid)

def all_careers():
    return DATA["careers"]

def careers_in_group(group):
    return [CAREERS[i] for i in group["career_ids"]]
##
from collections import Counter
import re

def search_careers_by_tags(query: str):
    """
    Searches careers matching any tag, name, or keyword with relevance scoring.
    Returns sorted list of careers with matched tags highlighted.
    """
    if not query or not query.strip():
        return []

    # Clean and split query into individual search tokens
    tokens = [re.sub(r'[^a-zA-Z0-9-]', '', t.lower()) for t in query.replace(",", " ").split()]
    tokens = [t for t in tokens if t]

    if not tokens:
        return []

    all_careers = CAREERS.values() if isinstance(CAREERS, dict) else CAREERS
    results = []

    for c in all_careers:
        c_tags = [t.lower() for t in c.get("tags", [])]
        c_name = c.get("name", "").lower()
        
        score = 0
        matched_tags = []

        for token in tokens:
            # 1. Exact Tag Match (Highest weight)
            for tag in c_tags:
                if token == tag:
                    score += 20
                    matched_tags.append(tag)
                elif token in tag:  # Partial tag match (e.g., "code" in "coding")
                    score += 10
                    matched_tags.append(tag)

            # 2. Career Name Match
            if token == c_name:
                score += 25
            elif token in c_name:
                score += 15

        if score > 0:
            results.append({
                "career": c,
                "score": score,
                "matched_tags": list(set(matched_tags))
            })

    # Sort by highest relevance score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def get_popular_tags(limit: int = 12):
    """Returns the most common tags across all careers for quick-filter buttons."""
    allCAREERS = CAREERS.values() if isinstance(CAREERS, dict) else CAREERS
    tag_counter = Counter()
    
    # Exclude overly generic tags
    ignored = {"science", "technology", "engineering", "btech", "bsc"}
    
    for c in allCAREERS:
        for t in c.get("tags", []):
            t_clean = t.strip().lower()
            if t_clean not in ignored and len(t_clean) > 2:
                tag_counter[t_clean] += 1
                
    return [tag for tag, count in tag_counter.most_common(limit)]