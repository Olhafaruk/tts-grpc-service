# src/assistant/core.py


from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class PatchedFastAPI(FastAPI):
    def openapi(self):
        if self.openapi_schema:
            return self.openapi_schema

        # 1) Генерация базовой схемы
        openapi_schema = get_openapi(
            title=self.title,
            version=self.version,
            routes=self.routes,
        )

        comp_name = "Body_upload_upload_post"
        schemas = openapi_schema.setdefault("components", {}).setdefault("schemas", {})
        comp = schemas.get(comp_name)
        if comp:
            files_prop = comp["properties"]["files"]
            # обязательно format: binary для items
            files_prop["items"]["format"] = "binary"

        path_item = (
            openapi_schema.get("paths", {})
            .get("/upload", {})
            .get("post", {})
            .get("requestBody", {})
            .get("content", {})
            .get("multipart/form-data", {})
        )
        if path_item is not None:
            path_item.setdefault("encoding", {})["files"] = {
                "style": "form",
                "explode": True,
            }

        self.openapi_schema = openapi_schema
        return self.openapi_schema
