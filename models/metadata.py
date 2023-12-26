from db import db


class MetadataModel(db.Model):
    __tablename__ = "metadatas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    idOficio = db.Column(db.String(200), unique=False, nullable=True)
    pubName = db.Column(db.String(200), unique=False, nullable=True)
    artType = db.Column(db.String(500), unique=False, nullable=True)
    artClass = db.Column(db.String(500), unique=False, nullable=True)
    artSize = db.Column(db.String(200), unique=False, nullable=True)
    artNotes = db.Column(db.String(300), unique=False, nullable=True)
    numberPage = db.Column(db.String(200), unique=False, nullable=True)
    pdfPage = db.Column(db.String(200), unique=False, nullable=True)
    editionNumber = db.Column(db.String(50), unique=False, nullable=True)
    idMateria = db.Column(db.String(50), unique=False, nullable=True)
    journal_id = db.Column(
        db.Integer, db.ForeignKey("journals.id"), unique=True, nullable=False
    )

    journal = db.relationship("JournalModel", back_populates="meta_data")
