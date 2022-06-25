import functools
import datetime


class Log:
    
    __file_name = ""
    __active = True
    
    def __init__(self, dir="", active=True) -> None:
        Log.__active = active

        if Log.__active:
            now = datetime.datetime.now()
            
            Log.__file_name = dir + "/" + now.strftime("%Y-%m-%d_%H-%M-%S")

            with open(f"{Log.__file_name}", 'a+') as f:
                f.write(f"Created Log: {Log.__file_name}")
                f.write("\n")

    def log(message:str) -> None:
        if Log.__active:
            now = datetime.datetime.now()

            if Log.__file_name == "":
                raise RuntimeError("SetupError: Log not properly setup!")

            log_message = f"[{now.strftime('%Y.%m.%d-%H:%M:%S')}]{message}"

            with open(f"{Log.__file_name}", "a+") as f:
                f.write(log_message)
                f.write("\n")

    def log_func(func):
        @functools.wraps(func)
        def wrapped_func(**kwargs):
            try:
                Log.log(func.__name__)
                return func(**kwargs)
            except Exception as e:
                Log.log(e)
        return wrapped_func
