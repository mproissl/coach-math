from random import randint as _randint, shuffle as _shuffle, sample as _sample

def basic_integer_multiplication(result_max: int,
                                 multiplier_max: int = -1,
                                 max_tasks: int = -1) -> dict:
    # Init
    tasks = []

    # Generate
    for xy in range(result_max, 1, -1):
        for x in range(2, result_max):
            if xy % x == 0:
                y = int(xy / x)

                # Limit multiplier
                if (multiplier_max > 0 and y > multiplier_max):
                    continue
                
                # Exclude simple case
                if (x == 1 or y == 1):
                    continue

                # Random swap of x and y
                if _randint(0, 1) == 0:
                    x, y = y, x

                # Create task
                tasks.append({
                    "task": f"{x} x {y} =",
                    "result": xy
                })
            
    # Randomize
    if max_tasks < 0:
        _shuffle(tasks)
    else:
        tasks = _sample(tasks, max_tasks)

    return tasks
