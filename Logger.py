import datetime

def logger_format(type, message):
    return f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{type}] {message}"

def log_info(message):
    print(logger_format("INFO", message))

def log_error(message):
    print(logger_format("ERROR", message))

def log_warning(message):
    print(logger_format("WARNING", message))

def log_debug(message):
    print(logger_format("DEBUG", message))