from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse ,PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import store, ai_counselor

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
templates.env.globals["careers_in_group"] = store.careers_in_group

# Safe fallback for category images
if hasattr(store, "get_category_image"):
    templates.env.globals["get_category_image"] = store.get_category_image


# --- Home & Catalog Routes ---

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    popular = store.get_popular_tags(14) if hasattr(store, "get_popular_tags") else []
    return templates.TemplateResponse(
        request, 
        "home.html", 
        {
            "categories": store.categories(),
            "popular_tags": popular
        }
    )

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
    cats = [store.get_category(i) for i in c["category_ids"] if store.get_category(i)]
    related = store.get_related_careers(career_id, limit=3) if hasattr(store, "get_related_careers") else []
    return templates.TemplateResponse(request, "career.html", {"career": c, "cats": cats, "related_careers": related})


# --- Live Tag & Keyword Search ---

@app.get("/search", response_class=HTMLResponse)
def search_careers(request: Request, q: str = ""):
    query = q.strip()
    if not query:
        return templates.TemplateResponse(
            request,
            "search_results_partial.html",
            {
                "query": "",
                "results": [],
                "total_matches": 0,
                "categories": store.categories()
            }
        )
    
    results = store.search_careers_by_tags(query) if hasattr(store, "search_careers_by_tags") else []
    return templates.TemplateResponse(
        request,
        "search_results_partial.html",
        {
            "query": query,
            "results": results,
            "total_matches": len(results),
            "categories": []
        }
    )


# --- AI Career Chat (Connected to your real 300+ careers database) ---

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    """Renders the Dual-Model AI Guidance Companion page."""
    return templates.TemplateResponse(request, "chat.html", {})


@app.api_route("/chat/evaluate", methods=["GET", "POST"], response_class=HTMLResponse)
async def chat_evaluate(request: Request):
    """
    Evaluates comprehensive 10-dimensional student inputs using the
    Dual-Model Self-Correction AI Architecture (Generator Agent + Senior Critic Agent).
    """
    if request.method == "POST":
        try:
            form = await request.form()
            grade = form.get("grade", "10th")
            academic_consistency = form.get("academic_consistency", "Average")
            favorite_subjects = form.get("favorite_subjects", "")
            disliked_subjects = form.get("disliked_subjects", "")
            free_time_passions = form.get("free_time_passions", form.get("free_time_activity", ""))
            cognitive_style = form.get("cognitive_style", form.get("learning_style", "Hands-on problem solver"))
            budget_tier = form.get("budget_tier", "Moderate (₹5L - ₹15L)")
            work_lifestyle = form.get("work_lifestyle", "High-growth tech / startup")
            future_tech_attitude = form.get("future_tech_attitude", "Eager to learn coding & AI tools")
            geography_ambition = form.get("geography_ambition", "Major Tech Hubs")
        except Exception:
            params = request.query_params
            grade = params.get("grade", "10th")
            academic_consistency = params.get("academic_consistency", "Average")
            favorite_subjects = params.get("favorite_subjects", "")
            disliked_subjects = params.get("disliked_subjects", "")
            free_time_passions = params.get("free_time_passions", "")
            cognitive_style = params.get("cognitive_style", "Hands-on problem solver")
            budget_tier = params.get("budget_tier", "Moderate (₹5L - ₹15L)")
            work_lifestyle = params.get("work_lifestyle", "High-growth tech / startup")
            future_tech_attitude = params.get("future_tech_attitude", "Eager to learn coding & AI tools")
            geography_ambition = params.get("geography_ambition", "Major Tech Hubs")
    else:
        params = request.query_params
        grade = params.get("grade", "10th")
        academic_consistency = params.get("academic_consistency", "Average")
        favorite_subjects = params.get("favorite_subjects", "")
        disliked_subjects = params.get("disliked_subjects", "")
        free_time_passions = params.get("free_time_passions", "")
        cognitive_style = params.get("cognitive_style", "Hands-on problem solver")
        budget_tier = params.get("budget_tier", "Moderate (₹5L - ₹15L)")
        work_lifestyle = params.get("work_lifestyle", "High-growth tech / startup")
        future_tech_attitude = params.get("future_tech_attitude", "Eager to learn coding & AI tools")
        geography_ambition = params.get("geography_ambition", "Major Tech Hubs")

    profile = {
        "grade": grade,
        "academic_consistency": academic_consistency,
        "favorite_subjects": favorite_subjects,
        "disliked_subjects": disliked_subjects,
        "free_time_passions": free_time_passions,
        "cognitive_style": cognitive_style,
        "budget_tier": budget_tier,
        "work_lifestyle": work_lifestyle,
        "future_tech_attitude": future_tech_attitude,
        "geography_ambition": geography_ambition
    }

    # Run the Dual-Model AI Engine
    evaluation = ai_counselor.evaluate_student_comprehensive(profile)

    return templates.TemplateResponse(
        request, 
        "chat_result_partial.html", 
        {
            "evaluation": evaluation,
            "inputs": profile
        }
    )


@app.post("/chat/message", response_class=HTMLResponse)
async def chat_message(request: Request):
    """
    Handles live interactive follow-up questions to the Dual-Model AI Counselor.
    """
    form = await request.form()
    user_query = form.get("message", "").strip()
    if not user_query:
        return HTMLResponse("<div class='text-xs text-rose-500 py-2'>Please type a question.</div>")

    result = ai_counselor.answer_followup_question(user_query)
    return templates.TemplateResponse(
        request,
        "chat_message_partial.html",
        {
            "query": user_query,
            "answer": result["answer"],
            "critic_audit": result.get("critic_audit", "")
        }
    )