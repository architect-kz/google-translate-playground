from fastapi import APIRouter

router = APIRouter(tags=["healthcheck"])


@router.get('/healthcheck')
async def healthcheck() -> dict:
    """ We can implement soon """
    return {'status': 'OK'}
