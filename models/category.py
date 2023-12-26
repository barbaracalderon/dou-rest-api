from db import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.String(300), unique=False, nullable=True)
    secondary = db.Column(db.String(500), unique=False, nullable=True)
    journal_id = db.Column(
        db.Integer, db.ForeignKey("journals.id"), unique=True, nullable=False
    )

    journal = db.relationship("JournalModel", back_populates="category")
