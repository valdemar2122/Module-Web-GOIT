import time
from multiprocessing import Pool, cpu_count


def factorize_number(num):
    return [i for i in range(1, num + 1) if num % i == 0]


def factorize_sync(*numbers):
    results = []
    for num in numbers:
        factors = factorize_number(num)
        results.append(factors)
    return results


def factorize_parallel(*numbers):
    with Pool(processes=cpu_count()) as pool:
        result = pool.map_async(factorize_number, numbers)
        pool.close()
        pool.join()
        return result.get()


if __name__ == "__main__":
    # Вимірюємо час виконання паралельної версії
    start_time = time.time()
    result_parallel = factorize_parallel(128, 255, 99999, 10651060)
    end_time = time.time()
    print(result_parallel)

    execution_time_parallel = end_time - start_time
    print("Паралельний час виконання:", execution_time_parallel, "секунд")

    # Вимірюємо час виконання синхронної версії
    start_time = time.time()
    result_sync = factorize_sync(128, 255, 99999, 10651060)
    end_time = time.time()
    print(result_sync)

    execution_time_sync = end_time - start_time
    print("Синхронний час виконання:", execution_time_sync, "секунд")
