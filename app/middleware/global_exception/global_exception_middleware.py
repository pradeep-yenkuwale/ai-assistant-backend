
from traceback import print_exception
from fastapi import Request, Response


async def exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        print("error", error)
        return Response(str(error), status_code=500)
