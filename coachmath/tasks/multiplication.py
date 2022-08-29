from random import randint as _randint, shuffle as _shuffle, sample as _sample

def basic_integer_multiplication(max_product: int,
                                 max_tasks: int = -1) -> dict:
    # Init
    tasks = []

    # Generate
    for xy in range(max_product, 1, -1):
        for x in range(2, max_product):
            if xy % x == 0:
                y = int(xy / x)

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
        _shuffle(self.tasks)
    else:
        tasks = _sample(self.tasks, self.max_tasks)

    return tasks