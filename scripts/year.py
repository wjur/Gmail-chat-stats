import numpy as np
import numpy.random
#import matplotlib.figure
import matplotlib.pyplot as plt
import sqlite3
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import spline

#username = 'yourlogin'
username = ''

def generate(sqldb, name='test', yearmin=None, yearmax=None, monthmin=None, monthmax=None, daymin=None, daymax=None, hourmin=None, hourmax=None, direction=None, people=None, title=""):
    """ Generates 2d histogram (day / hour) in selected year """
    where = []
    if yearmin != None: where.append('year >= '+ str(yearmin))
    if yearmax != None: where.append('year <= '+ str(yearmax))
    if monthmin != None: where.append('month >= '+str(monthmin))
    if monthmax != None: where.append('month <= '+str(monthmax))
    if daymin != None: where.append('day >= '+str(daymin))
    if daymax != None: where.append('day <= '+str(daymax))
    if hourmin != None: where.append('hour >= '+str(hourmin))
    if hourmax != None: where.append('hour <= '+str(hourmax))
    if direction != None: where.append('dir='+str(direction))
    
    datesql = None
    if where != None and len(where) > 0:
    	datesql = ' and '.join(where)
    	#print datesql
    	
    pplsql = None
    if people != None and len(people) > 0:
    	ppl = ["person = '"+p+"'" for p in people]
    	pplsql = ' or '.join(ppl)
    	pplsql = '(' + pplsql + ')'
    	#print pplsql
    	
    where = []
    
    if (datesql != None or pplsql != None):
        wheresql = " where "
        
    if (datesql != None):
        where.append(datesql)
    
    if (pplsql != None):
        where.append(pplsql)
    
    wheresql = ""    
    if len(where) > 0:
        wheresql = " where " + ' and '.join(where)
        
    #print wheresql
    
    #I should check how many days the year has but I'm too lazy to do it.
    heatmap = [0 for x in range(367)]
    for x in range(367):
	    heatmap[x] = [0 for y in range(24)]

    conn = sqlite3.connect(sqldb)	
    query = "select strftime('%j',datetime),hour, count(*) from stats "+wheresql+" group by strftime('%j',datetime), hour order by hour;"
    cur = conn.cursor()
    cur.execute(query)
    for row in cur:
        print row
        heatmap[(int(row[0]))][row[1]] = row[2]
    conn.close()
    print heatmap
    extent = [0, 24, 0, 366]
    plt.clf()
    plt.figure(num=None, figsize=(50, 50), dpi=80, facecolor='w', edgecolor='k') 
    plt.ylabel('Days')
    plt.xlabel('Hour')
    #plt.title('Distribution of the messages over days and hours' + title)
    #plt.yticks(np.arange(0.0,7.0,1)+0.5,('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun') )
    #plt.xticks(np.arange(0,24,1)+0.5, np.arange(0,24,1))
    ax = plt.subplot(111)
    im = ax.imshow(heatmap, extent=extent, interpolation='nearest')
    #cax = divider.append_axes("right", size="5%", pad=0.05)
    #cb = plt.colorbar(im, cax=cax)
    #cb.set_label("Number of the messages")
    #im.set_size_inches(8.27, 11.69)

    plt.savefig('./img/year_'+name+'.png', bbox_inches='tight')
    #plt.show()
    
#this is just an example!
sqldb = './output/'+username+'/stats.db'
generate(sqldb)
print '1'
generate(sqldb,yearmax=2010, yearmin=2010, name="2010", title = ' (2010)')
print '2'
generate(sqldb,yearmax=2009, yearmin=2009, name="2009", title = ' (2009)')
print '3'
generate(sqldb,yearmax=2008, yearmin=2008, name="2008", title = ' (2008)')
print '4'
generate(sqldb,yearmax=2011, yearmin=2011, name="2011", title = ' (2011)')
print '5'
generate(sqldb,yearmax=2012, yearmin=2012, name="2012", title = ' (2012)')
print '6'
generate(sqldb, name="total", title = ' (total)')
