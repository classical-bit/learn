from enum import Enum
from typing import Any


class CSVExportStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    SUCCESS = 3
    FAILURE = 4


RawCSVData = list[list[object]]
PreparedCSVData = list[list[str]]
CSVStatusResult = tuple[str, PreparedCSVData | str]

# Don't touch above this line

class UnknownStatusError(Exception):
    pass

def get_csv_status(status: CSVExportStatus, data: Any) -> CSVStatusResult:
    match status:
        case CSVExportStatus.PENDING:
            prepared_data = [[str(item) for item in row] for row in data]
            return ("Pending...", prepared_data)

        case CSVExportStatus.PROCESSING:
            csv_string = "\n".join([",".join(row) for row in data])
            return ("Processing...", csv_string)

        case CSVExportStatus.SUCCESS:
            return ("Sucess!", data)

        case CSVExportStatus.FAILURE:
            prepared_data = [[str(item) for item in row] for row in data]
            csv_string = "\n".join([",".join(row) for row in prepared_data])
            return ("Unknown error, retrying...", csv_string)

        case _:
            raise UnknownStatusError("unknown export status")
