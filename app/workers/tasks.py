from app.celery_app import celery_app
from app.services.document_service import process_document
from app.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.document import DocumentStatus

sync_engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
)
SyncSession = sessionmaker(bind=sync_engine)

@celery_app.task
def process_document_task(document_id: int, file_path: str):
    with SyncSession() as db:
        from app.models.document import Document
        doc = db.get(Document, document_id)
        if not doc:
            return
        doc.status = DocumentStatus.processing
        db.commit()
        try:
            process_document(document_id, file_path)
            doc.status = DocumentStatus.ready
        except Exception as e:
            print(f"TASK ERROR: {e}")
            import traceback
            traceback.print_exc()
            doc.status = DocumentStatus.failed
        db.commit()