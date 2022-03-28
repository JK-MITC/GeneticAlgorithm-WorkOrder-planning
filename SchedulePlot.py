from cProfile import label
import matplotlib.pyplot as plt
import random

from numpy import block



fig, gnt = plt.subplots()
fig_width = 0

def getColors():

    return {'setup':(0.4629979328756767, 0.21835054237240545, 0.3649058774274131, 1.0),0: (0.8465757999403946, 0.600695555461923, 0.760910722113421, 1.0), 1: (0.1294390186520718, 0.6160365105141384, 0.312136395945212, 1.0), 2: (0.5585032527641283, 0.256177165130733, 0.1772312048770222, 1.0), 3: (0.8320590864145786, 0.7986059369343825, 0.23867375911593536, 1.0), 4: (0.6099130083292249, 0.1907738372269024, 0.17321800842279583, 1.0), 5: (0.5085292438262377, 0.48019196425993127, 0.3712096216164097, 1.0), 6: (0.32413983393213663, 0.27143690687570705, 0.5985913598697046, 1.0), 7: (0.426129912049665, 0.446693771964658, 0.5374092619728105, 1.0), 8: (0.28339012144761694, 0.6413647052132629, 0.5889655552403823, 1.0), 9: (0.13750459808733506, 0.4562734628619436, 0.5740562869542097, 1.0), 10: (0.17545605896926386, 0.7209727449534825, 0.8941536301294938, 1.0), 11: (0.2891789882950511, 0.1832955383552637, 0.34300019357143957, 1.0), 12: (0.8616420730743021, 0.24914412582017295, 0.5270930912265664, 1.0), 13: (0.37333846783603375, 0.4522383669295674, 0.26038925112639666, 1.0), 14: (0.3746913528453374, 0.6664216748663568, 0.6372749974716163, 1.0), 15: (0.2802858675663846, 0.788100277467772, 0.8539638221859209, 1.0), 16: (0.11865276379861545, 0.275747046801176, 0.5647788950344205, 1.0), 17: (0.44737896953652323, 0.7103500534049395, 0.4443565395683111, 1.0), 18: (0.6917093203126766, 0.3224005815042632, 0.3402804141543057, 1.0), 19: (0.6862925212776556, 0.1062587341862452, 0.1583668232076393, 1.0), 20: (0.8374276990036071, 0.11406143952983312, 0.698327332022104, 1.0), 21: (0.37404980887894834, 0.5088204765644017, 0.2865147949027752, 1.0), 22: (0.5391058113525161, 0.19107159119784747, 0.127805006147947, 1.0), 23: (0.5689512917089193, 0.6028010859381107, 0.8003116137350171, 1.0), 24: (0.34656142984029065, 0.77633656140036, 0.5466361681047952, 1.0), 25: (0.49544512304784516, 0.5836771196979381, 0.3450386828024839, 1.0), 26: (0.34828180085097793, 0.8685481137103209, 0.6444111977597553, 1.0), 27: (0.33252242890651634, 0.7309963049574595, 0.5258481189424487, 1.0), 28: (0.5369236674275061, 0.7776937520258218, 0.7420516725402431, 1.0), 29: (0.7504003852419685, 0.6360410169651108, 0.6866045858271742, 1.0), 30: (0.24314311019797305, 0.6477462949426345, 0.4491924013920776, 1.0), 31: (0.5385983057421462, 0.12975496847632595, 0.8483874519883624, 1.0), 32: (0.6787198269243813, 0.1803904070547999, 0.7973064110802505, 1.0), 33: (0.4987426772787241, 0.46710674815251074, 0.5870314746621755, 1.0), 34: (0.5385538578156915, 0.4371217268243399, 0.719867933370514, 1.0), 35: (0.4177300829256664, 0.3746992335000999, 0.5128156826858609, 1.0), 36: (0.6920023492146437, 0.8817027390292737, 0.16851389667875843, 1.0), 37: (0.21718894915499654, 0.25842279049489947, 0.41915776297696217, 1.0), 38: (0.8588809370842632, 0.8119298528416876, 0.6719880658483209, 1.0), 39: (0.2592933360582904, 0.21426722442969037, 0.6866326883719349, 1.0), 40: (0.5801259073224297, 0.7528776493025519, 0.1882557673098278, 1.0), 41: (0.4327142229072368, 0.3577518005013193, 0.8848638967859389, 1.0), 42: (0.8601657585533244, 0.5352595069994573, 0.6424134744049365, 1.0), 43: (0.26010801745107126, 0.4652493173174558, 0.7931855696209342, 1.0), 44: (0.30469062363474597, 0.7622372209143918, 0.6976791407885744, 1.0), 45: (0.668853713843359, 0.7447330872733489, 0.4591755486405188, 1.0), 46: (0.4323453194471716, 0.4009110968178041, 0.8201047484361016, 1.0), 47: (0.646323076720932, 0.5043066926825274, 0.7690945171650964, 1.0), 48: (0.5820674381997041, 0.2708065298373421, 0.1487635304924565, 1.0), 49: (0.4731663783343365, 0.34221782056475747, 0.6540754208699079, 1.0)}

