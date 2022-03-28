
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

class WorkOrder:
    def __init__(self, part, size):
        self.partname = part
        self.order_size = size

