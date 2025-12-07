import time

from fastapi import Request, Response
from fastapi.routing import APIRoute
from typing import Callable

class Route(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            return response

        return custom_route_handler
