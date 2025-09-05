from assistant.application.query_service import QueryService
from assistant.application.table_store import TableService

ts = TableService()
qs = QueryService(ts)
