import os
import json
import shutil

import numpy
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, HTTPException, File
from openai import OpenAI
import pypdfium2 as pdfium
from datetime import date

from pytesseract import pytesseract

from direct_skill_match import DirectSkillMatch
from prompt import get_prompt
from skill_interface import SkillInterface


app = FastAPI()

load_dotenv()
llm = OpenAI(api_key=os.getenv('MY_OPENAI_KEY'))

pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')


@app.post("/resume/upload", status_code=200)
async def upload_resume(skills_to_match: str, file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Input file not valid")

    # parse input skills to convert into list, strip trailing and leading spaces if any
    skills_to_match = list(map(lambda x: x.strip(), list(skills_to_match.split(","))))

    # save a copy of the file
    file_path = f"uploads/{file.filename}"
    save_file(file, file_path)

    # convert pdf to image and apply ocr get extract text
    pdf_text = extract_text_from_pdf(file_path)

    # get response from llm
    response = get_response_from_llm(pdf_text)

    # converts string to json and strips invalid characters
    formatted_response = json.loads(response[8:-3])

    # created an interface which can be extended to implement various skill matching techniques
    matcher: SkillInterface = DirectSkillMatch()
    match_percentage = matcher.skill_match(formatted_response["candidate_skills"], skills_to_match)

    return {
        "candidate_name": formatted_response.get("candidate_name"),
        "years_of_experience": get_years_of_experience(formatted_response),
        "year_of_graduation": formatted_response.get("year_of_graduation"),
        "match_percentage": match_percentage
    }


def get_years_of_experience(formatted_response: dict) -> int:
    from_date_list = formatted_response.get("professional_experience_start_date").split("-")
    from_date = date(year=int(from_date_list[0]), month=int(from_date_list[1]), day=int(from_date_list[2]))
    return int((date.today() - from_date).days / 365)


def get_response_from_llm(pdf_text: str) -> str:
    try:
        completion = llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": get_prompt() + pdf_text
                }
            ]
        )

        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenAI: {str(e)}")


def extract_text_from_pdf(file_path: str) -> str:
    pdf = pdfium.PdfDocument(file_path)
    text = ""

    # Loop over pages and render
    for i in range(len(pdf)):
        page = pdf[i]
        image = page.render(scale=4).to_numpy()
        text += extract_text_from_image(image)
        text += "\n"

    return text


def extract_text_from_image(image: numpy.ndarray) -> str:
    return pytesseract.image_to_string(image, config='--oem 3 --psm 6')


def save_file(file: UploadFile, file_path: str) -> None:
    os.makedirs("uploads", exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)