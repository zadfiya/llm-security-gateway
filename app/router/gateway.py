from pydantic import BaseModel
router = APIRouter()

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    provider: str


@router.get("/HelloWorld")
async def get(request)
    item = {'Success':true, message:'Hello Wolrd'}
    return JSONResponse(status_code=status.HTTP_200_OK , content=item)