def showPlot():
    plt.ion()
    plt.show(block=False)

def keepPlot():
    plt.ioff()
    plt.show()

def plotUpdatedSchedule(makespan,schedule):

    global fig, gnt
    plt.cla()
    #print(schedule)

    bar_height = 3.0
    bar_margin = 2.0
    # Declaring a figure "gnt"
    #fig, gnt = plt.subplots()
    
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
    #work_order_color = {}
    work_order_color = getColors()

    def legend_without_duplicate_labels(ax):
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        return zip(*unique)

    for idx,sched in enumerate(schedule):
        
        for item in schedule[sched]:
            if item['order_id'] not in work_order_color.keys():
                work_order_color[item['order_id']] = (random.uniform(0.1, 0.9),random.uniform(0.1, 0.9),random.uniform(0.1, 0.9),1.0)
            y_bar_pos = yticks[idx]-(bar_height/2.0)

            #In Hours
            starttime = item['starttime']/60.0
            endtime = item['endtime'] /60.0
            duration = endtime-starttime
            label = 'Machine setup' if item['order_id'] == 'setup' else 'Order '+str(item['order_id'])
            #gnt.broken_barh([(item['starttime']/60.0,(item['endtime']-item['starttime'])/60.0)],(y_bar_pos,bar_height),facecolors=(work_order_color[item['order_id']]),edgecolor='black', label='Order '+str(item['order_id']))
            gnt.broken_barh([(starttime,duration)],(y_bar_pos,bar_height),facecolors=(work_order_color[item['order_id']]),edgecolor='black', label=label)
            if duration > 10:
                gnt.text(x=(starttime+duration/2), 
                        y=yticks[idx],
                        s=item['part_name'] + "-" + item['operation'], 
                        ha='center', 
                        va='center',
                        color='black',
                    )
    #fig.canvas.draw()
    #fig.set_figwidth(gnt.get_figure().get_figwidth()+10)
    fig.set_figwidth(gnt.get_ylim()[0]/10+18)
    
    plt.legend(*(legend_without_duplicate_labels(gnt)),loc='center left', bbox_to_anchor=(1,0.5))
    
    plt.pause(0.05)
    
    #plt.show()

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
    #work_order_color = {}
    work_order_color = getColors()

    def legend_without_duplicate_labels(ax):
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        return zip(*unique)

    for idx,sched in enumerate(schedule):
        
        for item in schedule[sched]:
            if item['order_id'] not in work_order_color.keys():
                work_order_color[item['order_id']] = (random.uniform(0.1, 0.9),random.uniform(0.1, 0.9),random.uniform(0.1, 0.9),1.0)
            y_bar_pos = yticks[idx]-(bar_height/2.0)

            #In Hours
            starttime = item['starttime']/60.0
            endtime = item['endtime'] /60.0
            duration = endtime-starttime
            label = 'Machine setup' if item['order_id'] == 'setup' else 'Order '+str(item['order_id'])
            #gnt.broken_barh([(item['starttime']/60.0,(item['endtime']-item['starttime'])/60.0)],(y_bar_pos,bar_height),facecolors=(work_order_color[item['order_id']]),edgecolor='black', label='Order '+str(item['order_id']))
            gnt.broken_barh([(starttime,duration)],(y_bar_pos,bar_height),facecolors=(work_order_color[item['order_id']]),edgecolor='black', label=label)
            if duration > 10:
                gnt.text(x=(starttime+duration/2), 
                        y=yticks[idx],
                        s=item['part_name'] + "-" + item['operation'], 
                        ha='center', 
                        va='center',
                        color='black',
                    )
    #fig.canvas.draw()
    #fig.set_figwidth(gnt.get_figure().get_figwidth()+10)
    fig.set_figwidth(gnt.get_ylim()[0]/10+18)
    
    plt.legend(*(legend_without_duplicate_labels(gnt)),loc='center left', bbox_to_anchor=(1,0.5))
    
    plt.show()
