from pydantic import BaseModel, model_validator, Field


class CreateCat(BaseModel):
    name: str
    exp_years: int = Field(..., gt=0)
    breed: str
    salary: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class UpdateCat(BaseModel):
    exp_years: int | None = Field(default=None, gt=0)
    salary: int | None = Field(default=None, gt=0)


    @model_validator(mode='after')
    @classmethod
    def check_at_least_one(cls, model):
        if not any([model.name, model.exp_years, model.breed, model.salary]):
            raise ValueError('At least one field should be provided')

        return model

    class Config:
        from_attributes = True


class CatResponse(BaseModel):
    id: int
    name: str
    exp_years: int
    breed: str
    salary: int

    # class Config:
    #     orm_mode = True

