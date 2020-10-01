from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer_dir
from app.ocr.text_complexity import evaluate, good_vocab_stars, efficiency_stars, descriptiveness_stars, \
        sentence_length_stars, word_length_stars
from pydantic import BaseModel

router = APIRouter()


class ImageOcrS3Dir(BaseModel):
    s3_dir: str
    get_complexity_score: int = 0


@router.post('/img_ocr_s3_dir')
async def ocr(params: ImageOcrS3Dir):
    """
    Handwriting recognizer with google's vision API for
    all .jpg files in a dir

    ### Request Body

    - `s3_dir`: string
        - example:
        "Stories Dataset/Transcribed Stories/31--/3101/"

    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    ### Response
    - `ocr_text_list`: list, a list of strings representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.s3_obj is not None:
        ocr_text = google_handwriting_recognizer_dir(s3_dir=params.s3_dir)
        return {
            "ocr_text": ocr_text,
            "vocab_score" : good_vocab_stars(ocr_text),
            "efficiency_score" : efficiency_stars(ocr_text),
            "descriptiveness_score" : descriptiveness_stars(ocr_text),
            "sentence_length_score" : sentence_length_stars(ocr_text),
            "word_length_score" : word_length_stars(ocr_text),
            "complexity_score": evaluate(ocr_text)
            
        }

    else:
        return "s3_obj was not set"