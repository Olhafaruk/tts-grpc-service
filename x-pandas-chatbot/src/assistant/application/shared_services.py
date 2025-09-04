from assistant.application.table_store import TableService
from assistant.application.query_service import QueryService

ts = TableService()
qs = QueryService(ts)
