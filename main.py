import threading as th
from time import time

import itertools as it

def Collatz(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def ParallelCollatz(N, thread_count):

    result = 0
    lock = th.Lock()
    numbers_iter = it.count(1)

    def worker():
        nonlocal result
        for _ in range(N // thread_count):
            current_num = numbers_iter.__next__()
            current_count = Collatz(current_num)
            with lock:
                result += current_count

    threads = []
    for i in range(thread_count):
        thread = th.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    avg_steps = result / N
    return avg_steps

if __name__ == "__main__":
    N = 20000
    num_threads = 6
    start_time = time()
    avg_steps = ParallelCollatz(N, num_threads)
    end_time = time()
    print(f"Середня кількість кроків: {avg_steps}")
    print(f"Час виконання: {(end_time - start_time):.4f} сек.")
