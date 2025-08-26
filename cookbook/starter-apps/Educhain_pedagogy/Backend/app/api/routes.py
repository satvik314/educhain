from fastapi import APIRouter, HTTPException
from app.models.pedagogy_models import ContentRequest, ContentResponse, PedagogyInfo
from app.services.educhain_services import generate_content, get_pedagogies
import logging
from typing import Dict

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate-content", response_model=ContentResponse)
def generate_content_route(req: ContentRequest):
    try:
        result = generate_content(req.topic, req.pedagogy, req.params)
        return ContentResponse(
            pedagogy=req.pedagogy,
            topic=req.topic,
            content=result
        )
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available-pedagogies", response_model=Dict[str, PedagogyInfo])
def get_available_pedagogies_route():
    try:
        return get_pedagogies()
    except Exception as e:
        logger.error(f"Error fetching pedagogies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

