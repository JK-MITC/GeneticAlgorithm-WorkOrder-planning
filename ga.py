from turtle import delay
import pygad as ga
from production import Part,Machine,WorkOrder, ProductionManager
import random
import numpy as np
import SchedulePlot as sp


#Part with it's operations
parts = [
    Part('Part1',['Op1','Op2']),
    Part('Part2',['Op1','Op2']),
    Part('Part3',['Op1']),
    Part('Part4',['Op1','Op2','Op3','Op4','Op5']),
    Part('Part5',['Op1','Op2','Op3'])
    ]

#Machines that can do the work with operation time in minutes
machines = [
    Machine('Machine0', [
                        {'partname': 'Part1','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':10}]},
                        {'partname': 'Part2','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':10}]},
                        {'partname': 'Part3','operations':[{'opname':'Op1','optime':10}]},
                        {'partname': 'Part4','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':15},{'opname':'Op3','optime':20},{'opname':'Op4','optime':15},{'opname':'Op5','optime':15}]},
                        {'partname': 'Part5','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':10},{'opname':'Op3','optime':10}]}
                        ]),
    
    Machine('Machine1', [
                        {'partname': 'Part1','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':10}]},
                        {'partname': 'Part2','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':10}]},
                        {'partname': 'Part3','operations':[{'opname':'Op1','optime':10}]},
                        #{'partname': 'Part4','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':15},{'opname':'Op3','optime':20},{'opname':'Op4','optime':15},{'opname':'Op5','optime':15}]},
                        {'partname': 'Part5','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':20},{'opname':'Op3','optime':10}]}
                        ]),
    
    Machine('Machine2', [
                        {'partname': 'Part1','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':20}]},
                        {'partname': 'Part2','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':20}]},
                        #{'partname': 'Part3','operations':[{'opname':'Op1','optime':10}]},
                        {'partname': 'Part4','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':15},{'opname':'Op3','optime':20},{'opname':'Op4','optime':15},{'opname':'Op5','optime':15}]},
                        {'partname': 'Part5','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':20},{'opname':'Op3','optime':10}]}
                        ]),

    Machine('Machine3', [
                        {'partname': 'Part1','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':20}]},
                        {'partname': 'Part2','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':30}]},
                        {'partname': 'Part3','operations':[{'opname':'Op1','optime':20}]},
                        {'partname': 'Part4','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':15},{'opname':'Op3','optime':20},{'opname':'Op4','optime':15},{'opname':'Op5','optime':15}]},
                        {'partname': 'Part5','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':10},{'opname':'Op3','optime':10}]}
                        ]),

    Machine('Machine4', [
                        {'partname': 'Part1','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':20}]},
                        #{'partname': 'Part2','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':10}]},
                        {'partname': 'Part3','operations':[{'opname':'Op1','optime':10}]},
                        {'partname': 'Part4','operations':[{'opname':'Op1','optime':10},{'opname':'Op2','optime':15},{'opname':'Op3','optime':20},{'opname':'Op4','optime':15},{'opname':'Op5','optime':15}]},
                        {'partname': 'Part5','operations':[{'opname':'Op1','optime':20},{'opname':'Op2','optime':15},{'opname':'Op3','optime':15}]}
                        ]),
                         
    ]

#Work orders with Part and amount of parts to produce
work_orders = [WorkOrder('Part4',100),WorkOrder('Part2',150),
                WorkOrder('Part3',10),WorkOrder('Part3',20),
                WorkOrder('Part1',100),WorkOrder('Part2',100),
                WorkOrder('Part1',200),WorkOrder('Part5',50),
                WorkOrder('Part4',10),WorkOrder('Part3',10),
                WorkOrder('Part5',150),WorkOrder('Part2',250)]

prod_manager = ProductionManager(parts,machines)

prod_manager.createWorkPlan(work_orders)


