from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import MetadataModel, JournalModel
from schemas import MetadataSchema, MetadataSearchQueryArgs
from sqlalchemy import and_
from datetime import date
from resources.upper import Upper

blp = Blueprint("metadatas", __name__, description="Operations on metadatas.")


@blp.route("/metadata")
class MetadataList(MethodView, Upper):
    @blp.arguments(MetadataSearchQueryArgs, location="query", required=False)
    @blp.response(200, MetadataSchema(many=True))
    def get(self, search_args):
        start_date = search_args.get("start_date", "").strip()
        end_date = search_args.get("end_date", "").strip()
        art_type = search_args.get("art_type", "").upper().strip()

        if art_type == "" and start_date == "" and end_date == "":
            return MetadataModel.query.all()

        elif art_type != "" and start_date == "" and end_date == "":
            return MetadataModel.query.filter(MetadataModel.artType == art_type).all()

        elif art_type == "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            journals_subquery = db.session.query(JournalModel.id).filter(
                JournalModel.date.between(formatted_start_date, formatted_end_date)
            )

            results = MetadataModel.query.filter(
                and_(MetadataModel.journal_id.in_(journals_subquery))
            ).all()
            return results

        elif art_type != "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            journals_subquery = db.session.query(JournalModel.id).filter(
                JournalModel.date.between(formatted_start_date, formatted_end_date)
            )

            results = MetadataModel.query.filter(
                and_(
                    MetadataModel.artType == art_type,
                    MetadataModel.journal_id.in_(journals_subquery),
                )
            ).all()
            return results

        else:
            return {"message": "Missing parameters."}, 404

    @jwt_required()
    @blp.arguments(MetadataSchema)
    @blp.response(201, MetadataSchema)
    def post(self, metadata_data):
        transformed_metadata_data = self.upper_data(metadata_data)
        metadata = MetadataModel(**transformed_metadata_data)
        try:
            db.session.add(metadata)
            db.session.commit()
        except IntegrityError:
            abort(500, message="It already exists a 'metadata' for this journal.")
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred while inserting the metadata into the database.",
            )
        return metadata


@blp.route("/metadata/<int:metadata_id>")
class Metadata(MethodView):
    @blp.response(200, MetadataSchema)
    def get(self, metadata_id):
        metadata = MetadataModel.query.get_or_404(metadata_id)
        return metadata

    @jwt_required()
    def delete(self, metadata_id):
        metadata = MetadataModel.query.get_or_404(metadata_id)
        db.session.delete(metadata)
        db.session.commit()
        return {"message": "Metadata deleted."}, 200
