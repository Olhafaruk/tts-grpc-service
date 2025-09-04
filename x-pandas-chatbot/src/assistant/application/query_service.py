#src/assistant/application/query_service.py

import os
import json

import logging
from openai import OpenAI, OpenAIError
from fastapi import HTTPException

from assistant.application.table_store import TableService

from typing import Dict, Any
from assistant.application.function_registry import FUNCTIONS
from assistant.infrastructure.weaviate_client import WeaviateClient

logger = logging.getLogger(__name__)



class QueryService:
    def __init__(self, ts: TableService, vdb=None):
        self.ts = ts
        self.vdb = vdb or WeaviateClient()
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    def find_tables(self, query: str):
        res = (
            self.vdb.client.query
            .get("TableDoc", ["table_id","text"])
            .with_near_text({"concepts":[query], "certainty":0.7})
            .with_additional(["certainty"])
            .do()
        )
        docs = res["data"]["Get"]["TableDoc"]
        return [(d["table_id"], d["text"]) for d in docs]

    def ask(self, user_question: str) -> Dict[str,Any]:

        hits = self.find_tables(user_question)
        if not hits:
            logger.warning(f"No relevant tables found for question: '{user_question}'")
            return {"reply": "No relevant tables found to answer the question."}

        context = "\n\n".join(f"[{tid}]\n{text}" for tid, text in hits)

        table_ids = [tid for tid,_ in hits]

        logger.info(f"User question: {user_question}")
        logger.info(f"Found table_ids: {table_ids}")
        logger.info(f"Context passed to LLM:\n{context}")

        try:
            resp = self.llm.chat.completions.create(
                model=os.getenv("OPENAI_MODEL","gpt-3.5-turbo"),
                messages=[
                  {"role":"system","content":"You are a table assistant."},
                  {"role":"user","content": f"Context tables:\n{context}\n\nQuestion: {user_question}"}
                ],
                functions=FUNCTIONS,
                function_call="auto"
            )
        except OpenAIError as e:
            raise HTTPException(status_code=502, detail=str(e))

        msg = resp.choices[0].message


        if msg.function_call:
            name = msg.function_call.name
            args = json.loads(msg.function_call.arguments)

            logger.info(f"Function call received: {name}")
            logger.info(f"Function arguments: {args}")

            result = self._execute(name, args)

            logger.info(f"Function result: {result}")

            return {"function":name, "arguments":args, "result":result}

        logger.info(f"LLM reply: {msg.content}")
        return {"reply": msg.content}

    def _execute(self, name: str, args: Dict[str, Any]) -> Any:
        df_store = self.ts
        logger.info(f"Executing function '{name}' with args: {args}")

        if name in {"filter_rows", "show_table", "convert_currency", "rename_column"}:
            table_id = args.get("table_id")
            if not table_id or table_id not in self.ts.tables:
                try:
                    latest_id = self.ts.get_latest_id()
                except KeyError:
                    raise HTTPException(status_code=404, detail="No tables available")
                args["table_id"] = latest_id
                logger.info(f"Using latest table_id: {latest_id}")
        logger.info(f"Final args for '{name}': {args}")

        if name == "filter_rows":
            df = df_store.get_any(args["table_id"])
            filtered = df[df[args["column"]] == args["value"]]
            rows = filtered.head(args.get("n_rows", 5)).to_dict(orient="records")
            return {"rows": rows}

        if name == "merge_tables":
            df1 = df_store.get_any(args["table1_id"])
            df2 = df_store.get_any(args["table2_id"])
            merged = df1.merge(df2, on=args["on"], how=args.get("how", "inner"))
            return {
                "table_id": df_store.upload("merged.csv", merged.to_csv(index=False).encode())
            }

        if name == "rename_column":
            df = df_store.get_any(args["table_id"])
            if args["old_name"] not in df.columns:
                raise HTTPException(status_code=400, detail=f"Column '{args['old_name']}' not found in table.")
            df2 = df.rename(columns={args["old_name"]: args["new_name"]})
            return {
                "table_id": df_store.upload("renamed.csv", df2.to_csv(index=False).encode())
            }

        if name == "convert_currency":
            df = df_store.get_any(args["table_id"])
            if args["column"] not in df.columns:
                raise HTTPException(status_code=400, detail=f"Column '{args['column']}' not found in table.")
            try:
                df[args["column"]] *= args["exchange_rate"]
            except Exception as e:
                logger.error(f"Failed to convert currency in column '{args['column']}': {e}")
                raise HTTPException(status_code=500, detail=f"Currency conversion failed: {e}")
            return {
                "table_id": df_store.upload("converted.csv", df.to_csv(index=False).encode())
            }

        if name == "show_table":
            df = df_store.get_any(args["table_id"])
            rows = df.head(args.get("n_rows", 5)).to_dict(orient="records")
            return {"rows": rows}

        logger.warning(f"Unknown function requested: {name}")
        raise HTTPException(status_code=400, detail=f"Unknown function '{name}'")

