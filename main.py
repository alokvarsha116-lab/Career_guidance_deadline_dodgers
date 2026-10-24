from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import store

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals["careers_in_group"] = store.careers_in_group

def evaluate_career_path(
    grade: str,
    favorite_subjects: str,
    free_time_activity: str,
    learning_style: str,
    marks: str,
    tech_interest: str,
    flexibility_pref: str,
    work_lifestyle: str
):
    """Your exact 5-dimension evaluation logic translated into structured web response."""
    subs = favorite_subjects.lower()
    activity = free_time_activity.lower()
    style = learning_style.lower()
    flex = flexibility_pref.lower()
    life = work_lifestyle.lower()

    # Possibility 1: Humanities, Law, Public Policy & Civil Services
    if "history" in subs or "political" in subs or "law" in subs or "reading" in activity or "debate" in activity or "communication" in style:
        return {
            "career_title": "Corporate Lawyer / Public Policy Analyst / Civil Servant (IAS/IPS)",
            "stream": "Humanities / Arts or Commerce",
            "market_scope": "Steady, high-respect public and private sector demand, especially in legal advisory, governance, and policy formulation.",
            "flexibility_note": "High adaptability; legal and administrative training opens doors to corporate governance, diplomacy, media, and social enterprise.",
            "credentials": "Requires integrated law degrees (BA LLB) through entrance tests (CLAT) or civil service examinations (UPSC).",
            "lifestyle_note": "Requires extensive reading, argumentative writing, public speaking, and managing high-stakes administrative tasks.",
            "next_steps": [
                "Improve reading speed and vocabulary through newspapers, editorials, and literature.",
                "Join school debate clubs, Model United Nations (MUN), or public speaking workshops.",
                "Study the basics of how the legal system and government policies operate."
            ]
        }

    # Possibility 2: Technology, Computing, and AI Engineering
    elif "math" in subs or "computer" in subs or "coding" in activity or "hands-on" in style or "tech" in life:
        return {
            "career_title": "Software Engineer / AI & Data Developer",
            "stream": "Science (PCM - Physics, Chemistry, Mathematics)",
            "market_scope": "Extremely High demand, excellent starting salaries, and rapid global growth driven by artificial intelligence and software automation.",
            "flexibility_note": "Offers moderate flexibility; a PCM background allows you to pivot later into management, finance, or design.",
            "credentials": "Requires higher education degree (B.Tech/B.Sc in Computer Science or related fields) and strong self-taught project portfolios.",
            "lifestyle_note": "Involves continuous learning, coding sessions, and remote/office hybrid work environments with dynamic workloads.",
            "next_steps": [
                "Focus strongly on high school Mathematics and logical problem-solving.",
                "Learn Python or JavaScript through beginner tutorials and small personal projects.",
                "Explore how AI tools work under the hood."
            ]
        }

    # Possibility 3: Medical, Healthcare, and Life Sciences
    elif "biology" in subs or ("science" in subs and "computer" not in subs and "math" not in subs) or "hospital" in life or "health" in activity:
        return {
            "career_title": "Doctor / Healthcare Professional / Biomedical Researcher",
            "stream": "Science (PCB - Physics, Chemistry, Biology)",
            "market_scope": "Evergreen, recession-proof job demand with high societal impact and stable long-term career growth.",
            "flexibility_note": "Specialized track; locks you into the medical/life-sciences vertical early, requiring dedicated higher education.",
            "credentials": "Requires cracking competitive entrance exams (like NEET) and completing long-term medical degrees (MBBS).",
            "lifestyle_note": "High commitment, rigorous study hours, emotional resilience, and rewarding patient care or lab research environments.",
            "next_steps": [
                "Master fundamental concepts in Biology and Chemistry practicals.",
                "Read medical science journals and biographies of pioneering researchers.",
                "Build disciplined study schedules to prepare for competitive entrance requirements."
            ]
        }

    # Possibility 4: Commerce, Finance, and Business Management
    elif "economics" in subs or "business" in subs or "finance" in activity or "corporate" in life or "account" in subs:
        return {
            "career_title": "Business Manager / Startup Founder / Financial Analyst",
            "stream": "Commerce (with Mathematics or Business Studies)",
            "market_scope": "Strong industry demand across startups, multinational corporations, and financial institutions with robust earning potential.",
            "flexibility_note": "High interdisciplinary flexibility; combines well with technology, law, or public policy.",
            "credentials": "Requires commerce degrees (B.Com, BBA) or professional certifications (CA, CFA, MBA).",
            "lifestyle_note": "Dynamic, meeting-heavy, strategic, and leadership-oriented corporate or entrepreneurial work culture.",
            "next_steps": [
                "Read foundational books on basic economics, financial literacy, and corporate case studies.",
                "Participate in school business fests, quizzes, and leadership activities.",
                "Observe how modern businesses market their products and manage operating costs."
            ]
        }

    # Possibility 5: Arts, Design, and Creative Media (Fallback / Studio Track)
    else:
        return {
            "career_title": "Product Designer / UI/UX Specialist / Digital Content Creator",
            "stream": "Any Stream (Focus on building a creative portfolio)",
            "market_scope": "Growing digital economy demand for creative problem-solvers, designers, and multimedia communicators.",
            "flexibility_note": "Extremely flexible; creative skills apply across technology, entertainment, marketing, and entrepreneurship.",
            "credentials": "Portfolio-driven field supported by design degrees (B.Des) or specialized certification courses.",
            "lifestyle_note": "Independent, studio-based, or freelance flexibility with project-based collaborative workflows.",
            "next_steps": [
                "Experiment with digital sketching, UI/UX tools (like Figma), or storytelling.",
                "Build a personal portfolio showcasing creative projects or design concepts.",
                "Research design schools and digital media educational pathways."
            ]
        }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"categories": store.categories()})

