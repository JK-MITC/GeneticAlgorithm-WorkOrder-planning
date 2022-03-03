from cProfile import label
import matplotlib.pyplot as plt
import random

def plotSchedule(makespan,schedule):

    #print(schedule)

    bar_height = 3.0
    bar_margin = 2.0
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    
    hours = makespan/60.0
    title = "Work order - Lead Time %.1f hours" % hours
    gnt.set_title(title)
    
    # Setting Y-axis limits
    gnt.set_ylim(0, ((bar_margin + bar_height)*len(schedule))+bar_margin)

    # Setting X-axis limits
    gnt.set_xlim(0, makespan/60.0)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time (Hours)')
    gnt.set_ylabel('Machine')
    #ylm = ((bar_margin+bar_height)*len(schedule)+bar_margin)/(len(schedule)+1)
    ylm = gnt.get_ylim()[1]/(len(schedule)+1)
    yticks = [(x+1)*ylm for x in range(len(schedule))]
    #yticks = [(x*bar_height)+(bar_height/2)+bar_margin for x in range(len(schedule))]
    # Setting ticks on y-axis
    gnt.set_yticks(yticks)
    # Labelling tickes of y-axis
    gnt.set_yticklabels(schedule)

    # Setting graph attribute
    #gnt.grid(True)
    work_order_color = {}

    def legend_without_duplicate_labels(ax):
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        return zip(*unique)

    for idx,sched in enumerate(schedule):
        
        for item in schedule[sched]:
            if item['order_id'] not in work_order_color.keys():
                work_order_color[item['order_id']] = (random.uniform(0.0, 1.0),random.uniform(0.0, 1.0),random.uniform(0.0, 1.0),1.0)
            y_bar_pos = yticks[idx]-(bar_height/2.0)

            #In Hours
            starttime = item['starttime']/60.0
            endtime = item['endtime'] /60.0
            duration = (item['endtime']-item['starttime'])/60.0
            label = 'Machine setup' if item['order_id'] == 'setup' else 'Order '+str(item['order_id'])
            #gnt.broken_barh([(item['starttime']/60.0,(item['endtime']-item['starttime'])/60.0)],(y_bar_pos,bar_height),facecolors=(work_order_color[item['order_id']]),edgecolor='black', label='Order '+str(item['order_id']))
            gnt.broken_barh([(starttime,duration)],(y_bar_pos,bar_height),facecolors=(work_order_color[item['order_id']]),edgecolor='black', label=label)
            if duration > 100:
                gnt.text(x=(starttime+duration/2), 
                        y=yticks[idx],
                        s=item['part_name'] + "-" + item['operation'], 
                        ha='center', 
                        va='center',
                        color='black',
                    )

    fig.set_figwidth(gnt.get_figure().get_figwidth()+10)
    
    plt.legend(*(legend_without_duplicate_labels(gnt)),loc='center left', bbox_to_anchor=(1,0.5))
    
    plt.show()
