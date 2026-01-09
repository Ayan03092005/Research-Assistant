from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body, Query, status
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

# CRITICAL FIX: Restore ALL necessary security functions for login/register/auth
from .core.security import get_current_user, create_access_token, verify_password, get_password_hash
from .core.rbac import require_role, Roles
from .db.session import get_db
from .db import models
from .io.schemas import (
    LoginRequest, LoginResponse, UserCreate, UserOut, ProjectCreate, ProjectOut,
    SurveyRequest, SurveyResponse, GapRequest, GapResponse, TranslateRequest, TranslateResponse,
    PersonaSummaryRequest, PersonaSummaryResponse, MethodologyRequest, MethodologyResponse,
    ReplicatorRequest, ReplicatorResponse, CrossDomainRequest, CrossDomainResponse,
    BenchmarkRequest, BenchmarkResponse, ContradictionRequest, ContradictionResponse,
    CitationValidateRequest, CitationValidateResponse, LatexRequest, LatexResponse, JobOut
)
from .features.literature_survey import generate_literature_survey
from .features.research_gap_finder import find_research_gaps
from .features.translator import translate_paper
from .features.persona_summarizer import make_persona_summary
from .features.methodology_builder import build_methodology
from .features.experiment_replicator import suggest_experiment_variants
from .features.cross_domain_synth import synthesize_cross_domain
from .features.benchmark_explorer import recommend_benchmarks
from .features.contradiction_analyzer import analyze_contradictions
from .features.citation_validator import validate_citations
from .features.latex_generator import generate_latex_package
from .voice.speech_io import transcribe_audio
from .io.storage import save_upload

router = APIRouter()

# ---------------------- Auth ----------------------

@router.post("/auth/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.scalar(select(models.User).where(models.User.email == payload.email))
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # FIX: Truncate password before hashing to prevent ValueError (bcrypt limit of 72 bytes)
    truncated_password = payload.password[:72]

    user = models.User(
        email=payload.email,
        name=payload.name,
        role=payload.role,
        password_hash=get_password_hash(truncated_password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=user.id, email=user.email, name=user.name, role=user.role)

@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(models.User).where(models.User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Payload must include 'sub' (user ID) and 'role'
    token = create_access_token({"sub": str(user.id), "role": user.role})
    
    return LoginResponse(access_token=token, token_type="bearer", 
                         user=UserOut(id=user.id, email=user.email, name=user.name, role=user.role))


@router.get("/auth/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    return UserOut(id=current.id, email=current.email, name=current.name, role=current.role)

# ---------------------- Projects & Uploads ----------------------

@router.post("/projects", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    project = models.Project(user_id=current.id, title=payload.title, domain=payload.domain, aim=payload.aim)
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectOut(id=project.id, title=project.title, domain=project.domain, aim=project.aim)

@router.get("/projects", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db), current=Depends(get_current_user)):
    # Filter projects by the current authenticated user's ID
    rows = db.scalars(select(models.Project).where(models.Project.user_id == current.id)).all()
    return [ProjectOut(id=p.id, title=p.title, domain=p.domain, aim=p.aim) for p in rows]

# FIX: Added missing route handler for fetching a single project
@router.get("/projects/{project_id}", response_model=ProjectOut)
def get_project_by_id(project_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    # Retrieve project by ID
    project = db.get(models.Project, project_id)
    
    # Check if project exists AND if the current user is the owner (Authorization)
    if not project or project.user_id != current.id:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return ProjectOut(id=project.id, title=project.title, domain=project.domain, aim=project.aim)


@router.post("/upload", response_model=Dict[str, Any])
def upload_document(
    project_id: int = Query(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    path = save_upload(file)
    doc = models.Document(project_id=project_id, user_id=current.id, filename=file.filename, path=path, mime=file.content_type)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"document_id": doc.id, "filename": doc.filename}

# ---------------------- Feature Endpoints ----------------------

# 1) Literature Survey Generator
@router.post("/survey/generate", response_model=SurveyResponse)
def survey_generate(payload: SurveyRequest, db: Session = Depends(get_db), current=Depends(require_role(Roles.researcher_like()))):
    return generate_literature_survey(payload, db, current)

# 2) Research Gap Finder
@router.post("/survey/gaps", response_model=GapResponse)
def survey_gaps(payload: GapRequest, db: Session = Depends(get_db), current=Depends(require_role(Roles.researcher_like()))):
    return find_research_gaps(payload, db, current)

# 3) Multilingual Research Paper Translator
@router.post("/translate", response_model=TranslateResponse)
def translate(payload: TranslateRequest, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return translate_paper(payload, db, current)

# 4) Persona-based Summarizer
@router.post("/summary/persona", response_model=PersonaSummaryResponse)
def persona_summary(payload: PersonaSummaryRequest, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return make_persona_summary(payload, db, current)

# 5) Methodology Builder
@router.post("/methodology/build", response_model=MethodologyResponse)
def methodology_build(payload: MethodologyRequest, db: Session = Depends(get_db), current=Depends(require_role(Roles.researcher_like()))):
    return build_methodology(payload, db, current)

# 6) Experiment Replicator
@router.post("/methodology/replicate", response_model=ReplicatorResponse)
def methodology_replicate(payload: ReplicatorRequest, db: Session = Depends(get_db), current=Depends(require_role(Roles.researcher_like()))):
    return suggest_experiment_variants(payload, db, current)

# 7) Cross-Domain Synthesizer
@router.post("/cross-domain/suggest", response_model=CrossDomainResponse)
def cross_domain(payload: CrossDomainRequest, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return synthesize_cross_domain(payload, db, current)

# 8) Benchmark Evolution Explorer
@router.post("/benchmark/recommend", response_model=BenchmarkResponse)
def benchmark(payload: BenchmarkRequest, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return recommend_benchmarks(payload, db, current)

# 9) Contradiction Analyzer
@router.post("/contradiction/scan", response_model=ContradictionResponse)
def contradiction(payload: ContradictionRequest, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return analyze_contradictions(payload, db, current)

# 10) Citation & Reference Validator
@router.post("/citation/validate", response_model=CitationValidateResponse)
def citation_validate(payload: CitationValidateRequest, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return validate_citations(payload, db, current)

# 11) LaTeX Typescript Generator
@router.post("/latex/generate", response_model=LatexResponse)
def latex(payload: LatexRequest, db: Session = Depends(get_db), current=Depends(require_role(Roles.researcher_like()))):
    return generate_latex_package(payload, db, current)

# 12) Voice/Text (Whisper)
@router.post("/voice/transcribe", response_model=Dict[str, str])
def voice_transcribe(file: UploadFile = File(...), current=Depends(get_current_user)):
    text = transcribe_audio(file)
    return {"transcript": text}

# ---------------------- Jobs (simple placeholders) ----------------------

@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    job = db.get(models.Job, job_id)
    if not job or job.user_id != current.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobOut(id=job.id, type=job.type, status=job.status, message=job.message)
