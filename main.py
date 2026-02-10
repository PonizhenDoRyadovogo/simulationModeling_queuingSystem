import math
import random
from typing import Tuple, Optional

INF = float("inf") #определяем "бесконечность"

def exp_time(rate: float, rng: random.Random) -> float:
    """
    Генерирует экспоненциально рапределенное время ожидания с интенсивностью rate с помощью метода обратных функций
    """
    if rate <= 0:
        raise ValueError("Интенсивность должна быть > 0")
    u = rng.random() # данная функция из библиотеки random генерирует равномерно распределенное число 0<=u<1
    return -math.log(1.0 - u) / rate

def simulation_mm11(lam: float, mu: float, end_time: float, seed: Optional[int]=None) -> Tuple[float, int, int]:
    """
    lam - интенсивность потока заявок
    mu - интенсивность обслуживания
    end_time - время моделирования
    seed - фиксируем для воспроизводимости (если None, то будет "случайно")
    """
    if end_time <= 0:
        raise ValueError("Время моделирования должно быть > 0")

    rng = random.Random(seed) # генератор случайных чисел

    t = 0.0 # текущее время моделирования
    busy = False # флаг занят ли прибор
    t_depart = INF # время ближайшего окончания обслуживания (INF, если уход не запланирован)

    arrived = 0 # всего пришло заявок
    lost = 0 # всего потеряно заявок

    t_arrival = exp_time(lam, rng) # планируем момент поступления первой заявки

    while True:
        t_event = min(t_arrival, t_depart) # ближайшее событие - либо поступление заявки, либо ее уход после окончания
        # обслуживания
        if t_event > end_time: # если ближайшее событие уже после окончания времени моделирования, то выходим из цикла
            break
        t = t_event # текущее время моделирования переносим к ближайшему событию

        if t_arrival <= t_depart: # если выполняется данное условие, то это означает, что поступила заявка
            arrived += 1 # фиксируем факт прихода
            if not busy: # если прибор не занят, то планируем окончание обслуживания
                busy = True
                t_depart = t + exp_time(mu, rng)
            else: # иначе прибор занят, тогда заявка теряется
                lost += 1
            t_arrival = t + exp_time(lam, rng) # планируем поступление следующей заявки
        else: # обслуживание заявки завершилось
            busy = False # прибор освобождается
            t_depart = INF

    p_hat = (lost / arrived) if arrived > 0 else 0.0 # оценка вероятности потери заявки
    return p_hat, arrived, lost

if __name__ == "__main__":
    lam = float(input("Введите lambda: ").strip())
    mu = float(input("Введите mu: ").strip())
    end_time = float(input("Введите время моделирования: ").strip())

    seed_in = input("Введите сид: ").strip()
    seed = int(seed_in) if seed_in else None

    p_hat, arrived, lost = simulation_mm11(lam, mu, end_time, seed)

    print(f"p_loss_hat = {p_hat:.5f}")