import os
import csv
import json
import random
from flask import Flask, render_template, request, redirect, url_for
from production import Part, Machine, WorkOrder, ProductionManager
import numpy as np
import pygad as ga
from importlib import reload
import SchedulePlot as sp
import PySimpleGUI as sg  # Added import for PySimpleGUI

app = Flask(__name__)

# Load GA parameters from config file
with open('ga_config.json') as f:
    ga_config = json.load(f)
    ga_parameters = ga_config['ga_parameters']

# Initialize variables
prod_manager = None
previous_best_solution = (-1, 0)
crossover_swap_thresh = 150
crossover_part = 0
lead_time = float('inf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_ga', methods=['POST'])
def run_ga():
    global prod_manager, previous_best_solution, crossover_swap_thresh, crossover_part, lead_time

    # Get GA parameters from the form
    ga_parameters['population_size'] = int(request.form['population_size'])
    ga_parameters['generations'] = int(request.form['generations'])
    ga_parameters['parents_mating'] = int(request.form['parents_mating'])
    ga_parameters['keep_parents'] = int(request.form['keep_parents'])
    ga_parameters['mutation_percent_of_genes'] = int(request.form['mutation_percent_of_genes'])
    ga_parameters['saturation'] = int(request.form['saturation'])

    # Save updated GA parameters to config file
    with open('ga_config.json', 'w') as f:
        json.dump({'ga_parameters': ga_parameters}, f, indent=4)

    # Retrieve file paths from form
    machines_path = request.form['machines']
    parts_path = request.form['parts']
    workorders_path = request.form['workorders']

    # Load data from CSV files
    machines = Machine.machinesFromCSV(machines_path)
    parts = Part.partsFromCSV(parts_path)
    work_orders = WorkOrder.workOrdersFromCSV(workorders_path)

    # Create production manager and work plan
    prod_manager = ProductionManager(parts, machines)
    prod_manager.createWorkPlan(work_orders)

    # GA execution
    population_size = ga_parameters['population_size']
    num_generations = ga_parameters['generations']
    num_parents_mating = ga_parameters['parents_mating']
    gene_type = int
    num_genes = len(prod_manager.work_plan) * 2
    parent_selection_type = 'sss'
    keep_parents = ga_parameters['keep_parents']
    mutation_percent_genes = ga_parameters['mutation_percent_of_genes']
    stop_criterias = ['saturate_' + str(ga_parameters['saturation'])]
    population = create_initial_population(population_size)

    if not ga_parameters.get('no_plot', False):
        sp.showPlot()

    ga_instance = ga.GA(
        num_generations=num_generations,
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
        stop_criteria=stop_criterias,
        parallel_processing=["thread", os.cpu_count()]
    )

    ga_instance.run()

    if not ga_parameters.get('no_plot', False):
        ga_instance.plot_fitness(title='Fitness vs Generation')
        sp.keepPlot()

    makespan, machine_schedule = scheduleFromSolution(ga_instance.best_solution()[0])

    # CSV export requested
    if not ga_parameters.get('no_csv_export', False):
        file_path = f"exports/schedule_export_{random.randint(1, 100)}_{makespan}.csv"
        exportScheduleAsCSV(machine_schedule, path=file_path)

    # Reset the plot
    if not ga_parameters.get('runs', 1):
        reload(sp)

    return render_template('result.html', makespan=makespan, lead_time=lead_time)

# Add the 'submit' endpoint here
@app.route('/submit', methods=['POST'])
def submit():
    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
