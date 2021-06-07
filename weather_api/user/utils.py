from rest_framework_jwt.settings import api_settings


def generate_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    # jwt payload for user
    payload = jwt_payload_handler(user)
    # returning generated jwt token
    return jwt_encode_handler(payload)