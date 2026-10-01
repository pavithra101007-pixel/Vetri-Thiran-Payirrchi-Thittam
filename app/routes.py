import os
import uuid

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.gemini_flash import generate_comic_story
from app.layout_builder import build_comic_layout
from app.exporters import export_comic_pdf


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------
# PDF EXPORT FOLDER
# --------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

EXPORT_FOLDER = os.path.join(
    BASE_DIR,
    "generated",
    "exports"
)


# IMPORTANT:
# The generated/exports folder already exists.
# We do NOT create it again here.


# --------------------------------
# HOME PAGE
# --------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# --------------------------------
# GENERATE COMIC STORY
# --------------------------------

@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate_comic(

    request: Request,

    story_prompt: str = Form(...),

    character: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

    story = generate_comic_story(

        story_prompt=story_prompt,

        character=character,

        setting=setting,

        tone=tone,

        art_style=art_style
    )


    comic = build_comic_layout(
        story
    )


    return templates.TemplateResponse(

        request=request,

        name="comic_preview.html",

        context={

            "request": request,

            "story": story,

            "comic": comic
        }
    )


# --------------------------------
# EXPORT PDF
# --------------------------------

@router.post(
    "/export-pdf",
    response_class=HTMLResponse
)
async def export_pdf(

    request: Request,

    comic_title: str = Form(...),

    panel_titles: list[str] = Form(...),

    panel_narrations: list[str] = Form(...),

    panel_dialogues: list[str] = Form(...),

    panel_images: list[str] = Form(...)
):

    comic = []


    for index in range(
        len(panel_titles)
    ):

        comic.append({

            "panel": index + 1,

            "title": panel_titles[index],

            "narration": panel_narrations[index],

            "dialogue": panel_dialogues[index],

            "image_prompt": panel_images[index]

        })


    # Create unique PDF filename

    filename = (
        "comic_"
        + uuid.uuid4().hex[:8]
        + ".pdf"
    )


    output_path = os.path.join(
        EXPORT_FOLDER,
        filename
    )


    # Create PDF

    export_comic_pdf(

        comic=comic,

        output_path=output_path,

        comic_title=comic_title
    )


    pdf_file = (
        "/download/"
        + filename
    )


    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={

            "request": request,

            "pdf_file": pdf_file,

            "comic_title": comic_title

        }
    )


# --------------------------------
# DOWNLOAD PDF
# --------------------------------

@router.get(
    "/download/{filename}"
)
async def download_pdf(
    filename: str
):

    file_path = os.path.join(
        EXPORT_FOLDER,
        filename
    )


    if not os.path.isfile(
        file_path
    ):

        return HTMLResponse(
            "PDF file not found.",
            status_code=404
        )


    return FileResponse(

        path=file_path,

        filename=filename,

        media_type="application/pdf"
    )