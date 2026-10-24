from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import store

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
    """Renders the AI Guidance Companion page."""
    return templates.TemplateResponse(request, "chat.html", {})

@app.api_route("/chat/evaluate", methods=["GET", "POST"], response_class=HTMLResponse)
async def chat_evaluate(request: Request):
    """Evaluates student interests, strengths, and lifestyle against all careers."""
    if request.method == "POST":
        try:
            form = await request.form()
            grade = form.get("grade", "10th")
            favorite_subjects = form.get("favorite_subjects", "")
            free_time_activity = form.get("free_time_activity", "")
            learning_style = form.get("learning_style", "Hands-on problem solving")
            marks = form.get("marks", "Average")
            tech_interest = form.get("tech_interest", "Yes")
            flexibility_pref = form.get("flexibility_pref", "Flexible")
            work_lifestyle = form.get("work_lifestyle", "High-intensity corporate/tech")
        except Exception:
            params = request.query_params
            grade = params.get("grade", "10th")
            favorite_subjects = params.get("favorite_subjects", "")
            free_time_activity = params.get("free_time_activity", "")
            learning_style = params.get("learning_style", "Hands-on problem solving")
            marks = params.get("marks", "Average")
            tech_interest = params.get("tech_interest", "Yes")
            flexibility_pref = params.get("flexibility_pref", "Flexible")
            work_lifestyle = params.get("work_lifestyle", "High-intensity corporate/tech")
    else:
        params = request.query_params
        grade = params.get("grade", "10th")
        favorite_subjects = params.get("favorite_subjects", "")
        free_time_activity = params.get("free_time_activity", "")
        learning_style = params.get("learning_style", "Hands-on problem solving")
        marks = params.get("marks", "Average")
        tech_interest = params.get("tech_interest", "Yes")
        flexibility_pref = params.get("flexibility_pref", "Flexible")
        work_lifestyle = params.get("work_lifestyle", "High-intensity corporate/tech")

    # Call the smart evaluation engine in services/store.py
    evaluation = store.evaluate_student_ai(
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