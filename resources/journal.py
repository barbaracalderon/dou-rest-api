from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from db import db
from models import JournalModel
from schemas import JournalSchema, JournalSearchQueryArgs
from datetime import date


blp = Blueprint("journals", __name__, description="Operations on journals.")


@blp.route("/journal")
class JournalList(MethodView):
    @blp.arguments(JournalSearchQueryArgs, location="query", required=False)
    @blp.response(200, JournalSchema(many=True))
    def get(self, search_args):
        start_date = search_args.get("start_date", "").strip()
        end_date = search_args.get("end_date", "").strip()
        article = search_args.get("article", "").strip()

        if start_date == "" and end_date == "" and article == "":
            return JournalModel.query.with_entities(JournalModel.id).all()

        elif article != "" and start_date == "" and end_date == "":
            return (
                JournalModel.query.filter_by(article=article)
                .with_entities(JournalModel.id)
                .all()
            )

        elif article == "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            results = (
                JournalModel.query.filter(
                    JournalModel.date.between(formatted_start_date, formatted_end_date)
                )
                .with_entities(JournalModel.id)
                .all()
            )
            return results

        elif article != "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            results = (
                JournalModel.query.filter(
                    JournalModel.date.between(formatted_start_date, formatted_end_date),
                    JournalModel.article == article,
                )
                .with_entities(JournalModel.id)
                .all()
            )

            return results

        else:
            return {"message": "Missing parameters."}, 404

    @jwt_required()
    @blp.arguments(JournalSchema)
    @blp.response(201, JournalSchema)
    def post(self, journal_data):
        transformed_journal_data = self.transform_journal_data(journal_data)
        journal = JournalModel(**transformed_journal_data)
        try:
            db.session.add(journal)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred while inserting the journal into the database.",
            )
        return journal

    def transform_journal_data(self, journal_data: dict) -> dict:
        fields_to_convert = ["article", "date"]
        for field in fields_to_convert:
            if field in journal_data:
                journal_data[field] = journal_data[field].upper().strip()

        if "date" in journal_data:
            day, month, year = map(int, journal_data["date"].split("/"))
            formatted_date = date(year, month, day)
            journal_data["date"] = formatted_date

        return journal_data


@blp.route("/journal/<int:journal_id>")
class Journal(MethodView):
    @blp.response(200, JournalSchema)
    def get(self, journal_id):
        journal = JournalModel.query.get_or_404(journal_id)
        return journal

    @jwt_required()
    def delete(self, journal_id):
        journal = JournalModel.query.get_or_404(journal_id)
        db.session.delete(journal)
        db.session.commit()
        return {"message": "Journal deleted."}, 200
