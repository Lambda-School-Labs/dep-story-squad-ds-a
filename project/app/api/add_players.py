from fastapi import APIRouter, HTTPException

from typing import Dict, List
from pydantic import BaseModel, Field
import boto3

router = APIRouter()


class AddPlayers(BaseModel):

    # user_stories: List[Dict["user_id": str, "s3_dir": str]] =\
    user_stories: List[Dict[str, str]] =\
        Field(..., example=[
                {
                    "user_id": "12322187",
                    "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
                },
                {
                    "user_id": "12322188",
                    "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322188/story_5"
                },
            ]
        )


# TODO make it actually it is available for Mon ~ Wed
@router.post('/multiplayer/add_players')
async def add_players(params: AddPlayers):
    """
    It's available to use from Monday till Wednesday.
    Adds players to a table to match them together later.

    ### Request Body

    - `user_stories`: List[Dict{"user_id": str, "s3_dir": str}]


    ### Response
    "successfully added"
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_stories')

    for player_story in params.user_stories:
        # Get the service resource.
        print(player_story)
        table.put_item(
            Item=player_story
        )

    return "successfully added"
