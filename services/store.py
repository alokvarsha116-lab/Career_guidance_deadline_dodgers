import json
import re
from collections import Counter

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

def search_careers_by_tags(query: str):
    """
    Searches careers matching any tag, name, or keyword with relevance scoring.
    Returns sorted list of careers with matched tags highlighted.
    """
    if not query or not query.strip():
        return []

    tokens = [re.sub(r'[^a-zA-Z0-9-]', '', t.lower()) for t in query.replace(",", " ").split()]
    tokens = [t for t in tokens if t]

    if not tokens:
        return []

    results = []
    for c in CAREERS.values():
        c_tags = [t.lower() for t in c.get("tags", [])]
        c_name = c.get("name", "").lower()
        
        score = 0
        matched_tags = []

        for token in tokens:
            for tag in c_tags:
                if token == tag:
                    score += 20
                    matched_tags.append(tag)
                elif token in tag:
                    score += 10
                    matched_tags.append(tag)

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

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def get_popular_tags(limit: int = 12):
    """Returns the most common tags across all careers for quick-filter buttons."""
    tag_counter = Counter()
    ignored = {"science", "technology", "engineering", "btech", "bsc"}
    
    for c in CAREERS.values():
        for t in c.get("tags", []):
            t_clean = t.strip().lower()
            if t_clean not in ignored and len(t_clean) > 2:
                tag_counter[t_clean] += 1
                
    return [tag for tag, count in tag_counter.most_common(limit)]

# --- AI Career Guidance Evaluation ---

def evaluate_student_ai(
    grade: str,
    favorite_subjects: str,
    free_time_activity: str,
    learning_style: str,
    marks: str,
    tech_interest: str,
    flexibility_pref: str,
    work_lifestyle: str
):
    """
    Evaluates student inputs against all 300+ careers in careers.json
    and returns accurate stream advice, entrance exams, and top matched careers.
    """
    typed_text = f"{favorite_subjects} {free_time_activity}".lower()
    style_text = f"{learning_style} {work_lifestyle}".lower()

    # 1. Determine Recommended Stream based on typed subjects & passions
    if any(k in typed_text for k in ["law", "polity", "political", "history", "debate", "debating", "public policy", "civics", "literature", "writing"]):
        if any(k in typed_text for k in ["economics", "finance", "business", "commerce", "math"]):
            stream = "Commerce with Applied Mathematics OR Humanities with Economics & Legal Studies"
            exams = "CLAT (National Law Universities), CUET-UG, IPMAT (IIM 5-Year Management)"
            degrees = "5-Year Integrated BA LLB / BBA LLB, B.Com (Hons), or BA Economics"
        else:
            stream = "Humanities / Arts (Political Science, History, Legal Studies, English)"
            exams = "CLAT (Law), CUET-UG (Top Central Universities), UPSC Civil Services (later)"
            degrees = "BA LLB, BA in International Relations / Journalism / Public Administration"
    elif any(k in typed_text for k in ["economics", "finance", "business", "account", "accounts", "investing", "stock", "marketing", "management", "startup"]):
        stream = "Commerce (with Applied Mathematics or Business Studies)"
        exams = "IPMAT (IIMs), CUET-UG (Top Commerce Colleges like SRCC), CA Foundation"
        degrees = "B.Com (Hons), BBA, CA (ICAI), followed by MBA"
    elif any(k in typed_text for k in ["biology", "bio", "doctor", "health", "hospital", "medicine", "biotech", "zoology", "botany", "pharmacy"]):
        stream = "Science with Biology (PCB: Physics, Chemistry, Biology)"
        exams = "NEET-UG, CUET-UG (for Biotechnology & Research Universities)"
        degrees = "MBBS, BDS, B.Pharm, B.Sc Biotechnology / Biomedical Science"
    elif any(k in typed_text for k in ["math", "maths", "computer", "cs", "coding", "code", "ai", "robot", "robotics", "software", "physics", "electronics"]):
        stream = "Science with Maths (PCM: Physics, Chemistry, Mathematics)"
        exams = "JEE Main, JEE Advanced, BITSAT, State Engineering CETs"
        degrees = "B.Tech / B.E in CSE / Data Science / AI, or B.Sc Computing"
    elif any(k in typed_text for k in ["art", "design", "sketch", "drawing", "ui", "ux", "animation", "game", "film", "media"]):
        stream = "Any Stream (Humanities, Commerce, or Science) with Creative Portfolio"
        exams = "UCEED (IIT Bombay), NID DAT, NIFT, NATA (Architecture)"
        degrees = "B.Des (Bachelor of Design), B.Arch, B.Sc Animation / Game Design"
    else:
        stream = "Commerce or Humanities with Electives matching your interests"
        exams = "CUET-UG, State University Entrance Exams"
        degrees = "Undergraduate Honors degrees in your favorite disciplines"

    # 2. Score all real careers from your database (CAREERS)
    matched_careers = []
    search_tokens = [w.strip() for w in typed_text.replace(",", " ").split() if len(w.strip()) > 2]

    for career in CAREERS.values():
        c_tags = [t.lower() for t in career.get("tags", [])]
        c_name = career.get("name", "").lower()
        score = 0
        matching_tags = []

        # Strong priority for what the student typed
        for token in search_tokens:
            if token in c_name:
                score += 35
            for tag in c_tags:
                if token == tag:
                    score += 25
                    matching_tags.append(tag)
                elif token in tag:
                    score += 15
                    matching_tags.append(tag)

        # Style & lifestyle tie-breakers
        if "hands-on" in style_text and any(t in c_tags for t in ["engineering", "machines", "coding", "design"]):
            score += 8
        if "communication" in style_text and any(t in c_tags for t in ["law", "management", "media", "consulting", "policy"]):
            score += 10
        if "corporate" in style_text and any(t in c_tags for t in ["business", "finance", "management", "corporate", "law"]):
            score += 10

        if score > 0:
            matched_careers.append({
                "id": career["id"],
                "name": career["name"],
                "summary": career.get("summary", ""),
                "score": min(score, 99),
                "matched_tags": list(set(matching_tags))[:4]
            })

    # Sort and take top 4 careers from your database
    matched_careers.sort(key=lambda x: x["score"], reverse=True)
    top_careers = matched_careers[:4]

    # Grade-specific next steps
    is_junior = "9" in grade or "10" in grade
    if is_junior:
        next_steps = [
            f"Select **{stream.split('(')[0].strip()}** in Class 11.",
            f"Focus on building strong conceptual foundations in {favorite_subjects.title()}.",
            "Read weekly industry blogs and participate in school debate, business, or coding clubs."
        ]
    else:
        next_steps = [
            f"Target Key Entrance Tests: **{exams.split(',')[0]}**.",
            f"Prepare your timeline for Class 12 Boards and competitive exam mock tests.",
            "Explore universities offering degrees such as: " + degrees.split(',')[0]
        ]

    # Personalized reason
    why_text = f"Your interest in **{favorite_subjects.title()}** combined with your passion for **{free_time_activity.title()}** naturally aligns with analytical problem-solving, strategic thinking, and strong career versatility."

    return {
        "stream": stream,
        "exams": exams,
        "degrees": degrees,
        "top_careers": top_careers,
        "why_text": why_text,
        "next_steps": next_steps,
        "grade_level": grade,
        "marks_advice": f"With {marks.lower()} academic consistency, focus on understanding core logic rather than memorization."
    }