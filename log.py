import functools
import inspect
import time, datetime


class Log:
    
    __file_name = ""
    __active = True
    
    def __init__(self, path="", active=True) -> None:
        Log.__active = active

        if Log.__active:
            now = datetime.datetime.now()
            
            Log.__file_name = now.strftime("%Y-%m-%d_%H-%M-%S")

            with open(f"{path}{Log.__file_name}", 'a+') as f:
                f.write(f"Created Log: {Log.__file_name}")
                f.write("\n")

    def log(message:str) -> None:
        if Log.__active:
            now = datetime.datetime.now()

            if Log.__file_name == "":
                raise RuntimeError("SetupError: Log not properly setup!")

            log_message = f"[{now.strftime('%Y.%m.%d-%H:%M:%S')}]{message}"

            with open(Log.__file_name, "a+") as f:
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

    def log_command(func):
        @functools.wraps(func)
        async def wrapped_func(**kwargs):
            try:
                Log.log(func.__name__, kwargs[0].user.id)
                await func(**kwargs)
            except Exception as e:
                Log.log(e)
        return wrapped_func
