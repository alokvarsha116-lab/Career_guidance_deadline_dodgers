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
    c = CAREERS.get(cid)
    if not c:
        return None
    return enrich_career_details(dict(c))

def all_careers():
    return DATA["careers"]

def enrich_career_details(c: dict) -> dict:
    """
    Enriches career data with comprehensive details:
    - Specialized Job Roles
    - Career Growth Ladder
    - Typical Day & Work Dynamics
    - Beginner Projects, Learn Platforms, Hackathons
    - Top Recruiters & Future Outlook
    - Degree Costs & ROI Timeline
    - Stream Pathways (Class 10 / Class 12 / College)
    """
    c_id = c.get("id", "").lower()
    c_tags = [t.lower() for t in c.get("tags", [])]
    c_cat_ids = c.get("category_ids", [])
    c_group_ids = c.get("group_ids", [])

    is_ai_data = (
        "ai-data-emerging-tech" in c_cat_ids
        or any(x in c_id for x in ["ai-", "machine-learning", "deep-learning", "data-scientist", "data-engineer", "data-analyst", "nlp", "computer-vision", "prompt-engineer"])
        or any(t in c_tags for t in ["artificial intelligence", "machine learning", "deep learning", "nlp", "computer vision", "generative ai", "data science"])
    )

    is_software = (
        not is_ai_data and (
            "science-engineering-tech--computing-and-it" in c_group_ids
            or any(x in c_id for x in ["computer-science", "software", "developer", "web-", "frontend", "backend", "full-stack", "cloud", "devops", "systems-architect", "qa-", "site-reliability", "network-engineer", "database-"])
            or any(t in c_tags for t in ["coding", "software", "computer science", "cse", "it", "web", "frontend", "backend", "full-stack", "devops", "cloud", "cybersecurity", "blockchain", "programming"])
        )
    )

    is_law = (
        "law-legal-public-policy" in c_cat_ids
        or any(x in c_id for x in ["law", "legal", "advocate", "attorney", "judge", "mediator", "arbitrator", "paralegal"])
        or any(t in c_tags for t in ["law", "legal", "clat", "llb", "justice"])
    )

    is_medical = (
        "medical-healthcare" in c_cat_ids
        or any(x in c_id for x in ["doctor", "surgeon", "physician", "nurse", "therapist", "dentist", "pharmacist", "radiologist", "pathologist", "oncologist", "cardiologist", "neurologist", "pediatrician", "paramedic"])
        or any(t in c_tags for t in ["medicine", "mbbs", "doctor", "neet", "healthcare", "allied health", "paramedical"])
    )

    is_finance = (
        "commerce-finance-accounting" in c_cat_ids
        or any(x in c_id for x in ["accountant", "ca", "cma", "auditor", "banker", "trader", "financial", "equity", "hedge-fund", "treasury", "actuary", "underwriter"])
        or any(t in c_tags for t in ["accounting", "ca", "cma", "cs", "finance", "banking", "investment", "audit", "tax", "stock market", "trading"])
    )

    is_business = (
        "business-management-entrepreneurship" in c_cat_ids
        or "startups-vc-private-equity" in c_cat_ids
        or any(x in c_id for x in ["manager", "consultant", "founder", "entrepreneur", "ceo", "coo", "cfo", "product-manager", "project-manager", "business-analyst"])
        or any(t in c_tags for t in ["management", "business", "entrepreneurship", "mba", "leadership", "consulting", "startup"])
    )

    is_design = (
        "arts-design-creative" in c_cat_ids
        or any(x in c_id for x in ["design", "artist", "illustrator", "animator", "architect"])
        or any(t in c_tags for t in ["design", "art", "creative", "nid", "nift", "uceed", "ui", "ux", "fashion", "animation"])
    )

    # 1. AI & Data Block
    if is_ai_data:
        c["job_roles"] = ["Data Analyst", "Machine Learning Engineer", "Data Scientist", "AI Research Scientist", "NLP Engineer", "Computer Vision Specialist", "Business Intelligence Developer", "MLOps Engineer"]
        c["career_ladder"] = ["Data Analyst / Junior ML Engineer (0–2 yrs)", "Machine Learning Engineer (2–4 yrs)", "Senior Data Scientist (4–7 yrs)", "Staff ML Engineer / Research Scientist (7–10 yrs)", "Principal AI Scientist / Head of AI (10+ yrs)", "Chief AI Officer (CAIO)"]
        c["typical_day"] = "Exploratory data analysis (EDA) in Jupyter notebooks, model training and evaluation, deploying models to production APIs, attending cross-functional meetings with product teams, writing documentation and ML papers."
        c["work_dynamics"] = "Predominantly remote-friendly. Heavy laptop/screen work. Creative and research-oriented — more self-directed compared to standard engineering. Fast-paced in product companies, research-paced in academia."
        c["beginner_projects"] = ["Train an image classifier using Teachable Machine (no code!)", "Predict house prices using linear regression on Kaggle", "Build a movie recommendation system", "Analyze IPL data with Python pandas", "Create a chatbot using basic NLP rules"]
        c["learn_platforms"] = ["Kaggle (competitions + datasets)", "fast.ai (free practical deep learning)", "DeepLearning.AI (Andrew Ng — Coursera)", "Google ML Crash Course (free)", "Hugging Face (transformers & NLP)", "NPTEL AI courses (IIT professors, free)"]
        c["hackathons"] = ["Kaggle Competitions", "Google AI Impact Challenge", "Smart India Hackathon (AI track)", "Zindi (African AI competitions)", "HackerEarth ML Challenges"]
        c["company_types"] = ["Big Tech AI Labs (Google DeepMind, Microsoft Research, OpenAI)", "Indian Tech Giants (TCS Research, Infosys AI Lab)", "AI-first Startups (Sarvam AI, Krutrim, Observe.AI)", "HealthTech & FinTech AI divisions", "Government (DRDO, ISRO AI research units)"]
        c["future_outlook"] = "The #1 fastest-growing career globally. Generative AI has created entirely new sub-fields: prompt engineering, RLHF, AI safety, and multimodal AI. Demand is outpacing supply by 10x. Expected to remain the highest-paying tech specialization through 2035."
        c["degree_costs"] = [
            {"tier": "IIT / IISc / IISER (Government)", "cost": "₹8L – ₹15L (Total)", "note": "World-class research labs. Best for AI research careers."},
            {"tier": "Private Engineering Colleges", "cost": "₹15L – ₹25L (Total)", "note": "Quality varies; check placement statistics carefully."},
            {"tier": "Online PGP / Bootcamp Route", "cost": "₹1L – ₹3L (Total)", "note": "Portfolio + Kaggle rankings often matter more than degree for industry roles."},
        ]
        c["roi_timeline"] = "At ₹12–18 LPA starting salary for ML roles, college investment recovered within 10–14 months at IIT, and 18–24 months at private colleges."
        if not c.get("summary"):
            c["summary"] = f"Design and implement intelligent algorithms, machine learning models, and data-driven systems as a {c.get('name')}."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 with Physics, Chemistry, Maths (PCM)", "B.Tech in CSE / AI & Data Science (or B.Sc Statistics/CS, followed by M.Tech/MS)"]
        if not c.get("exams"):
            c["exams"] = ["JEE Main & Advanced", "BITSAT", "GATE (Computer Science / Data Science)", "CUET-PG"]
        if not c.get("skills"):
            c["skills"] = ["Python & PyTorch/TensorFlow", "Statistics & Probability", "Linear Algebra", "Data Wrangling & SQL"]

    # 2. Software & IT Block
    elif is_software:
        c["job_roles"] = ["Frontend Developer", "Backend Engineer", "Full-Stack Developer", "DevOps Engineer", "Site Reliability Engineer", "Cloud Architect", "QA Engineer"]
        c["career_ladder"] = ["Intern / Trainee Developer", "Junior Software Engineer (0–2 yrs)", "Software Engineer (2–5 yrs)", "Senior Software Engineer (5–8 yrs)", "Tech Lead / Staff Engineer (8–12 yrs)", "Engineering Manager / Principal Engineer (12+ yrs)", "CTO / VP Engineering"]
        c["typical_day"] = "Morning standup meeting (15 min), coding features or fixing bugs (3–4 hrs), code review for teammates, system design discussions, writing unit tests, and deploying updates."
        c["work_dynamics"] = "High remote/hybrid flexibility. Screen time: 8–10 hrs/day. Generally low physical stress but high cognitive load. Most companies offer flexible hours."
        c["beginner_projects"] = ["Build a personal portfolio website (HTML/CSS/JS)", "Create a To-Do List app in Python", "Build a weather app using a free API", "Make a simple budget tracker in Excel/Python", "Clone a webpage (Amazon/Google homepage)"]
        c["learn_platforms"] = ["freeCodeCamp (free)", "LeetCode (DSA practice)", "GitHub (host your code)", "The Odin Project (free full-stack)", "Coursera / NPTEL (certificates)", "HackerRank (beginner challenges)"]
        c["hackathons"] = ["Smart India Hackathon (SIH)", "MLH Local Hack Day", "Google Summer of Code", "GitHub Campus Program", "Microsoft Imagine Cup"]
        c["company_types"] = ["Product Companies (Google, Microsoft, Amazon, Flipkart)", "Indian IT Services (TCS, Infosys, Wipro, HCL)", "High-Growth Startups (Razorpay, Zepto, CRED)", "Fintech (PhonePe, Paytm, Groww)", "Cybersecurity Firms, EdTech, HealthTech"]
        c["future_outlook"] = "Extremely strong. AI is augmenting (not replacing) software engineers — demand for engineers who can work with AI tools (GitHub Copilot, LLMs) is accelerating. Cloud, cybersecurity, and data engineering roles are growing 35%+ annually globally."
        c["degree_costs"] = [
            {"tier": "IIT / NIT (Government)", "cost": "₹8L – ₹12L (Total)", "note": "Highest ROI. Subsidized tuition + top placements."},
            {"tier": "Private Universities (VIT, SRM, BITS)", "cost": "₹12L – ₹22L (Total)", "note": "Good placement records in top private colleges."},
            {"tier": "BCA / B.Sc CS Route", "cost": "₹2L – ₹6L (Total)", "note": "Low cost, portfolio + skills matter more than brand."},
        ]
        c["roi_timeline"] = "At ₹8–12 LPA starting salary, a student typically recovers their full college investment within 12–18 months of starting their first job."
        if not c.get("summary"):
            c["summary"] = f"Design, develop, test, and maintain modern technological systems and applications as a {c.get('name')}."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 with PCM (Physics, Chemistry, Maths)", "B.Tech / B.E in CSE / IT or BCA followed by MCA"]
        if not c.get("exams"):
            c["exams"] = ["JEE Main", "BITSAT", "State Engineering CETs (MHT-CET, WBJEE, KCET)", "GATE"]
        if not c.get("skills"):
            c["skills"] = ["Data Structures & Algorithms", "Git & GitHub Version Control", "System Architecture & APIs", "Problem Solving"]

    # 3. Law Block
    elif is_law:
        c["job_roles"] = ["Litigation Lawyer", "Corporate Counsel", "Public Prosecutor", "Legal Advisor", "Compliance Officer", "IP Attorney", "Arbitrator", "Public Policy Analyst", "Legal Researcher"]
        c["career_ladder"] = ["Law Intern / Junior Associate (0–2 yrs)", "Associate Lawyer (2–5 yrs)", "Senior Associate (5–8 yrs)", "Partner / Senior Advocate (8–15 yrs)", "Managing Partner / Judge / Legal Director (15+ yrs)"]
        c["typical_day"] = "Reviewing contracts and case files, researching case law and precedents, drafting legal briefs or client memos, attending court hearings or client meetings, and staying updated on new legislation."
        c["work_dynamics"] = "Primarily office and courtroom work. Long hours especially around deadlines and hearings. High intellectual demand — reading and writing-intensive. Litigation is high-pressure; corporate law is structured but deadline-heavy."
        c["beginner_projects"] = ["Read one Supreme Court judgment per week and write a 1-page summary", "Follow Parliament sessions and analyze a new bill's implications", "Participate in school or college Moot Court competitions", "Write a legal opinion on a real news event (e.g., data privacy)", "Shadow a local district court advocate for a week"]
        c["learn_platforms"] = ["Indian Kanoon (free legal database)", "SCC Online / Manupatra (legal research)", "Coursera Law courses (Yale, Duke)", "Bar & Bench (legal news)", "NLSIU free lectures on YouTube", "PRS Legislative Research (Indian policy)"]
        c["hackathons"] = ["National Moot Court Competitions (NLIU, NALSAR, NLSIU)", "Model United Nations (MUN)", "Inter-school Debate Championships", "Essay competitions by Bar Council of India", "ADR (Alternative Dispute Resolution) competitions"]
        c["company_types"] = ["Top Law Firms (AZB, Cyril Amarchand, Trilegal, Shardul Amarchand)", "Big 4 Legal (PwC Law, EY Law)", "In-house Corporate Legal Departments (Reliance, Tata, HDFC)", "Government Prosecution (Central / State)", "International Law Organizations (UN, ICC, ICJ)"]
        c["future_outlook"] = "Strong and stable. Growing specializations include Data Privacy Law (DPDP Act 2023), Cybersecurity Compliance, AI Ethics & Regulation, ESG Law, and International Trade Law. Corporate law firms are expanding aggressively due to India's startup and FDI boom."
        c["degree_costs"] = [
            {"tier": "NLUs — National Law Universities (Govt.)", "cost": "₹7L – ₹12L (5-year total)", "note": "Highest ROI. CLAT rank-based admission."},
            {"tier": "Private Law Schools (Symbiosis, Christ, UPES)", "cost": "₹12L – ₹22L (5-year total)", "note": "Good placement for top private law schools."},
            {"tier": "State University Law Colleges (3-year LLB)", "cost": "₹50K – ₹2L (Total)", "note": "Very affordable. Combined with a strong undergrad degree for better prospects."},
        ]
        c["roi_timeline"] = "Starting salaries at top NLUs average ₹10–18 LPA. Investment recovery within 12–18 months. Corporate law partners earn ₹1Cr+ annually."
        if not c.get("summary"):
            c["summary"] = f"Provide expert legal representation, counsel, and regulatory interpretation as a {c.get('name')}."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 in any stream (Commerce, Humanities, or Science)", "5-Year Integrated BA LLB / BBA LLB or 3-Year LLB post graduation"]
        if not c.get("exams"):
            c["exams"] = ["CLAT (National Law Universities)", "AILET (NLU Delhi)", "SLAT (Symbiosis)", "State Law CETs"]
        if not c.get("skills"):
            c["skills"] = ["Legal Research & Drafting", "Critical Thinking & Analysis", "Courtroom Advocacy", "Negotiation & Dispute Resolution"]

    # 4. Medical / Doctors Block
    elif is_medical:
        c["job_roles"] = ["General Physician / Family Doctor", "Surgeon (General / Cardio / Neuro)", "Medical Researcher / Clinical Researcher", "Radiologist", "Psychiatrist", "Emergency Medicine Specialist", "Anesthesiologist", "Pediatrician"]
        c["career_ladder"] = ["MBBS Intern (1 year post-MBBS)", "Junior Resident / House Officer (1–3 yrs)", "Senior Resident (MD/MS in progress)", "Specialist Consultant (post MD/MS)", "Senior Consultant / Dept. Head (8–15 yrs)", "Director of Medical Services / Medical Superintendent"]
        c["typical_day"] = "Hospital morning ward rounds (checking on admitted patients), outpatient consultations (OPD), scheduled surgeries or procedures, reviewing test reports and prescribing treatment, attending case conferences with medical team."
        c["work_dynamics"] = "High-intensity physical and emotional work. Long shifts (12–24 hrs in hospitals during residency). Very high job satisfaction and societal impact. Work-life balance is challenging early in career, improves significantly after specialization."
        c["beginner_projects"] = ["Understand how one organ system works (e.g., Cardiovascular) — draw and explain it", "Volunteer at a local hospital or health camp", "Read 'Being Mortal' by Atul Gawande to understand healthcare realities", "Study a real disease outbreak (e.g., COVID-19) from an epidemiological angle", "Shadow a doctor at a primary health centre for a day"]
        c["learn_platforms"] = ["NCERT Biology (Class 11-12 — foundation)", "Khan Academy Medicine (free)", "TeachMeAnatomy.com (free 3D anatomy)", "Osmosis (YouTube — medical concepts)", "AMBOSS (for advanced students)", "NEET Prep: Aakash, Allen, Physics Wallah"]
        c["hackathons"] = ["National Science Olympiad (NSO)", "CBSE Science Exhibition", "SIH Healthcare Track (Smart India Hackathon)", "Medical case discussion competitions at AIIMS/PGI", "Public health essay competitions (WHO India)"]
        c["company_types"] = ["Government Hospitals (AIIMS, PGI, NIMHANS, District Hospitals)", "Corporate Hospitals (Apollo, Fortis, Manipal, Max Healthcare)", "Research Institutes (ICMR, DBT, WHO India)", "Pharmaceutical Industry (Clinical Trials)", "International Positions (MSF Doctors Without Borders, WHO)"]
        c["future_outlook"] = "Perennially strong. India is severely understaffed — 1 doctor per 2,000 patients (WHO recommends 1 per 1,000). Telemedicine, AI diagnostic tools, and precision medicine are creating new hybrid roles. Global Indian doctor diaspora is highly valued internationally."
        c["degree_costs"] = [
            {"tier": "Government Medical Colleges (AIIMS / State MBBS)", "cost": "₹50K – ₹5L (Total MBBS)", "note": "Life-changing ROI. NEET rank-based. Highly subsidized."},
            {"tier": "Private Deemed Medical Colleges", "cost": "₹60L – ₹1.5Cr (Total MBBS)", "note": "High cost — evaluate carefully. Check MCI recognition and NEET cutoff."},
            {"tier": "BAMS / BHMS / BPT (Allied Medical)", "cost": "₹3L – ₹12L (Total)", "note": "Affordable healthcare entry with growing demand in wellness and rehabilitation."},
        ]
        c["roi_timeline"] = "Government MBBS ROI: Outstanding — investment recovered within 6 months of first job. Private MBBS ROI: 5–8 years post-specialization. Specialist (MD/MS) starting at ₹15–30 LPA."
        if not c.get("summary"):
            c["summary"] = f"Diagnose, treat, and improve patient health and healthcare outcomes as a {c.get('name')}."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 with PCB (Physics, Chemistry, Biology)", "MBBS (5.5 yrs including internship) followed by MD/MS or Allied Health degree"]
        if not c.get("exams"):
            c["exams"] = ["NEET-UG", "NEET-PG / INI-CET (for MD/MS specialization)"]
        if not c.get("skills"):
            c["skills"] = ["Clinical Diagnosis", "Patient Empathy & Communication", "Pharmacology & Treatment Protocols", "Emergency Decision Making"]

    # 5. Finance / CA Block
    elif is_finance:
        c["job_roles"] = ["Chartered Accountant (CA)", "Investment Banker", "Equity Research Analyst", "Financial Planning Analyst (FPA)", "Tax Consultant", "Auditor", "Risk Manager", "Treasury Analyst", "Chief Financial Officer (CFO)"]
        c["career_ladder"] = ["Articleship Trainee / Analyst Intern (CA Foundation stage)", "Junior Analyst / CA Intermediate (2–3 yrs)", "Associate / CA Final Qualified (3–5 yrs)", "Senior Associate / Manager (5–8 yrs)", "Director / VP Finance (8–15 yrs)", "CFO / Managing Director"]
        c["typical_day"] = "Reviewing financial statements, building Excel models, preparing audit reports, client calls to discuss tax planning, analyzing market data or equity research, and presenting financial forecasts to senior management."
        c["work_dynamics"] = "Office and hybrid work. Deadline-heavy (especially during tax filing and audit seasons). High analytical work — Excel, financial databases, and data-heavy tasks dominate. Generally well-paid progression with structured career ladders."
        c["beginner_projects"] = ["Read and understand a company's Annual Report (try Infosys or Tata Motors)", "Build a simple personal budget tracker in Excel", "Track one stock for 30 days and write a one-page analysis", "Calculate the P&L of a hypothetical small business scenario", "Learn basic Excel (VLOOKUP, Pivot Tables, IF formulas)"]
        c["learn_platforms"] = ["ICAI Portal (CA Foundation study material — free)", "Zerodha Varsity (free investing & finance education)", "CFI (Corporate Finance Institute — free basics)", "Investopedia (financial concepts)", "NSE Academy Certification courses", "CA Wallah / Sanyam Jain on YouTube (CA prep)"]
        c["hackathons"] = ["ICAI Business Case Studies Competition", "CFA Institute Research Challenge", "NSE / BSE Investment Challenge", "IIM Finance Summits & Case Competitions", "RBI Young Scholars Award"]
        c["company_types"] = ["Big 4 Accounting (Deloitte, PwC, EY, KPMG)", "Investment Banks (Goldman Sachs, JP Morgan India, Morgan Stanley)", "Indian Banks (HDFC, ICICI, Axis, Kotak)", "NBFCs & Fintech (Zerodha, Groww, Paytm Money)", "Corporate Finance Teams (Reliance, TCS, Tata Group CFO office)"]
        c["future_outlook"] = "Strong. India's growing startup ecosystem, GST implementation, SEBI regulations, and international trade expansion create massive demand for finance professionals. AI is automating basic bookkeeping — specialists in tax law, investment strategy, and risk management are becoming more valuable."
        c["degree_costs"] = [
            {"tier": "CA (ICAI — Direct Route)", "cost": "₹30K – ₹80K (Total exam fees)", "note": "Highest finance ROI globally. 3-year articleship + self-study. Minimal cost."},
            {"tier": "B.Com / BBA (Government Colleges)", "cost": "₹50K – ₹2L (Total)", "note": "Excellent foundation. Delhi University, Christ, SRCC are top picks."},
            {"tier": "Private Commerce Colleges", "cost": "₹3L – ₹10L (Total)", "note": "Focus on placements data before choosing."},
        ]
        c["roi_timeline"] = "CA qualification: one of the highest-ROI credentials in India. CA fresher earns ₹7–12 LPA. Investment banker with MBA earns ₹20–40 LPA. Full ROI within 6–12 months of first job."
        if not c.get("summary"):
            c["summary"] = f"Manage financial planning, auditing, tax strategies, and capital allocation as a {c.get('name')}."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 (Commerce preferred, any stream eligible)", "B.Com / BBA + CA / CMA / CFA / CS certification"]
        if not c.get("exams"):
            c["exams"] = ["ICAI CA Foundation", "CMA Foundation", "CUET-UG (for top Commerce colleges)", "CAT (for MBA Finance)"]
        if not c.get("skills"):
            c["skills"] = ["Financial Accounting & Taxation", "Financial Modelling in Excel", "Corporate Auditing", "Risk & Capital Management"]

    # 6. Business & Management Block
    elif is_business:
        c["job_roles"] = ["Business Analyst", "Product Manager", "Management Consultant", "Operations Manager", "Marketing Manager", "Strategy Lead", "Startup Founder / Co-Founder", "Venture Capital Analyst", "Supply Chain Manager"]
        c["career_ladder"] = ["Business Analyst / Management Trainee (0–2 yrs)", "Associate Consultant / Product Associate (2–4 yrs)", "Manager / Senior Product Manager (4–7 yrs)", "Principal / Associate Director (7–10 yrs)", "VP / Director (10–15 yrs)", "CEO / Managing Director / Partner"]
        c["typical_day"] = "Stakeholder meetings and strategic discussions, data analysis to identify business opportunities, preparing presentations and reports, coordinating between teams (tech, design, marketing), and tracking KPIs and business metrics."
        c["work_dynamics"] = "Meeting-heavy and communication-intensive. Hybrid/office-dominant. Moderate to high stress depending on role. Consulting roles involve extensive travel. Leadership and networking are as important as technical skills."
        c["beginner_projects"] = ["Write a 1-page business plan for a local problem you've observed", "Analyze why a popular startup succeeded or failed (Case study format)", "Run a small-scale business experiment (sell something, track profit/loss)", "Do a SWOT analysis of your school's canteen business", "Read 'Zero to One' by Peter Thiel or 'The Lean Startup'"]
        c["learn_platforms"] = ["Harvard Business Review (free articles)", "NPTEL Business Management (IIT/IIM faculty — free)", "Coursera Business Foundations (Wharton — free audit)", "LinkedIn Learning (professional skills)", "IIMB Online Courses (IIM Bangalore — free/low cost)", "Case Interview resources (for consulting)"]
        c["hackathons"] = ["IIM Case Competition & B-School Summits", "E-Summit (IIT Bombay Entrepreneurship)", "National Entrepreneurship Challenge (NEC, Harvard India)", "Niti Aayog AIM ATL challenges", "CII Young Indians Leadership Programs"]
        c["company_types"] = ["Top Consulting Firms (McKinsey, BCG, Bain — 'MBB')", "Indian Conglomerates (Tata, Mahindra, Reliance — Management Trainee Programs)", "Startups (Founder/Early employee tracks)", "Venture Capital Firms (Sequoia, Accel, Elevation)", "FMCG & Consumer Companies (HUL, P&G, Nestle — strong management programs)"]
        c["future_outlook"] = "Perennially strong. The business world always needs strategic thinkers and leaders. Emerging specializations include AI Product Management, Climate Business Strategy, and Digital Transformation Consulting. MBA from top schools opens global doors."
        c["degree_costs"] = [
            {"tier": "IIM (5-Year IPMAT or MBA via CAT)", "cost": "₹25L – ₹30L (MBA total)", "note": "Average placement ₹25–35 LPA. ROI within 1–1.5 years."},
            {"tier": "BBA (Top Private Colleges — Symbiosis, Christ, NMIMS)", "cost": "₹8L – ₹18L (Total)", "note": "Good corporate exposure. Combine with CA or MBA for best outcomes."},
            {"tier": "B.Com + MBA Route", "cost": "₹5L – ₹15L (B.Com) + MBA costs", "note": "Cost-effective if B.Com is from a top college like SRCC or Loyola."},
        ]
        c["roi_timeline"] = "IIM MBA ROI: Typically recovered within 12–18 months. MBB consultant starting at ₹25–35 LPA. Startup founder route is high-risk, high-reward — no fixed timeline."
        if not c.get("summary"):
            c["summary"] = f"Drive organisational growth, operational efficiency, and leadership strategy as a {c.get('name')}."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 in any stream", "BBA / B.Com / B.Tech followed by MBA or Post Graduate Diploma in Management (PGDM)"]
        if not c.get("exams"):
            c["exams"] = ["CAT (for IIMs)", "IPMAT (5-Year IIM Indore/Rohtak)", "XAT", "GMAT"]
        if not c.get("skills"):
            c["skills"] = ["Strategic Decision Making", "Stakeholder Communication", "Financial & Data Analysis", "Team Leadership"]

    # 7. Design & Creative Block
    elif is_design:
        c["job_roles"] = ["UI/UX Designer", "Product Designer", "Visual Designer", "Interaction Designer", "Motion Designer", "Brand Designer", "UX Researcher", "Design Lead / Creative Director", "Industrial Designer", "Game Designer"]
        c["career_ladder"] = ["Junior Designer / Design Intern (0–2 yrs)", "Mid-level Designer (2–4 yrs)", "Senior Designer (4–7 yrs)", "Lead Designer / Design Manager (7–10 yrs)", "Creative Director / Head of Design (10+ yrs)", "Chief Design Officer (CDO)"]
        c["typical_day"] = "User research and interviews, wireframing and prototyping in Figma, design critique sessions with team, creating final visual assets, collaborating with developers on implementation, and iterating based on user feedback."
        c["work_dynamics"] = "Creative and collaborative. Hybrid/studio-friendly. Project-based workflows. High creative autonomy in senior roles. Freelance and remote work very common. Portfolio quality matters far more than degree brand."
        c["beginner_projects"] = ["Redesign the UI of your school's website or canteen menu", "Create an app wireframe for a problem you face daily (in Figma — free)", "Design a poster for a school event using Canva", "Build a personal brand logo and identity system", "Do a UX teardown: identify 5 usability issues in any app you use"]
        c["learn_platforms"] = ["Figma (free for students)", "Google UX Design Certificate (Coursera — affordable)", "Behance & Dribbble (portfolio inspiration)", "DesignWithArun YouTube (Indian UX)", "Nielsen Norman Group (UX research articles)", "Canva Design School (free basics)"]
        c["hackathons"] = ["Smart India Hackathon (Design Track)", "Adobe GenStudio Challenges", "Figma Community challenges", "NID, NIFT internal design fests", "Google UX Design Hackathons"]
        c["company_types"] = ["Tech Product Companies (Google, Zomato, Swiggy, Meesho — in-house design teams)", "Design Agencies (Elephant Design, Landor, Superunion India)", "Startups (early-stage design generalist roles)", "Advertising & Branding Agencies (Ogilvy, JWT, Leo Burnett)", "Freelance & Independent Design Studio"]
        c["future_outlook"] = "Excellent. AI design tools (Midjourney, Adobe Firefly) are changing workflows — but human design thinking, user research, and creative direction are more valuable. Companies realize that good design = better products = more revenue. Design is shifting from 'nice to have' to 'business-critical'."
        c["degree_costs"] = [
            {"tier": "NID / IIT Design (Government)", "cost": "₹3L – ₹8L (Total B.Des)", "note": "Hardest to get into. Highest design brand value in India."},
            {"tier": "NIFT (Government — Fees regulated)", "cost": "₹6L – ₹12L (Total)", "note": "Best for Fashion, Textile, and Accessory Design streams."},
            {"tier": "Private Design Schools (Srishti, MIT-ID, Pearl Academy)", "cost": "₹12L – ₹25L (Total)", "note": "Strong portfolio from reputable private schools opens industry doors."},
        ]
        c["roi_timeline"] = "UI/UX designers at tech companies: ₹6–15 LPA starting. Portfolio-driven career means ROI depends heavily on skill quality. Freelancers can earn ₹5–30 LPA depending on clients and specialization."
        if not c.get("summary"):
            c["summary"] = f"Craft intuitive visual experiences, user interfaces, and brand systems as a {c.get('name')}."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 in any stream", "B.Des (Bachelor of Design) or B.Sc in Multimedia / Animation with strong design portfolio"]
        if not c.get("exams"):
            c["exams"] = ["UCEED (IIT Bombay)", "NID DAT", "NIFT Entrance Exam", "CEED (for M.Des)"]
        if not c.get("skills"):
            c["skills"] = ["Figma & Prototyping", "Design Thinking & UX Research", "Visual Hierarchy & Typography", "Wireframing & Usability Testing"]

    # 8. Fallback for All Other Careers
    else:
        c["job_roles"] = [f"Entry-level Specialist in {c.get('name','')}", "Mid-level Domain Expert", "Senior Consultant / Manager", "Director / Independent Practitioner"]
        c["career_ladder"] = ["Entry Level (0–2 yrs)", "Mid Level Specialist (2–5 yrs)", "Senior Specialist / Manager (5–10 yrs)", "Director / Domain Leader (10+ yrs)"]
        c["typical_day"] = f"Daily work in {c.get('name','')} involves research, client or stakeholder interaction, project execution, and continuous domain knowledge building."
        c["work_dynamics"] = "Office or field-based work depending on the specialization. Regular interaction with clients, peers, and cross-functional teams."
        c["beginner_projects"] = ["Research 3 professionals working in this field on LinkedIn", "Read one foundational book about this career", "Shadow a professional in this field for a day", "Write a short essay on how this career helps society", "Find and join an online community (Reddit, Discord) around this field"]
        c["learn_platforms"] = ["Coursera / edX (domain-specific free courses)", "NPTEL (free IIT/IIM lectures)", "YouTube domain experts", "LinkedIn Learning", "Local professional associations and workshops"]
        c["hackathons"] = ["Domain-specific national competitions", "University-level case competitions", "Niti Aayog challenges", "Internship programs as competitive exposure"]
        c["company_types"] = ["Government departments and public sector units", "Private sector companies in this domain", "Non-governmental organizations (NGOs)", "International bodies and organizations", "Independent consulting and freelance practice"]
        c["future_outlook"] = "Growing specialization demand. As India's economy expands, all professional domains are seeing increased need for skilled, trained, and certified experts."
        c["degree_costs"] = [
            {"tier": "Government / State University", "cost": "₹50K – ₹3L (Total)", "note": "Most affordable. Quality varies by college."},
            {"tier": "Reputed Private Colleges", "cost": "₹5L – ₹15L (Total)", "note": "Research placement data before choosing."},
            {"tier": "Online Certification Route", "cost": "₹20K – ₹2L (Total)", "note": "Great for upskilling alongside a degree."},
        ]
        c["roi_timeline"] = "Varies by specialization. Research average salaries for your specific role in this field on LinkedIn Salary Insights or AmbitionBox."
        if not c.get("summary"):
            c["summary"] = f"Specialize as a professional {c.get('name')}, applying domain expertise and practical problem solving."
        if not c.get("qualifications"):
            c["qualifications"] = ["Class 12 in the relevant stream", f"Bachelor's degree in {c.get('name','related field')} or associated discipline"]
        if not c.get("exams"):
            c["exams"] = ["CUET-UG", "State University Entrance Tests", "National Domain Certification Exams"]
        if not c.get("skills"):
            c["skills"] = ["Domain Fundamentals", "Analytical Problem Solving", "Effective Communication", "Project Execution"]

    # Stream & Stage Pathways for dynamic toggle
    c["stream_pathways"] = {
        "class_10": {
            "title": "Class 9–10 Milestone",
            "action": f"Focus on high conceptual marks in core subjects related to {c.get('name','')}. Build habit of reading domain articles and practicing fundamental reasoning.",
            "next_step": "Choose the right stream (PCM, PCB, Commerce, or Arts) aligned with your target degree."
        },
        "class_12": {
            "title": "Class 11–12 Milestone",
            "action": f"Prepare consistently for key entrance tests: {', '.join(c.get('exams', ['Entrance Tests'])[:2])}. Balance board exams with entrance test problem solving.",
            "next_step": "Target top central/state universities or specialized institutes offering high placement ROI."
        },
        "college": {
            "title": "College & Career Launch",
            "action": f"Complete at least 2 real-world projects or internships. Network on LinkedIn and contribute to competitions/hackathons.",
            "next_step": "Build an active portfolio or prepare for campus recruitments and domain certifications."
        }
    }

    return c

def get_related_careers(cid: str, limit: int = 3):
    """Returns top 3 alternative/related careers for side-by-side comparison."""
    current = CAREERS.get(cid)
    if not current:
        return []

    current_tags = set(t.lower() for t in current.get("tags", []))
    current_cats = set(current.get("category_ids", []))
    current_groups = set(current.get("group_ids", []))

    scored = []
    for other_id, other in CAREERS.items():
        if other_id == cid:
            continue
        score = 0
        other_tags = set(t.lower() for t in other.get("tags", []))
        other_cats = set(other.get("category_ids", []))
        other_groups = set(other.get("group_ids", []))

        score += len(current_groups.intersection(other_groups)) * 25
        score += len(current_cats.intersection(other_cats)) * 15
        score += len(current_tags.intersection(other_tags)) * 5

        if score > 0:
            scored.append((score, other))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [enrich_career_details(dict(item[1])) for item in scored[:limit]]


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