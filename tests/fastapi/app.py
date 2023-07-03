from typing import Any, Dict, Optional, Union

from fastapi import BackgroundTasks, Depends, FastAPI, Request, WebSocket
from strawberry.fastapi import GraphQLRouter
from tests.views.schema import schema


def custom_context_dependency() -> str:
    return "Hi!"


async def get_context(
    background_tasks: BackgroundTasks,
    request: Optional[Request] = None,
    ws: Optional[WebSocket] = None,
    custom_value=Depends(custom_context_dependency),
) -> Dict[str, Any]:
    return {
        "custom_value": custom_value,
        "request": request or ws,
        "background_tasks": background_tasks,
    }


async def get_root_value(
    request: Optional[Request] = None, ws: Optional[WebSocket] = None
) -> Union[Request, WebSocket]:
    return request or ws


def create_app(schema=schema, **kwargs: Any) -> FastAPI:
    app = FastAPI()

    graphql_app = GraphQLRouter(
        schema, context_getter=get_context, root_value_getter=get_root_value, **kwargs
    )
    app.include_router(graphql_app, prefix="/graphql")

    return app
