from utils import load_catalog
from llm import extract_hiring_intent


TECH_KEYWORDS = {
    # Generic tech roles
    "developer", "engineer", "programmer", "architect",
    "software", "technical", "backend", "frontend",
    "fullstack", "full stack", "api", "rest", "microservices",

    # Cloud / DevOps
    "cloud", "aws", "azure", "gcp", "devops", "docker",
    "kubernetes", "terraform", "jenkins", "ci/cd",
    "linux", "unix", "server", "infrastructure",
    "platform engineer", "site reliability engineer", "sre",
    "cloud engineer", "infrastructure engineer",
    "systems engineer",

    # Programming languages
    "java", "python", "c", "c++", "c#", ".net",
    "javascript", "typescript", "node", "nodejs",
    "php", "ruby", "golang", "go", "rust",
    "scala", "kotlin", "swift", "perl",

    # Frameworks
    "react", "angular", "vue", "django", "flask",
    "fastapi", "spring", "spring boot", "hibernate",
    "express", "nestjs", "laravel",

    # Databases
    "sql", "mysql", "postgresql", "mongodb",
    "oracle", "nosql", "redis", "snowflake",
    "database", "database developer", "database engineer",

    # Data Engineering
    "etl", "hadoop", "spark", "airflow",
    "data warehouse", "data modeling",

    # Data / Analytics
    "data analyst", "senior data analyst", "junior data analyst",
    "business analyst", "business intelligence analyst",
    "bi analyst", "bi developer", "reporting analyst",
    "analytics engineer", "data engineer",
    "data architect", "research analyst",
    "insights analyst", "decision scientist",
    "product analyst", "quant analyst",
    "statistical analyst",
    "analytics", "analysis", "reporting",
    "dashboard", "visualization",
    "power bi", "tableau", "excel",
    "business intelligence", "kpi",
    "statistics", "statistical analysis",
    "data cleaning", "data wrangling",

    # AI / ML
    "data scientist", "machine learning engineer",
    "ml engineer", "ai engineer",
    "artificial intelligence engineer",
    "deep learning engineer",
    "nlp engineer", "computer vision engineer",
    "research scientist", "ai researcher",
    "prompt engineer", "llm engineer",
    "machine learning", "ml", "ai",
    "artificial intelligence", "deep learning",
    "nlp", "computer vision", "llm",
    "generative ai", "transformers",
    "neural networks", "tensorflow",
    "pytorch", "scikit-learn",

    # QA / Testing
    "qa", "testing", "automation",
    "selenium", "pytest", "test engineer",

    # Security
    "cybersecurity", "security", "soc",
    "network security", "penetration testing",
    "ethical hacking", "infosec",

    # Networking
    "network"
}


BEHAVIORAL_KEYWORDS = {
    "manager", "management", "sales", "leadership",
    "customer support", "customer service", "communication",
    "people management", "team lead", "recruiter",
    "hr", "human resources", "marketing",
    "business development", "operations", "support",
    "relationship manager", "account manager"
}


TECH_ASSESSMENT_HINTS = {
    "java", "python", "sql", "react", "javascript",
    "typescript", "docker", "kubernetes", "aws",
    "azure", "gcp", "cloud", "api", "backend",
    "frontend", "spring", ".net", "c#", "node",
    "data science", "machine learning", "analytics",
    "power bi", "tableau", "excel", "qa", "testing"


    # data analytics
    "data analyst",
    "business analyst",
    "analytics",
    "analysis",
    "power bi",
    "tableau",
    "excel",
    "reporting",
    "dashboard",
    "data science",
    "machine learning"
}


BEHAVIORAL_ASSESSMENT_HINTS = {
    "opq", "sales", "customer service", "leadership",
    "manager", "motivation", "behavioral",
    "personality", "communication", "supervisor"
}


COGNITIVE_ASSESSMENT_HINTS = {
    "verify", "reasoning", "cognitive",
    "numerical", "deductive", "logical",
    "ability", "problem solving"
}