@app.get("/category/{cat_id}", response_class=HTMLResponse)
def category(request: Request, cat_id: str):
    cat = store.get_category(cat_id)
    if not cat:
        raise HTTPException(404, "Category not found")
    return templates.TemplateResponse(request, "category.html", {"cat": cat})

@app.get("/career/{career_id}", response_class=HTMLResponse)
def career(request: Request, career_id: str):
    c = store.get_career(career_id)
    if not c:
        raise HTTPException(404, "Career not found")
    cats = [store.get_category(i) for i in c["category_ids"]]
    return templates.TemplateResponse(request, "career.html", {"career": c, "cats": cats})

# --- AI Chat Routes ---

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    """Renders the interactive AI Career Guidance Companion chat UI."""
    return templates.TemplateResponse(request, "chat.html", {})

@app.post("/chat/evaluate", response_class=HTMLResponse)
def chat_evaluate(
    request: Request,
    grade: str = Form(...),
    favorite_subjects: str = Form(...),
    free_time_activity: str = Form(...),
    learning_style: str = Form(...),
    marks: str = Form(...),
    tech_interest: str = Form("Yes"),
    flexibility_pref: str = Form("Flexible"),
    work_lifestyle: str = Form("High-intensity corporate/tech")
):
    evaluation = evaluate_career_path(
        grade=grade,
        favorite_subjects=favorite_subjects,
        free_time_activity=free_time_activity,
        learning_style=learning_style,
        marks=marks,
        tech_interest=tech_interest,
        flexibility_pref=flexibility_pref,
        work_lifestyle=work_lifestyle
    )
    return templates.TemplateResponse(
        request, 
        "chat_result_partial.html", 
        {
            "evaluation": evaluation,
            "inputs": {
                "grade": grade,
                "favorite_subjects": favorite_subjects,
                "free_time_activity": free_time_activity,
                "learning_style": learning_style,
                "marks": marks
            }
        }
    )
# Pass popular tags into the home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request, 
        "home.html", 
        {
            "categories": store.categories(),
            "popular_tags": store.get_popular_tags(14)
        }
    )

# Live search endpoint (HTMX partial response)
@app.get("/search", response_class=HTMLResponse)
def search_careers(request: Request, q: str = ""):
    query = q.strip()
    results = store.search_careers_by_tags(query) if query else []
    
    return templates.TemplateResponse(
        request,
        "search_results_partial.html",
        {
            "query": query,
            "results": results,
            "total_matches": len(results)
        }
    )