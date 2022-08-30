from random import randint as _randint, shuffle as _shuffle, sample as _sample

def basic_integer_division(dividend_max: int,
                           divisor_max: int = -1,
                           max_tasks: int = -1) -> dict:
    # Init
    tasks = []

    # Generate
    for x in range(dividend_max, 1, -1):
        for y in range(2, dividend_max+1):
            if x % y == 0:
                xy = int(x / y)

                # Limit divisor
                if (divisor_max > 0 and y > divisor_max):
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