def classify_role(message):
    message = message.lower()

    if any(word in message for word in TECH_KEYWORDS):
        return "technical"

    if any(word in message for word in BEHAVIORAL_KEYWORDS):
        return "behavioral"

    return "unknown"


def classify_assessment(assessment):
    name = assessment.get("name", "")
    test_type = assessment.get("test_type", "")

    if not isinstance(name, str):
        name = ""

    if not isinstance(test_type, str):
        test_type = ""

    name = name.lower()
    test_type = test_type.lower()

    if "technical" in test_type:
        return "technical"

    if "behavioral" in test_type:
        return "behavioral"

    if "cognitive" in test_type:
        return "cognitive"

    if any(word in name for word in TECH_ASSESSMENT_HINTS):
        return "technical"

    if any(word in name for word in BEHAVIORAL_ASSESSMENT_HINTS):
        return "behavioral"

    if any(word in name for word in COGNITIVE_ASSESSMENT_HINTS):
        return "cognitive"

    return "general"

def score_assessment(assessment, role_type, user_text, extracted_skills):
    score = 0

    name = assessment.get("name", "")
    if not isinstance(name, str):
        name = ""
    name = name.lower()

    category = classify_assessment(assessment)

    # Strict filtering
    if role_type == "technical":
        if category not in ["technical"]:
            return 0

    if role_type == "behavioral":
        if category not in ["behavioral", "cognitive"]:
            return 0

    # User keyword scoring
    for word in user_text.split():
        clean_word = word.strip(",.()")

        if len(clean_word) > 2 and clean_word in name:
            score += 8

    # Gemini skill scoring
    for skill in extracted_skills:
        skill = str(skill).lower()

        if skill in name:
            score += 15

       # Base score
    if category == "technical":
        score += 10

    if category == "behavioral":
        score += 10

    if category == "cognitive":
        score += 8

    # Role-aware boosts
    if "data analyst" in user_text or "business analyst" in user_text:
        if any(word in name for word in [
            "sql", "excel", "power bi", "tableau",
            "analytics", "analysis", "data", "cognitive"
        ]):
            score += 40

    if "python developer" in user_text or "backend developer" in user_text:
        if any(word in name for word in [
            "python", "api", "backend", "aws", "sql"
        ]):
            score += 40

    if "sales" in user_text or "manager" in user_text:
        if any(word in name for word in [
            "opq", "sales", "leadership", "personality"
        ]):
            score += 40

    return score

