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
* **Time** is time required for the operation in the machine

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
