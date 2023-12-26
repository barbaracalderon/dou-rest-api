from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import CategoryModel, JournalModel
from schemas import CategorySchema, CategorySearchQueryArgs
from sqlalchemy import and_
from datetime import date
from resources.upper import Upper


blp = Blueprint("categories", __name__, description="Operations on categories.")


@blp.route("/category")
class CategoryList(MethodView, Upper):
    @blp.arguments(CategorySearchQueryArgs, location="query", required=False)
    @blp.response(200, CategorySchema(many=True))
    def get(self, search_args):
        start_date = search_args.get("start_date", "").strip()
        end_date = search_args.get("end_date", "").strip()
        main = search_args.get("main", "").upper().strip()

        if main == "" and start_date == "" and end_date == "":
            return CategoryModel.query.all()

        elif main != "" and start_date == "" and end_date == "":
            return CategoryModel.query.filter(CategoryModel.main == main).all()

        elif main == "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            journals_subquery = db.session.query(JournalModel.id).filter(
                JournalModel.date.between(formatted_start_date, formatted_end_date)
            )

            results = CategoryModel.query.filter(
                and_(CategoryModel.journal_id.in_(journals_subquery))
            ).all()
            return results

        elif main != "" and start_date != "" and end_date != "":
            start_day, start_month, start_year = map(int, start_date.split("/"))
            formatted_start_date = date(start_year, start_month, start_day)

            end_day, end_month, end_year = map(int, end_date.split("/"))
            formatted_end_date = date(end_year, end_month, end_day)

            journals_subquery = db.session.query(JournalModel.id).filter(
                JournalModel.date.between(formatted_start_date, formatted_end_date)
            )

            results = CategoryModel.query.filter(
                and_(
                    CategoryModel.main == main,
                    CategoryModel.journal_id.in_(journals_subquery),
                )
            ).all()
            return results

        else:
            return {"message": "Missing parameters."}, 404

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        transformed_category_data = self.upper_data(category_data)
        category = CategoryModel(**transformed_category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(500, message="It already exists a 'category' for this journal.")
        except SQLAlchemyError:
            abort(
                500,
                message="An error occured while inserting the category into the database.",
            )
        return category


@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @jwt_required()
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted."}, 200
