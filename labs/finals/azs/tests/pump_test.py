import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.pump import Pump
from models.tank import Tank

pump = Pump(5, {"AI95": "AI95_2", "AI92": "AI92_1"})

tanks = {
    "AI95_2": Tank("AI95_2", "AI95", 20000, 12000, 1500, False),  # Отключена
    "AI92_1": Tank("AI92_1", "AI92", 20000,12000,  2000, True)
}

available = pump.get_available_fuels(tanks)
print(available)  # [("AI92", "AI92_1")]  - только АИ-92 доступна
