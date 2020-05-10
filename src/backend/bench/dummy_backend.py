import random

from backend.main import Backend

backend = Backend()
backend.kpro.status = True
backend.kpro.version = 4

while True:
    backend.kpro.data0 = [random.randint(0, 255) for _ in range(38)]
    backend.kpro.data1 = [random.randint(0, 255) for _ in range(7)]
    backend.kpro.data3 = [random.randint(0, 255) for _ in range(100)]
    backend.kpro.data4 = [random.randint(0, 255) for _ in range(18)]
    backend.kpro.data5 = [random.randint(0, 255) for _ in range(20)]
