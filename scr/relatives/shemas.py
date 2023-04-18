from typing import Optional

from pydantic import BaseModel

from datetime import date


class CreateRelatives(BaseModel):
    last_name: str
    first_name: str
    surname : Optional [str]
    birth_data: Optional [date]
    death_data: Optional [date]
    sity: Optional [str]

    class Config:
        orm_mode = True
