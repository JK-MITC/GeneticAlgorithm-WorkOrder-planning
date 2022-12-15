import csv
import sys

class ProductionManager:
        
    def __init__(self, parts, machines):

        self.parts = list(set(parts))
        #self.parts = parts
        self.machines = list(set(machines))
        #self.machines = machines
    
    
    def createWorkPlan(self, work_order_list):
        self.work_orders = [{'id':id,'order':order} for id,order in enumerate(work_order_list)]
      
        self.work_plan = []
        
        for wo in self.work_orders:
            
            part_operations = [op for part in self.parts for op in part.operations if part.name == wo['order'].partname]
            
            for ind,op in enumerate(part_operations):
                
                dependencies = None if ind == 0 else part_operations[:ind]
                work_point = {'order_id': wo['id'],'order_size':wo['order'].order_size,'part_name':wo['order'].partname,'operation': op, 'dependencies':dependencies,'scheduled':False, 'starttime':0,'endtime':0}
                
                self.work_plan.append(work_point)
        #print(self.work_plan)
    def getPossibleMachinesForWorkOp(self, part, operation): 
         return [idx for idx,m in enumerate(self.machines) if m.canDoWork(part,operation)[0]]

      



class Machine:
    
    def __init__(self, name, parts, setuptime=60):
        self.name = name
        self.parts = parts
        self.next_time_slot = 0
        self.planned_work = []
        self.setup_time=setuptime

    def __hash__(self):
        # necessary for instances to behave sanely in dicts and sets.
        return hash(self.name)

    def __eq__(self, other):

        if not isinstance(other, Machine):
            # don't attempt to compare against unrelated types
            return NotImplemented
       
        return self.name == other.name

    def addWork(self,time):
        self.time_slot += time
    
    def canDoWork(self, part, operation):
        
        for p in self.parts:
            if p['partname'] == part:
                for op in p['operations']:
                    
                    if operation == op['opname']:
                        return True,op['optime']
                    
        return False,-1

    @staticmethod
    def machinesFromCSV(path):

        with open(path,encoding="utf-8-sig") as csv_file:

            reader = csv.reader(csv_file, delimiter=';')

            machines = {}

            for row in reader:
                
                machine_name = row[0]
                partname = row[1]
                opname = row[2]
                optime = int(row[3])

                if not machines.get(machine_name):
                    machines[machine_name] = []
                
                part_in_machine = next((p for p in machines[machine_name] if p['partname'] == partname),None)
         
                if not part_in_machine:

                    part_data = {'partname':partname,'operations':[{'opname':opname,'optime':optime}]}
                    
                    machines[machine_name].append(part_data)
                
                else:
                    part_in_machine['operations'].append({'opname': opname, 'optime':optime})

        machine_data = []

        for m in machines:
            machine_data.append(Machine(m,machines[m]))

        return machine_data  
         
class Part:
    
    def __init__(self, name, operations):
        self.name = name
        self.operations = operations

    def __hash__(self):
        # necessary for instances to behave sanely in dicts and sets.
        return hash(self.name)

    def __eq__(self, other):

        if not isinstance(other, Machine):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.name == other.name

    #Import parts with operations from CSV - First column is Part name, rest of columns are Operations
    @staticmethod
    def partsFromCSV(path):

        with open(path,encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            parts = []
            for row in reader:
                part = Part(row[0],[op for op in row[1:] if not op == ""])
                parts.append(part)

        return parts    

class WorkOrder:
    def __init__(self, part, size):
        self.partname = part
        self.order_size = size

    @staticmethod
    def workOrdersFromCSV(path):

        with open(path,encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            workorders = []
            for row in reader:
                order = WorkOrder(row[0],int(row[1]))
                workorders.append(order)

        return workorders
