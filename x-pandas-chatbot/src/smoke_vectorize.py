from weaviate import Client
import pandas as pd
import uuid
from assistant.config import WEAVIATE_URL

client = Client(WEAVIATE_URL, startup_period=30)

# Гарантируем схему
schema = client.schema.get()
if "TableDoc" not in {c["class"] for c in schema.get("classes", [])}:
    client.schema.create_class({
        "class": "TableDoc",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {"name": "table_id", "dataType": ["string"]},
            {"name": "text",     "dataType": ["text"]}
        ]
    })
    print("✅ Schema created")

# Пишем объект
df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [30, 25]})
text = f"Test Table: cols={list(df.columns)} samples={df.head(3).to_dict()}"
tid = str(uuid.uuid4())
client.data_object.create(
    {"table_id": tid, "text": text},
    class_name="TableDoc",
    uuid=tid
)
print(f"✅ Object created: {tid}")

# Читаем и проверяем вектор
obj = client.data_object.get(tid, "TableDoc")
vec = obj.get("vector") or obj.get("_additional", {}).get("vector")
print("Vector length:", len(vec) if vec else 0)
