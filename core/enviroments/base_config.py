class BaseConfig(object):
    PROPAGATE_EXCEPTIONS = True
    RESTX_MASK_SWAGGER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    },
    SWAGGER_UI_DOC_EXPANSION = 'none'
    SWAGGER_UI_REQUEST_DURATION = True

