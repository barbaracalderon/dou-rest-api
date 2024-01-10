from marshmallow import Schema, fields


class PlainMetadataSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    idOficio = fields.Str(required=True)
    pubName = fields.Str(required=True)
    artType = fields.Str(required=True)
    artClass = fields.Str(required=True)
    artSize = fields.Str(required=True)
    artNotes = fields.Str(required=True)
    numberPage = fields.Str(required=True)
    pdfPage = fields.Str(required=True)
    editionNumber = fields.Str(required=True)
    idMateria = fields.Str(required=True)


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    main = fields.Str(required=True)
    secondary = fields.Str(required=True)


class PlainBodySchema(Schema):
    id = fields.Int(dump_only=True)
    identifica = fields.Str(required=True)
    data = fields.Str(required=True)
    ementa = fields.Str(required=True)
    titulo = fields.Str(required=True)
    subtitulo = fields.Str(required=True)
    texto = fields.Str(required=True)


class PlainSignatureSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainJournalSchema(Schema):
    id = fields.Int(dump_only=True)
    article = fields.Str(required=True)
    date = fields.Str(required=True)


class MetadataSchema(PlainMetadataSchema):
    journal_id = fields.Int(required=True, load_only=True)
    journal = fields.Nested(PlainJournalSchema(), dump_only=True)


class CategorySchema(PlainCategorySchema):
    journal_id = fields.Int(required=True, load_only=True)
    journal = fields.Nested(PlainJournalSchema(), dump_only=True)


class BodySchema(PlainBodySchema):
    journal_id = fields.Int(required=True, load_only=True)
    journal = fields.Nested(PlainJournalSchema(), dump_only=True)


class SignatureSchema(PlainSignatureSchema):
    journal_id = fields.Int(required=True, load_only=True)
    journal = fields.Nested(PlainJournalSchema(), dump_only=True)


class JournalSchema(PlainJournalSchema):
    meta_data = fields.Nested(PlainMetadataSchema(), dump_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)
    body = fields.Nested(PlainBodySchema(), dump_only=True)
    signatures = fields.List(fields.Nested(PlainSignatureSchema()), dump_only=True)


class JournalSearchQueryArgs(Schema):
    start_date = fields.String()
    end_date = fields.String()
    article = fields.String()


class MetadataSearchQueryArgs(Schema):
    start_date = fields.String()
    end_date = fields.String()
    art_type = fields.String()


class CategorySearchQueryArgs(Schema):
    start_date = fields.String()
    end_date = fields.String()
    main = fields.String()


class SignatureSearchQueryArgs(Schema):
    start_date = fields.String()
    end_date = fields.String()
    name = fields.String()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True, load_only=True)