#print(work_operations)
def scheduleFromSolution(solution):
    
    machine_selection = solution[:len(prod_manager.work_plan)]
    job_schedule = solution[len(prod_manager.work_plan):]
    #print('Machine: ', machine_selection)
    #print('Job schedule: ',job_schedule)
    
    workplan = [item.copy() for item in prod_manager.work_plan]
    
    makespan = float('-inf')
    
    #Get machines for current work operations
    machine_schedule = {}    
    for machine in machine_selection:

        machine_schedule[prod_manager.machines[machine].name] = []
    
    #Schedule job operations in machines    
    for job in job_schedule:
               
        work_points = [(idx,x) for idx,x in enumerate(workplan) if x['order_id'] == job and x['scheduled'] == False]
        
        current_work_point = work_points[0]
        
        selected_machine_for_op = prod_manager.machines[machine_selection[current_work_point[0]]]
        
        #Get process time for operation on the selected machine
        for part in selected_machine_for_op.parts:
            
            if part['partname'] == current_work_point[1]['part_name']:
                for operation in part['operations']:
                    if operation['opname'] == current_work_point[1]['operation']:
                        
                        op_work_time = operation['optime']
                        
                        dependency_offset = 0
                        
                        #Check scheduled dependencies
                        dependent_ops = current_work_point[1]['dependencies'] 
                        if dependent_ops:
                            for wo in workplan:
                                
                                if wo['order_id'] == current_work_point[1]['order_id'] and wo['operation'] == dependent_ops[-1]:
                                    
                                    if wo['scheduled'] == True:
                                        
                                        dependency_offset = wo['endtime']
                                        #print('Dependency found!',wo, wo['endtime'])    
                            
                                                                       
                        scheduled_machine_ops = len(machine_schedule[selected_machine_for_op.name])
                        
                        #First job scheduled in machine
                        if scheduled_machine_ops == 0:
                            
                            current_work_point[1]['starttime'] = 0 + dependency_offset
                            current_work_point[1]['endtime'] = (op_work_time * current_work_point[1]['order_size']) + dependency_offset
                        #Jobs previously scheduled, get time from last job    
                        else:
                            last_op = machine_schedule[selected_machine_for_op.name][-1]

                            #Setup time needed?
                            if last_op['part_name'] != current_work_point[1]['part_name'] or last_op['operation'] != current_work_point[1]['operation']:
                                setup_operation = {'order_id':'setup','part_name':'setup','operation':'setup','starttime':last_op['endtime'],'endtime':last_op['endtime']+selected_machine_for_op.setup_time}
                                machine_schedule[selected_machine_for_op.name].append(setup_operation)
                                last_op = setup_operation

                            if last_op['endtime'] >= dependency_offset:
                                current_work_point[1]['starttime'] = last_op['endtime']
                                current_work_point[1]['endtime'] = last_op['endtime'] + (op_work_time * current_work_point[1]['order_size'])
                            else:
                                current_work_point[1]['starttime'] = dependency_offset
                                current_work_point[1]['endtime'] = dependency_offset + (op_work_time * current_work_point[1]['order_size'])
                        
                        makespan = max(makespan,current_work_point[1]['endtime'])
                        
                        #Schedule work operation    
                        machine_schedule[selected_machine_for_op.name].append(current_work_point[1])
                        current_work_point[1]['scheduled'] = True
        
    return (makespan,machine_schedule)

def create_initial_population(size):
    print('Creating initial population of size %d...' % size)
    population = []
    
    #Size of population
    for i in range(size):
        
        #Chromosome Two parts each of length = job operations
        #First part: Machine selection for job operations
        #Second part: Job operation order
        chromo_part1 = []
        chromo_part2 = []
        
        #Create copy of workoperations to pick from
        remaining_work_operations = [wo.copy() for wo in prod_manager.work_plan]
        
        #Iterate all job operations
        for index,op in enumerate(prod_manager.work_plan):
            
            #Populate first part(machine selection)
            #Get all compatible machines for this job operation
            possible_machines = prod_manager.getPossibleMachinesForWorkOp(op['part_name'], op['operation'])
            
            #print('Possible machines for part: '+op['part_name'] +' op: ' +op['operation'] +' -- ',possible_machines)
            
            gene = random.choice(possible_machines)
            
            chromo_part1.append(gene)
            
            #Populate second part(Job operation order)
            work_op_indx = random.randrange(0,len(remaining_work_operations))
            work_op_for_schedule = remaining_work_operations.pop(work_op_indx)
                           
            chromo_part2.append(work_op_for_schedule['order_id'])
            
            full_cromo = chromo_part1+chromo_part2
            
        #print(full_cromo)
        #print('--------------')    
        population.append(full_cromo)   
        
    return np.array(population)
    
def fitness_function(solution, index):
    
    makespan = scheduleFromSolution(solution)[0]/10000
    #return -makespan
    return 1.0/makespan



