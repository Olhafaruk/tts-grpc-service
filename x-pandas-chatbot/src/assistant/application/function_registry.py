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
        "description": "Convert a specific amount from one currency to USD using a rate from a specific date",
        "parameters": {
            "type": "object",
             "properties": {
                "table_id": {"type": "string"},
                "currency": {"type": "string"},
                "amount": {"type": "number"},
                "date": {"type": "string", "format": "date"}
            },
         "required": ["table_id", "currency", "amount", "date"]
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
    },

    {
        "name": "filter_rows",
        "description": "Filter rows in a table by column value",
        "parameters": {
            "type": "object",
            "properties": {
                "table_id": {"type": "string"},
                "column": {"type": "string"},
                "value": {"type": "string"},
                "n_rows": {"type": "integer", "default": 5}
            },
            "required": ["table_id", "column", "value"]
        }
    },

    {
        "name": "scale_column_by_rate",
        "description": "Multiply all values in a numeric column by a given exchange rate",
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
        "name": "compare_rows",
        "description": "Compare exchange rates for two currencies on a specific date",
        "parameters": {
            "type": "object",
            "properties": {
                "table_id": {"type": "string"},
                "currency1": {"type": "string"},
                "currency2": {"type": "string"},
                "date": {"type": "string", "format": "date"}
            },
            "required": ["table_id", "currency1", "currency2", "date"]
        }
    },
    {
        "name": "aggregate_column",
        "description": "Aggregate values in a column using a specified method, optionally grouped by another column",
        "parameters": {
            "type": "object",
            "properties": {
                "table_id": {"type": "string"},
                "column": {"type": "string"},
                "agg": {
                    "type": "string",
                    "enum": ["mean", "sum", "max", "min"],
                    "default": "mean"
                },
                "group_by": {"type": "string"}
            },
            "required": ["table_id", "column"]
        }
    },
    {
        "name": "get_column_stats",
        "description": "Get basic statistics for a numeric column",
        "parameters": {
            "type": "object",
            "properties": {
             "table_id": {"type": "string"},
                "column": {"type": "string"}
            },
         "required": ["table_id", "column"]
        }
    },
    {
         "name": "list_columns",
        "description": "List all column names in a table",
        "parameters": {
            "type": "object",
            "properties": {
                "table_id": {"type": "string"}
            },
         "required": ["table_id"]
     }
    }

]
