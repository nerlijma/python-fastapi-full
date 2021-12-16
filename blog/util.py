from starlette.responses import JSONResponse


def json_error(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "message": message},
    )
