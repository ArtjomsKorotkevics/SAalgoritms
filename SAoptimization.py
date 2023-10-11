import random
import math
import time
# Definējam mērķa funkciju, kas aprēķina kopējo noteiktā grafika aizņemto laiku
def objective(schedule, t, c, T):
    total_time = 0
    penalty = 10000  # patvaļīgi liela vērtība, lai nodrošinātu termiņu prioritāti
    
    for machine_tasks in schedule:
        machine_time = 0  # Tekošās mašīnas aizņemtais laiks
        prev_product = None  # Lai izsekotu iepriekšējam tīrīšanas laikam
        
    for task in machine_tasks:
        # Pievienojam tīrīšanas laiku, ja notiek produkta izmaiņas
        if prev_product is not None and prev_product != task:
            cleaning_time = c[prev_product]  # Izmantojam iepriekšējā produkta tīrīšanas laiku
            machine_time += cleaning_time
            total_time += cleaning_time
            
        # Pārbaudam vai pašreizējā uzdevuma laika pievienošana nepārsniegs termiņu
        if machine_time + t[task] > T[task]:
            total_time += penalty
        
        machine_time += t[task]
        total_time += t[task]
        
        prev_product = task
            
    return total_time

# Ģenerējam blakus risinājumu, vai nu apmainot divus uzdevumus starp divām iekārtām
# vai uzdevuma pārvietošana no vienas mašīnas uz citu
def get_neighbor(schedule):
    new_schedule = [list(machine) for machine in schedule]  # Pašreizējā grafika kopēšana
    machine1 = random.randint(0, len(schedule) - 1)  # Nejauši izvēlieties mašīnu
    machine2 = random.randint(0, len(schedule) - 1)  # Nejauši izvēlieties citu mašīnu
    
    # Ja pirmajai izvēlētajai iekārtai nav uzdevumu, atgriezt sākotnējo grafiku, jo to nevar mainīt
    if not new_schedule[machine1]:
        return schedule

    # Nejauši atlasīt uzdevumu no pirmās mašīnas
    task1_idx = random.randint(0, len(new_schedule[machine1]) - 1)
    task1 = new_schedule[machine1][task1_idx]

    # Apmainīt uzdevumus tajā pašā mašīnā
    if machine1 == machine2:
        # Ja ir tikai viens uzdevums, mēs nevaram to aizstāt ar sevi; tāpēc atgriezt sākotnējo grafiku
        if len(new_schedule[machine2]) <= 1:
            return schedule
        # Nejauši atlasīt citu uzdevumu no tās pašas iekārtas, kas atšķiras no pirmā
        task2_idx = random.randint(0, len(new_schedule[machine2]) - 1)
        while task2_idx == task1_idx:
            task2_idx = random.randint(0, len(new_schedule[machine2]) - 1)
       # Apmainam divus uzdevumus
        new_schedule[machine1][task1_idx], new_schedule[machine2][task2_idx] = new_schedule[machine2][task2_idx], new_schedule[machine1][task1_idx]
    else:
        # Apmainam uzdevumus starp dažādām mašīnām
        # Ja otrajai mašīnai ir uzdevumi, nomainam to ar nejaušu
        if new_schedule[machine2]:
            task2_idx = random.randint(0, len(new_schedule[machine2]) - 1)
            new_schedule[machine1][task1_idx], new_schedule[machine2][task2_idx] = new_schedule[machine2][task2_idx], new_schedule[machine1][task1_idx]
        else:
            # Ja otrajai iekārtai nav uzdevumu, pārvietojam uzdevumu no mašīnas1 uz mašīnu2
            new_schedule[machine2].append(task1)
            new_schedule[machine1].pop(task1_idx)
    return new_schedule

# Simulated Annealing algoritms, lai atrastu optimālo grafiku
def simulated_annealing(t, c, T, n, initial_temperature, cooling_rate):
    # Sākam ar naivu sākotnējo grafiku: visi uzdevumi pirmajā mašīnā
    schedule = [list(range(len(t)))] + [[] for _ in range(n-1)]
    # Aprēķinam laiku, kas vajadzīgs šim sākotnējam grafikam
    current_cost = objective(schedule, t, c, T)
    temp = initial_temperature  # Iestatam sākuma temperatūru

    # Turpinam meklēšanu, līdz temperatūra nokrītas zem sliekšņa (šajā gadījumā 1)
    while temp > 1:
        # Ģenerējam blakus risinājumu
        neighbor = get_neighbor(schedule)
        # Aprēķinam blakus esošā risinājuma izmaksas
        neighbor_cost = objective(neighbor, t, c, T)

        # Ja blakus esošais risinājums ir labāks vai pastāv iespēja pāriet uz sliktāku risinājumu (pamatojoties uz pašreizējo temperatūru),
         # tad atjauninam pašreizējo risinājumu un tā izmaksas
        if neighbor_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - neighbor_cost) / temp):
            schedule, current_cost = neighbor, neighbor_cost

        # Samazinam temperatūru nākamajai iterācijai
        temp *= cooling_rate
        
    # Atgriezt atrasto optimālo grafiku un tā izmaksas
    return schedule, current_cost

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
        
        # Izpakojam testa gadījumu vērtības
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
        print('-'*60)  # Atdalīšanas līnija labākai lasāmībai

tests()