def crossover_func(parents, offspring_size, ga_instance):

    #Produce new offspring dependent on population size and how many parents to keep
    offspring = []
    gene_length = len(prod_manager.work_plan)
    idx = 0

    #Select part of chromosome to crossover: 0=Machine, 1=Schedule
    global crossover_part
    while len(offspring) != offspring_size[0]:

        #Pick the parents
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

        #Cross the Machine selection part (First half of chromosome)
        if crossover_part == 0:
            #random_split_point = np.random.choice(range(gene_length))         
            #parent1[random_split_point:gene_length] = parent2[random_split_point:gene_length]

            #pick amount of indices to cross
            selected_amount = gene_length*0.3
            picks = np.random.choice(range(gene_length),int(selected_amount))
            parent1[picks] = parent2[picks]
        #Cross Operation schedule selection part (Cannot be simply cut and swapped, must match the work operations available)        
        #PPX crossover
        else:
            p1_schedule = list(parent1[gene_length:])
            p2_schedule = list(parent2[gene_length:])
            parents_schedule = [p1_schedule,p2_schedule]
            
            #Vector of 0-1:s to select which parent to get next gene from
            random_selection_vector = np.random.randint(2,size=gene_length)

            #The new schedule
            schedule = np.zeros(gene_length,dtype=np.int32)

            #Iterate all genes
            for idx,i in enumerate(random_selection_vector):
                
                #Select the gene next in line from selected parent
                #Add gene to schedule
                schedule[idx] = parents_schedule[i][0]

                #Remove the occurence from both parents
                parents_schedule[i].remove(schedule[idx])
                parents_schedule[int(not i)].remove(schedule[idx])
        
            #Assemble the full chromosome(machine+schedule)
            parent1[gene_length:] = schedule
        offspring.append(parent1)

        idx += 1

    return np.array(offspring)

def mutation_func(offspring, ga_instance):
    
    #Value to select mutation type (50-50 chance) | >=0.5 Mutate Schedule order | <0.5 Mutate Machine selection
    mutation_type = random.random()
    gene_length = len(prod_manager.work_plan)
    
    #Mutate the schedule part
    if mutation_type >= 0.5:
     
        #Swap two genes in Work Operation part    
        #Pick first index
        idx1 = random.randint(gene_length, (gene_length*2)-1)
        idx2 = idx1
        
        #Make sure second index is not same as first index
        while idx1 == idx2:
            idx2 = random.randint(gene_length, (gene_length*2)-1)
        
        #Swap values at indices
        offspring[:,[idx1, idx2]] = offspring[:,[idx2, idx1]]

    #Mutate the machine select part - swap to another capable machine
    else:
        idx = random.randint(0, (gene_length)-1)
        op = prod_manager.work_plan[idx]
        possible_machines = prod_manager.getPossibleMachinesForWorkOp(op['part_name'], op['operation'])

        selected_machine = random.choice(possible_machines)
        offspring[:,[idx]] = selected_machine

    return offspring

def on_generation(ga_instance):
    solution,best_fitness,best_index = ga_instance.best_solution()
    global previous_best_solution,crossover_swap_thresh,crossover_part

    if best_fitness > previous_best_solution[0]:
        previous_best_solution = best_fitness,ga_instance.generations_completed
        makespan,schedule = scheduleFromSolution(solution=solution) 
        sp.plotUpdatedSchedule(makespan=makespan,schedule=schedule)
    gens_since_best = ga_instance.generations_completed - previous_best_solution[1]

    if gens_since_best != 0 and gens_since_best % crossover_swap_thresh == 0:
        crossover_part = int(not crossover_part)
    print("| Generation: %d | Best fitness: %0.4f | Generations since best: %d |" % (ga_instance.generations_completed, best_fitness, gens_since_best), end='\r')

    
#Used to know when to swap the part that is crossed over
#If no change after 'crossover_swap_thres' then move to next part to crossover(Machine vs Schedule)
previous_best_solution = (-1,0)
crossover_swap_thresh = 150
crossover_part = 0

population_size = 100
num_generations = 10000
num_parents_mating = 20
gene_type = (int)
num_genes = len(prod_manager.work_plan)*2
parent_selection_type = 'sss'
keep_parents = 5
mutation_percent_genes = 20
stop_criterias = ['saturate_500']
population = create_initial_population(population_size)

sp.showPlot()

ga_instance = ga.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       gene_type=gene_type,
                       num_genes=num_genes,
                       initial_population=population,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_func,
                       mutation_type=mutation_func,
                       mutation_percent_genes=mutation_percent_genes,
                       on_generation=on_generation,
                       stop_criteria=stop_criterias)

ga_instance.run()

ga_instance.plot_fitness(title='Fitness vs Generation')

sp.keepPlot()
makespan,machine_schedule = scheduleFromSolution(ga_instance.best_solution()[0])

#sp.plotSchedule(makespan,machine_schedule)