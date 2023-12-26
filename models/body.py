from db import db


class BodyModel(db.Model):
    __tablename__ = "bodies"

    id = db.Column(db.Integer, primary_key=True)
    identifica = db.Column(db.String(500), unique=False, nullable=True)
    data = db.Column(db.String(10), unique=False, nullable=True)
    ementa = db.Column(db.String(500), unique=False, nullable=True)
    titulo = db.Column(db.String(500), unique=False, nullable=True)
    subtitulo = db.Column(db.String(500), unique=False, nullable=True)
    texto = db.Column(db.String(15000), unique=False, nullable=True)
    journal_id = db.Column(
        db.Integer, db.ForeignKey("journals.id"), unique=True, nullable=False
    )

    journal = db.relationship("JournalModel", back_populates="body")
