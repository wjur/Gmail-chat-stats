import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import sqlite3
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import spline

#username = 'yourlogin'
username = 'wojtek.jurczyk'

def generate(sqldb, name='test', yearmin=None, yearmax=None, monthmin=None, monthmax=None, daymin=None, daymax=None, hourmin=None, hourmax=None, direction=None, people=None, title=""):
    """ Calculates distribution of the messages over hours in the selected time span"""
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
    
    
    x = [i for i in range(24)]
    y = [0 for i in range(24)]

    conn = sqlite3.connect(sqldb)	
    query = "select hour, count(*) from stats "+wheresql+" group by hour order by hour;"
    cur = conn.cursor()
    cur.execute(query)
    for row in cur:
	    y[int(row[0])-1] = row[1]
    conn.close()
    m = max(y)
    plt.plot(x,y)
    plt.axis([0, 24, 0, 1.1*float(m)])
    
    plt.ylabel('Number of messages')
    plt.xlabel('Hours')
    plt.title('Distribution of the messages over hours' + title)
    plt.xticks(np.arange(0,24,1), np.arange(0,24,1))
    #plt.show()
    plt.savefig('./days_'+name+'.png', bbox_inches='tight')
    
sqldb = './output/'+username+'/stats.db'
generate(sqldb)
print '1'
#generate(sqldb,yearmax=2010, yearmin=2010, name="2010", title = ' (2010)')
print '2'
#generate(sqldb,yearmax=2009, yearmin=2009, name="2009", title = ' (2009)')
print '3'
#generate(sqldb,yearmax=2008, yearmin=2008, name="2008", title = ' (2008)')
print '4'
#generate(sqldb,yearmax=2011, yearmin=2011, name="2011", title = ' (2011)')
print '5'
#generate(sqldb,yearmax=2012, yearmin=2012, name="2012", title = ' (2012)')
print '6'
#generate(sqldb, name="total", title = ' (total)')

