from starlette.config import Config

#set default values and constants in .env file
config=Config(".env")

PATH_SVR: str = config('PATH_SVR')
PATH_RF: str = config('PATH_RF')
PATH_GBM: str = config('PATH_GBM')
