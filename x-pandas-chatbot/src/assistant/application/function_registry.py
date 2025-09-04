#src/assistant/application/function_registry.py

FUNCTIONS = [
    {
        "name": "merge_tables",
        "description": "Merge two tables by columns",
        "parameters": {
            "type": "object",
            "properties": {
                "table1_id": {"type": "string"},
                "table2_id": {"type": "string"},
                "on": {"type": "array", "items": {"type": "string"}},
                "how": {"type": "string", "enum": ["inner", "left", "right", "outer"], "default": "inner"}
            },
            "required": ["table1_id", "table2_id", "on"]
        }
    },
    {
        "name": "rename_column",
        "description": "Rename a column in a table",
        "parameters": {
            "type": "object",
            "properties": {
                "table_id": {"type": "string"},
                "old_name": {"type": "string"},
                "new_name": {"type": "string"}
            },
            "required": ["table_id", "old_name", "new_name"]
        }
    },
    {
        "name": "convert_currency",
        "description": "Convert a currency column to USD",
        "parameters": {
            "type": "object",
            "properties": {
                "table_id": {"type": "string"},
                "column": {"type": "string"},
                "exchange_rate": {"type": "number"}
            },
            "required": ["table_id", "column", "exchange_rate"]
        }
    },
    {
        "name": "show_table",
        "description": "Show the first N rows of a table",
        "parameters": {
            "type": "object",
            "properties": {
                "table_id": {"type": "string"},
                "n_rows": {"type": "integer", "default": 5}
            },
            "required": ["table_id"]
        }
    }
]
