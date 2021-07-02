import time
times = time.time()
local_time = time.localtime(times)

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",local_time)
