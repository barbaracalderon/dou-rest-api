from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import BodyModel
from schemas import BodySchema
from resources.upper import Upper


blp = Blueprint("bodies", __name__, description="Operations on bodies.")


@blp.route("/body")
class BodyList(MethodView, Upper):
    @blp.response(200, BodySchema(many=True))
    def get(self):
        return BodyModel.query.all()

    @jwt_required()
    @blp.arguments(BodySchema)
    @blp.response(201, BodySchema)
    def post(self, body_data):
        transformed_body_data = self.upper_data(body_data)
        body = BodyModel(**transformed_body_data)
        try:
            db.session.add(body)
            db.session.commit()
        except IntegrityError:
            abort(500, message="It already exists a 'body' for this journal.")
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred while inserting the body into the database.",
            )
        return body


@blp.route("/body/<int:body_id>")
class Body(MethodView):
    @blp.response(200, BodySchema)
    def get(self, body_id):
        body = BodyModel.query.get_or_404(body_id)
        return body

    @jwt_required()
    def delete(self, body_id):
        body = BodyModel.query.get_or_404(body_id)
        db.session.delete(body)
        db.session.commit()
        return {"message": "Body deleted."}, 200
