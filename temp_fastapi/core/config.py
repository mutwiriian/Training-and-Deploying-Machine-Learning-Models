from starlette.config import Config

config=Config(".env")

PATH_SVR: str = config('PATH_SVR')
PATH_RF: str = config('PATH_RF')
PATH_GBM: str = config('PATH_GBM')
