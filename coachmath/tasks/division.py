from random import randint as _randint, shuffle as _shuffle, sample as _sample

def basic_integer_division(max_dividend: int,
                           max_divisor: int = -1,
                           max_tasks: int = -1) -> dict:
    # Init
    tasks = []

    # Generate
    for x in range(max_dividend, 1, -1):
        for y in range(2, max_dividend+1):
            if x % y == 0:
                xy = int(x / y)

                # Limit divisor
                if y > max_divisor:
                    continue

                # Create task
                tasks.append({
                    "task": f"{x} / {y} =",
                    "result": xy
                })
            
    # Randomize
    if max_tasks < 0:
        _shuffle(tasks)
    else:
        tasks = _sample(tasks, max_tasks)

    return tasks
