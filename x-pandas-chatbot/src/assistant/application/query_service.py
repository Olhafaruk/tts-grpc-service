#src/assistant/application/query_service.py

import os
import json
import pandas as pd
from openai import OpenAI, OpenAIError
from fastapi import HTTPException

from assistant.application.table_store import TableService

from typing import Dict, Any


FUNCTIONS = [
  {
    "name": "merge_tables",
    "description": "Объединить две таблицы по колонкам",
    "parameters": {
      "type":"object",
      "properties":{
        "table1_id":{"type":"string"},
        "table2_id":{"type":"string"},
        "on":{"type":"array","items":{"type":"string"}},
        "how":{"type":"string","enum":["inner","left","right","outer"],"default":"inner"}
      },
      "required":["table1_id","table2_id","on"]
    }
  },
  {
    "name": "rename_column",
    "description": "Переименовать колонку",
    "parameters":{
      "type":"object",
      "properties":{
        "table_id":{"type":"string"},
        "old_name":{"type":"string"},
        "new_name":{"type":"string"}
      },
      "required":["table_id","old_name","new_name"]
    }
  },
  {
    "name": "convert_currency",
    "description": "Перевести валютный столбец в USD",
    "parameters":{
      "type":"object",
      "properties":{
        "table_id":{"type":"string"},
        "column":{"type":"string"},
        "exchange_rate":{"type":"number"}
      },
      "required":["table_id","column","exchange_rate"]
    }
  },
  {
    "name": "show_table",
    "description": "Показать первые N строк",
    "parameters":{
      "type":"object",
      "properties":{
        "table_id":{"type":"string"},
        "n_rows":{"type":"integer","default":5}
      },
      "required":["table_id"]
    }
  }
]

class QueryService:
    def __init__(self, vdb=None):
        from assistant.infrastructure.weaviate_client import WeaviateClient
        self.vdb = vdb or WeaviateClient()
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.ts  = TableService()



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
        context = "\n\n".join(text for _, text in hits)
        table_ids = [tid for tid,_ in hits]


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
            result = self._execute(name, args)
            return {"function":name, "arguments":args, "result":result}


        return {"reply": msg.content}

    def _execute(self, name:str, args:Dict[str,Any]) -> Any:

        df_store = self.ts
        if name == "merge_tables":
            df1 = df_store.get(args["table1_id"])
            df2 = df_store.get(args["table2_id"])
            merged = df1.merge(df2, on=args["on"], how=args.get("how","inner"))
            return {"table_id": df_store.upload( "merged.xlsx", merged.to_csv().encode() )}

        if name == "rename_column":
            df = df_store.get(args["table_id"])
            df2 = df.rename(columns={args["old_name"]:args["new_name"]})
            return {"table_id": df_store.upload("renamed.xlsx", df2.to_csv().encode())}

        if name == "convert_currency":
            df = df_store.get(args["table_id"])
            df[args["column"]] *= args["exchange_rate"]
            return {"table_id": df_store.upload("converted.csv", df.to_csv().encode())}

        if name == "show_table":
            df = df_store.get(args["table_id"])
            rows = df.head(args.get("n_rows",5)).to_dict(orient="records")
            return {"rows":rows}

        raise HTTPException(status_code=400, detail=f"Unknown function {name}")