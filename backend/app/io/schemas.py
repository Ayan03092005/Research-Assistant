from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any

# Auth & Users
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# Projects
class ProjectCreate(BaseModel):
    title: str
    domain: str
    aim: str

class ProjectOut(BaseModel):
    id: int
    title: str
    domain: str
    aim: str

# Features
class SurveyRequest(BaseModel):
    topic: str
    keywords: List[str] = []
    n_results: int = 20
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    project_id: Optional[int] = None

class PaperBrief(BaseModel):
    title: str
    first_author: str
    year: str | None = None
    venue: str | None = None
    doi: str | None = None
    url: str | None = None
    provider: str

class SurveyResponse(BaseModel):
    papers: List[PaperBrief]
    draft: Optional[str] = None  # filled when Generate Draft is requested (front-end trigger)

class GapRequest(BaseModel):
    aim: str
    selected_papers: List[PaperBrief]

class GapResponse(BaseModel):
    limitations: List[Dict[str, Any]]
    opportunities: List[Dict[str, Any]]

class TranslateRequest(BaseModel):
    document_id: int
    target_lang: str = "en"
    full: bool = True

class TranslateResponse(BaseModel):
    translated_text: str
    download_url: Optional[str] = None

class PersonaSummaryRequest(BaseModel):
    document_id: int | None = None
    raw_text: str | None = None
    persona: str = "student"
    focus: str = "methods"
    length: str = "short"

class PersonaSummaryResponse(BaseModel):
    summary: str

class MethodologyRequest(BaseModel):
    concept: str
    datasets: List[str] = []
    baselines: List[str] = []
    constraints: Dict[str, Any] = {}

class MethodologyResponse(BaseModel):
    flowchart_json: Dict[str, Any]
    rationale: str

class ReplicatorRequest(BaseModel):
    methodology_json: Dict[str, Any]
    candidate_papers: List[PaperBrief]

class ReplicatorResponse(BaseModel):
    overlay_json: Dict[str, Any]
    notes: str

class CrossDomainRequest(BaseModel):
    draft_text: str
    target_domains: List[str]

class CrossDomainResponse(BaseModel):
    mappings: List[Dict[str, Any]]
    narrative: str

class BenchmarkRequest(BaseModel):
    task_type: str
    datasets: List[str] = []
    constraints: Dict[str, Any] = {}

class BenchmarkResponse(BaseModel):
    metrics: List[Dict[str, Any]]
    guidance: str

class ContradictionRequest(BaseModel):
    methodology_text: str
    results_text: str
    domain: str

class ContradictionResponse(BaseModel):
    conflicts: List[Dict[str, Any]]

class CitationValidateRequest(BaseModel):
    draft_markdown: str
    style: str = "IEEE"

class CitationValidateResponse(BaseModel):
    annotated_markdown: str
    references: List[str]

class LatexRequest(BaseModel):
    draft_markdown: str
    template: str = "conference"

class LatexResponse(BaseModel):
    zip_url: str

# Jobs
class JobOut(BaseModel):
    id: int
    type: str
    status: str
    message: str
