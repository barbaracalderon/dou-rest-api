from db import db


class SignatureModel(db.Model):
    __tablename__ = "signatures"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=False, nullable=True)
    journal_id = db.Column(
        db.Integer, db.ForeignKey("journals.id"), unique=False, nullable=False
    )

    journal = db.relationship("JournalModel", back_populates="signatures")
