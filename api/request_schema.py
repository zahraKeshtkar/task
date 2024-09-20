from marshmallow import Schema, fields

class UserSchema(Schema):
    national_number = fields.Integer(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class AuthenticateSchema(Schema):
    national_number = fields.Integer(required=True)
    password = fields.Str(required=True)


class SubmitTransactionSchema(Schema):
    currency_id = fields.Str(required=True)
    count = fields.Int(required=True)