import random
import math
import time
# Define the objective function which calculates the total time taken by a given schedule
def objective(schedule, t, c, T):
    total_time = 0
    penalty = 10000  # arbitrary high value to ensure deadlines are prioritized
    
    for machine_tasks in schedule:
        machine_time = 0  # The time taken by the current machine
        prev_product = None  # To track the previous task for cleaning time
        
    for task in machine_tasks:
        # Add cleaning time if there's a change in product
        if prev_product is not None and prev_product != task:
            cleaning_time = c[prev_product]  # Use the cleaning time for the previous product
            machine_time += cleaning_time
            total_time += cleaning_time
            
        # Check if adding the current task time will exceed the deadline
        if machine_time + t[task] > T[task]:
            total_time += penalty
        
        machine_time += t[task]
        total_time += t[task]
        
        prev_product = task
            
    return total_time

# Generate a neighboring solution by either swapping two tasks between two machines 
# or moving a task from one machine to another
def get_neighbor(schedule):
    new_schedule = [list(machine) for machine in schedule]  # Deep copy the current schedule
    machine1 = random.randint(0, len(schedule) - 1)  # Randomly select a machine
    machine2 = random.randint(0, len(schedule) - 1)  # Randomly select another machine
    
    # If the first chosen machine has no tasks, return the original schedule as it can't be modified
    if not new_schedule[machine1]:
        return schedule

    # Randomly select a task from the first machine
    task1_idx = random.randint(0, len(new_schedule[machine1]) - 1)
    task1 = new_schedule[machine1][task1_idx]

    # Swap tasks within the same machine
    if machine1 == machine2:
        # If there's only one task, we can't swap it with itself; so return the original schedule
        if len(new_schedule[machine2]) <= 1:
            return schedule
        # Randomly select another task from the same machine that's different from the first
        task2_idx = random.randint(0, len(new_schedule[machine2]) - 1)
        while task2_idx == task1_idx:
            task2_idx = random.randint(0, len(new_schedule[machine2]) - 1)
        # Swap the two tasks
        new_schedule[machine1][task1_idx], new_schedule[machine2][task2_idx] = new_schedule[machine2][task2_idx], new_schedule[machine1][task1_idx]
    else:
        # Swap tasks between different machines
        # If the second machine has tasks, swap with a random one
        if new_schedule[machine2]:
            task2_idx = random.randint(0, len(new_schedule[machine2]) - 1)
            new_schedule[machine1][task1_idx], new_schedule[machine2][task2_idx] = new_schedule[machine2][task2_idx], new_schedule[machine1][task1_idx]
        else:
            # If the second machine has no tasks, move the task from machine1 to machine2
            new_schedule[machine2].append(task1)
            new_schedule[machine1].pop(task1_idx)
    return new_schedule

# Simulated Annealing algorithm to find the optimal schedule
def simulated_annealing(t, c, T, n, initial_temperature, cooling_rate):
    # Start with a naive initial schedule: all tasks on the first machine
    schedule = [list(range(len(t)))] + [[] for _ in range(n-1)]
    # Calculate the time taken by this initial schedule
    current_cost = objective(schedule, t, c, T)
    temp = initial_temperature  # Set the starting temperature

    # Continue the search until the temperature falls below a threshold (1 in this case)
    while temp > 1:
        # Generate a neighboring solution
        neighbor = get_neighbor(schedule)
        # Calculate the cost of the neighboring solution
        neighbor_cost = objective(neighbor, t, c, T)

        # If the neighboring solution is better or there's a chance to move to a worse solution (based on current temperature),
        # then update the current solution and its cost
        if neighbor_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - neighbor_cost) / temp):
            schedule, current_cost = neighbor, neighbor_cost

        # Reduce the temperature for the next iteration
        temp *= cooling_rate
        
    # Return the found optimal schedule and its cost
    return schedule, current_cost

import time

def tests():
    test_cases = [
        {
            "name": "Small Test Case",
        "n": 2,
        "t": [5, 3, 4],
        "c": [1, 2, 3],  
        "T": [10, 14, 21],  
        "initial_temperature": 1000,
        "cooling_rate": 0.995,
    },
    {
        "name": "Medium Test Case",
        "n": 5,
        "t": [5, 3, 4, 6, 7, 3, 9],
        "c": [2, 2, 2, 3, 3, 1, 2],
        "T": [9, 13, 19, 28, 39, 43, 53], 
        "initial_temperature": 1000,
        "cooling_rate": 0.995,
    },
    {
        "name": "Large Test Case",
        "n": 10,
        "t": [4, 6, 7, 8, 9, 5, 3, 5, 8, 6, 7, 9, 3, 5, 4, 6, 7, 3, 4, 8],
        "c": [2, 3, 2, 3, 1, 2, 2, 3, 3, 1, 2, 3, 1, 2, 3, 2, 2, 3, 2, 1], 
        "T": [10, 14, 20, 24, 31, 36, 41, 45, 50, 56, 61, 66, 71, 76, 82, 86, 91, 96, 100, 105],  
        "initial_temperature": 1000,
        "cooling_rate": 0.995,
    }
    ]

    for test_case in test_cases:
        print(f"Running {test_case['name']}...")
        
        # Unpack test case values
        n = test_case["n"]
        t = test_case["t"]
        c = test_case["c"]
        T = test_case["T"]
        initial_temperature = test_case["initial_temperature"]
        cooling_rate = test_case["cooling_rate"]
        
        start_time = time.time()
        result, cost = simulated_annealing(t, c, T, n, initial_temperature, cooling_rate)
        end_time = time.time()
        
        print(f"Test Case {test_case['name']} Result:")
        print("Execution Time:", end_time - start_time, "seconds")
        print("Schedule:", result)
        print("Cost:", cost)
        print('-'*60)  # Separator line for better readability

tests()

