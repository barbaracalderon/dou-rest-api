from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import SignatureModel, JournalModel
from schemas import SignatureSchema, SignatureSearchQueryArgs
from sqlalchemy import and_
from datetime import date
from resources.upper import Upper

blp = Blueprint("signatures", __name__, description="Operations on signatures.")


@blp.route("/signature")
class SignatureList(MethodView, Upper):
    @blp.arguments(SignatureSearchQueryArgs, location="query", required=False)
    @blp.response(200, SignatureSchema(many=True))
    def get(self, search_args):
        start_date = search_args.get("start_date", "").strip()
        end_date = search_args.get("end_date", "").strip()
        name = search_args.get("name", "").upper().strip()

        if name == "" and start_date == "" and end_date == "":
            return SignatureModel.query.all()

        elif name != "" and start_date == "" and end_date == "":
            return SignatureModel.query.filter(SignatureModel.name == name).all()

        elif name == "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            journals_subquery = db.session.query(JournalModel.id).filter(
                JournalModel.date.between(formatted_start_date, formatted_end_date)
            )

            results = SignatureModel.query.filter(
                and_(SignatureModel.journal_id.in_(journals_subquery))
            ).all()
            return results

        elif name != "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            journals_subquery = db.session.query(JournalModel.id).filter(
                JournalModel.date.between(formatted_start_date, formatted_end_date)
            )

            results = SignatureModel.query.filter(
                and_(
                    SignatureModel.name == name,
                    SignatureModel.journal_id.in_(journals_subquery),
                )
            ).all()
            return results

        else:
            return {"message": "Missing parameters."}, 404

    @jwt_required()
    @blp.arguments(SignatureSchema)
    @blp.response(201, SignatureSchema)
    def post(self, signature_data):
        transformed_signature_data = self.upper_data(signature_data)
        signature = SignatureModel(**transformed_signature_data)
        try:
            db.session.add(signature)
            db.session.commit()
        except IntegrityError:
            abort(500, message="It already exists a signature with that 'name'.")
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred while inserting the signature into the database.",
            )
        return signature


@blp.route("/signature/<int:signature_id>")
class Signature(MethodView):
    @blp.response(200, SignatureSchema)
    def get(self, signature_id):
        signature = SignatureModel.query.get_or_404(signature_id)
        return signature

    @jwt_required()
    def delete(self, signature_id):
        signature = SignatureModel.query.get_or_404(signature_id)
        db.session.delete(signature)
        db.session.commit()
        return {"message": "Signature deleted."}, 200


@blp.route("/journal/<int:journal_id>/signature")
class SignaturesInJournal(MethodView):
    @blp.response(200, SignatureSchema(many=True))
    def get(self, journal_id):
        journal = JournalModel.query.get_or_404(journal_id)
        return journal.signatures.all()

    @jwt_required()
    @blp.arguments(SignatureSchema)
    @blp.response(201, SignatureSchema)
    def post(self, signature_data, journal_id):
        signature = SignatureModel(**signature_data, journal_id=journal_id)
        try:
            db.session.add(signature)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return signature
