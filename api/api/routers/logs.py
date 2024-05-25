from api.models.log_entry import LogEntry, LogEntryCreateUpdate, LogEntryModel

from api.utils.crud import CRUDRouter

logs_router = CRUDRouter(
    model=LogEntry,
    create_model=LogEntryCreateUpdate,
    update_model=LogEntryCreateUpdate,
    sql_model=LogEntryModel,
    prefix="/logs"
)
