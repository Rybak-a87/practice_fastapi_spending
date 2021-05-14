from fastapi import (
    APIRouter,
    Depends,
    File,    # достать Upload файл из тела запроса
    UploadFile,    # хранит в себе данные файла
    BackgroundTasks,  # для фоновых задач (для простых задач)
)
from fastapi.responses import StreamingResponse

from ..models.auth import UserModel
from ..services.auth import get_current_user
from ..services.reports import ReportsService


router = APIRouter(
    prefix="/reports"
)


@router.post("/import")
def import_csv(
        background_tasks: BackgroundTasks,    # для работы в фоне
        file: UploadFile = File(...),
        user: UserModel = Depends(get_current_user),
        reports_service: ReportsService = Depends()
):
    # # работа не в фоне
    # reports_service.import_csv(
    #     user_id=user.id,
    #     file=file.file
    # )

    # # работа в фоне
    background_tasks.add_task(
        reports_service.import_csv,
        user.id,
        file.file,
    )


@router.get("/export")
def export_csv(
        user: UserModel = Depends(get_current_user),
        reports_service: ReportsService = Depends()
):
    report = reports_service.export_csv(user_id=user.id)
    return StreamingResponse(    # асинхронно передает report клиенту
        report,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=report.csv"    # attachment - файл не откроется в браузере, а будет скачиватся
        }
    )
