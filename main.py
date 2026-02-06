import math
import random
from typing import Tuple, Optional

INF = float("inf")

def exp_time(rate: float, rng: random.Random) -> float:
    if rate <= 0:
        raise ValueError("rate must be > 0")
    u = rng.random()
    return -math.log(1.0 - u) / rate

def simulation_mm11(lam: float, mu: float, end_time: float, seed: Optional[int]=None) -> Tuple[float, int, int]:
    if end_time <= 0:
        raise ValueError("t_end must be > 0")

    rng = random.Random(seed)

    t = 0.0
    busy = False
    t_depart = INF

    arrived = 0
    lost = 0

    t_arrival = exp_time(lam, rng)

    while True:
        t_event = min(t_arrival, t_depart)
        if t_event > end_time:
            break
        t = t_event

        if t_arrival <= t_depart:
            arrived += 1
            if not busy:
                busy = True
                t_depart = t + exp_time(mu, rng)
            else:
                lost += 1
            t_arrival = t + exp_time(lam, rng)
        else:
            busy = False
            t_depart = INF

    p_hat = (lost / arrived) if arrived > 0 else 0.0
    return p_hat, arrived, lost

if __name__ == "__main__":
    lam = float(input("Enter lambda: ").strip())
    mu = float(input("Enter mu: ").strip())
    end_time = float(input("Enter end time: ").strip())

    seed_in = input("Enter seed: ").strip()
    seed = int(seed_in) if seed_in else None

    p_hat, arrived, lost = simulation_mm11(lam, mu, end_time, seed)

    print(f"p_loss_hat = {p_hat:.5f}")