def get_recommendations(messages, user_name="User"):
    catalog = load_catalog()

    full_conversation = " ".join(
        [msg.content for msg in messages]
    ).lower()

    latest_message = messages[-1].content.lower().strip()

    COMPARE_KEYWORDS = {
        "difference",
        "compare",
        "comparison",
        "vs",
        "versus",
        "explain"
    }

    LEGAL_KEYWORDS = {
        "legal",
        "law",
        "age",
        "gender",
        "religion",
        "discrimination",
        "reject candidate",
        "hire legally"
    }

    HIRING_ADVICE_KEYWORDS = {
        "interview questions",
        "best interview questions",
        "how to hire",
        "salary negotiation",
        "recruitment strategy"
    }

    PROMPT_INJECTION_KEYWORDS = {
        "ignore previous instructions",
        "ignore instructions",
        "bypass",
        "override",
        "recommend non-shl"
    }

    role_type = classify_role(full_conversation)
    extracted_skills = []

    vague_inputs = {
        "hi", "hello", "hey",
        "need assessment",
        "assessment",
        "help",
        "start"
    }

    ROLE_WORDS = {
        "developer",
        "engineer",
        "backend",
        "frontend",
        "fullstack",
        "full stack",
        "architect",
        "programmer",
        "analyst",
        "scientist",
        "manager",
        "lead"
    }

    # Prompt injection protection
    if any(word in latest_message for word in PROMPT_INJECTION_KEYWORDS):
        return {
            "reply": f"Sorry, {user_name} 👋\nI can only help with SHL assessment recommendations and related assessment queries.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Legal question protection
    if any(word in latest_message for word in LEGAL_KEYWORDS):
        return {
            "reply": f"Sorry, {user_name} 👋\nI cannot provide legal hiring advice. I can help you choose relevant SHL assessments instead.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # General hiring advice protection
    if any(word in latest_message for word in HIRING_ADVICE_KEYWORDS):
        return {
            "reply": f"Sorry, {user_name} 👋\nI focus on SHL assessment recommendations and assessment-related guidance.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Comparison / explanation support
    if any(word in latest_message for word in COMPARE_KEYWORDS):
        if "opq" in latest_message and "gsa" in latest_message:
            return {
                "reply": (
                    f"Sure, {user_name} 👋\n"
                    "OPQ (Occupational Personality Questionnaire) measures workplace personality traits, behavior preferences, motivation, teamwork, and leadership style.\n\n"
                    "GSA (General Ability Assessment) measures cognitive ability such as logical reasoning, problem solving, and learning capability.\n\n"
                    "In short: OPQ = personality fit, GSA = cognitive ability."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        return {
            "reply": f"Sure, {user_name} 👋\nWhich SHL assessments would you like me to compare?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Vague query handling
    if any(vague in latest_message for vague in vague_inputs):
        return {
            "reply": f"Hi {user_name} 👋\nI can help you find the most relevant SHL assessments for your hiring needs.\nWhat role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    try:
        llm_result = extract_hiring_intent(latest_message)

        if not isinstance(llm_result, dict):
            llm_result = {}

        GENERIC_TERMS = {
            "developer",
            "engineer",
            "backend",
            "frontend",
            "fullstack",
            "full stack",
            "architect",
            "programmer",
            "analyst",
            "scientist",
            "manager",
            "lead",
            "software",
            "technical",
            "api",
            "microservices",
            "server",
            "sales"
        }

        skills = llm_result.get("skills", [])

        if not isinstance(skills, list):
            skills = []

        for skill in skills:
            clean_skill = str(skill).lower().strip()

            if clean_skill not in GENERIC_TERMS:
                if clean_skill in latest_message:
                    extracted_skills.append(clean_skill)

        detected_role = llm_result.get("role_type", "unknown")

        if detected_role in ["technical", "behavioral"]:
            if role_type == "unknown":
                role_type = detected_role

    except Exception:
        extracted_skills = []

    if role_type == "unknown":
        return {
            "reply": f"Hi {user_name} 👋\nI can help you find relevant SHL assessments.\nWhat role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    raw_skill_detected = any(
        keyword in latest_message
        for keyword in TECH_KEYWORDS
        if keyword not in ROLE_WORDS
    )

    if role_type == "technical":
        role_only_query = any(word in latest_message for word in [
            "developer",
            "engineer",
            "backend",
            "frontend",
            "programmer",
            "architect"
        ])

        explicit_skill_present = any(skill in latest_message for skill in [
            "java", "python", "sql", "react", "node", "nodejs",
            "spring", "aws", "azure", "gcp", "docker",
            "kubernetes", ".net", "c#", "javascript", "typescript"
        ])

        if role_only_query and not explicit_skill_present:
            return {
                "reply": f"Got it, {user_name} 👋\nAre there any specific technologies or skills required?\nFor example: Java, Python, Spring Boot, SQL, AWS.",
                "recommendations": [],
                "end_of_conversation": False
            }

    scored_results = []

    for item in catalog:
        score = score_assessment(
            item,
            role_type,
            full_conversation,
            extracted_skills
        )

        if score > 0:
            scored_results.append((score, item))

    scored_results.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    top_matches = [
        item for score, item in scored_results[:10]
    ]

    if not top_matches:
        return {
            "reply": f"I couldn't find suitable SHL assessments, {user_name}. Please refine your hiring criteria.",
            "recommendations": [],
            "end_of_conversation": False
        }

    return {
        "reply": f"Perfect, {user_name} 👋\nI found {len(top_matches)} highly relevant SHL assessments for your hiring needs.",
        "recommendations": top_matches,
        "end_of_conversation": False
    }