# Genetic Algorithm for Orderplanning

## Requirements
* Python 3.7.3
* PyGAD 2.18.1

## Input CSV data examples (Do NOT include headers in file)
* Copy and edit the example CSV files from **/example input data/** to **/imports/**

### Part & operations (The parts that can be produced)
* Filename **input_parts.csv**
* First column **Part name**
* Add as many **Operations** as needed in following columns

|Part name|Operation|Operation|Operation|Operation|
|--------|-----|---|---|---|
|Part1   |Op1  |Op2|Op3|   |
|Part2   |Op1  |Op2|   |   |
|Part3   |Op1  |   |   |   |
|Part4   |Op1  |Op2|Op3|Op4|
|Part5   |Op1  |Op2|Op3|   |

### Machines/Assets (The assets that can produce Parts)
* Filename **input_machines.csv**
* **Part name & Operation name** must match a Part in the Parts input
* **Time** is the time required for the operation in the machine in minutes

|Name|Part name|Operation name|Time|
|--------|-----|---|---|
|Machine1|Part1|Op1|30 |
|Machine1|Part1|Op2|25 |
|Machine1|Part1|Op3|30 |
|Machine1|Part2|Op1|25 |
|Machine1|Part2|Op2|60 |
|Machine1|Part2|Op3|55 |
|Machine2|Part1|Op1|25 |
|Machine2|Part1|Op2|60 |
|Machine2|Part2|Op2|100|

### Work order list (The list of Parts that will be produced)
* Filename **input_workorders.csv**
* First column is the **Part name** to be produced
* **Amount** of parts to be produced

|Part name|Amount|
|--------|-----|
|Part1   |200  |
|Part2   |100  |
|Part2   |100  |
|Part3   |50   |
|Part1   |60   |
|Part4   |120  |
|Part4   |30   |
|Part1   |50   |
|Part5   |100  |

## Output schedule
* A schedule result file is output in the format **exports\schedule_export_{run_id}\_{total_time}.csv**

|Machine name|Order id|Order size|Part name|Operation|Dependencies         |Scheduled|Starttime|Endtime|
|------------|--------|----------|---------|---------|---------------------|---------|---------|-------|
|Machine2    |4       |60        |Part1    |Op1      |                     |True     |0        |1500   |
|Machine2    |0       |200       |Part1    |Op1      |                     |True     |1500     |6500   |
|Machine2    |7       |50        |Part1    |Op1      |                     |True     |6500     |7750   |
|Machine2    |setup   |setup     |setup    |setup    |                     |True     |7750     |7810   |
|Machine2    |7       |50        |Part1    |Op2      |['Op1']              |True     |7810     |10810  |
|Machine2    |setup   |setup     |setup    |setup    |                     |True     |10810    |10870  |
|Machine2    |2       |100       |Part2    |Op2      |['Op1']              |True     |10870    |20870  |
|Machine1    |2       |100       |Part2    |Op1      |                     |True     |0        |2500   |
|Machine1    |1       |100       |Part2    |Op1      |                     |True     |2500     |5000   |
|Machine1    |setup   |setup     |setup    |setup    |                     |True     |5000     |5060   |
|Machine1    |0       |200       |Part1    |Op2      |['Op1']              |True     |6500     |11500  |
|Machine1    |setup   |setup     |setup    |setup    |                     |True     |11500    |11560  |
|Machine1    |4       |60        |Part1    |Op3      |['Op1', 'Op2']       |True     |11560    |13360  |
|Machine1    |7       |50        |Part1    |Op3      |['Op1', 'Op2']       |True     |13360    |14860  |
|Machine1    |0       |200       |Part1    |Op3      |['Op1', 'Op2']       |True     |14860    |20860  |

## Run the application

To start the application, run the command: ```python ga.py --{optional arguments}```
#### Arguments
* --no_plot       (Do not show the plot, default **false**)
* --runs          (Number of runs, creates a separate schedule for every run, default **1**)
* --no_csv_export (Do not export a CSV file, default **false**)
