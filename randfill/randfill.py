from random import randbytes
import os
import time
import shutil
import hashlib

try:
    os.mkdir("./data")
except:
    pass


hashs = {}


def last10avg(key, data):
    global last10avg_data
    if not "last10avg_data" in globals():
        last10avg_data = dict()

    if not key in last10avg_data:
        last10avg_data[key] = []

    last10avg_data[key].append(data)
    last10avg_data[key] = last10avg_data[key][-10:]
    return(sum(last10avg_data[key]) / len(last10avg_data[key]))

def verify(curr):
    i = curr - 10
    if str(i) in hashs:
        m = hashlib.md5()
       
        with open(f"./data/{i // 100}/{i}.bin", "rb") as f:
            m.update(f.read())
        if m.hexdigest() != hashs[str(i)]:
            print(f"file not match! ./data/{i // 100}/{i}.bin")


i = 0
while True:
    try:
        os.mkdir(f"./data/{i // 100}")
    except:
        pass

    m = hashlib.md5()
    t = time.time_ns()
    with open(f"./data/{i // 100}/{i}.bin", "wb") as f:
        for j in range(2 ** 10):
            #f.write(randbytes(2**20))
            data = os.urandom(2**20)
            m.update(data)
            f.write(data)
        #f.flush()
        #os.fsync(f.fileno())

    hashs[str(i)] = m.hexdigest()


    t = (time.time_ns() - t) / 10 ** 9
    
    tr = time.time_ns() - 1

    
    verify(i)

    i += 1

    stat = shutil.disk_usage("./data")
    
    
    tr = (time.time_ns() - tr) / 10 ** 9
    s = 2**10 / t
    sr = 2**10 / tr

    r = 2 * stat.free / 2 ** 20 / ((s + sr)/2) / 60
    
    print(f"{last10avg('space', (stat.used / stat.total) * 100):.2f}% W:{last10avg('speed_w', s):.2f} MB/s R:{last10avg('speed_r', sr):.2f} MB/s {last10avg('time', r):.1f} min remain", end='\r')
