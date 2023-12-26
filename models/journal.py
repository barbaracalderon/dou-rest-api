from db import db


class JournalModel(db.Model):
    __tablename__ = "journals"

    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(20), unique=False, nullable=False)
    date = db.Column(db.Date, unique=False, nullable=False)

    meta_data = db.relationship(
        "MetadataModel", uselist=False, back_populates="journal", cascade="all, delete"
    )
    category = db.relationship(
        "CategoryModel", uselist=False, back_populates="journal", cascade="all, delete"
    )
    body = db.relationship(
        "BodyModel", uselist=False, back_populates="journal", cascade="all, delete"
    )
    signatures = db.relationship(
        "SignatureModel",
        back_populates="journal",
        lazy="dynamic",
        cascade="all, delete",
    )
