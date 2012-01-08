import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import sqlite3
from mpl_toolkits.axes_grid1 import make_axes_locatable

#username = 'yourlogin'
username = 'wojtek.jurczyk'

def generate(sqldb, name='test', yearmin=None, yearmax=None, monthmin=None, monthmax=None, daymin=None, daymax=None, hourmin=None, hourmax=None, direction=None, people=None, title=""):
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
    
    
    heatmap = [0 for x in range(7)]
    for x in range(7):
	    heatmap[x] = [0 for y in range(24)]

    conn = sqlite3.connect(sqldb)	
    query = "select strftime('%w',datetime), hour, count(*) from stats "+wheresql+" group by hour, strftime('%w',datetime) order by count(*) desc;"
    cur = conn.cursor()
    cur.execute(query)
    for row in cur:
	    heatmap[(6-int(row[0]) + 1)%7][row[1]] = row[2]
    conn.close()

    #print heatmap
    extent = [0, 24, 0, 7]
    plt.clf()
    plt.ylabel('Days')
    plt.xlabel('Hours')
    plt.title('Distribution of the messages over days and hours' + title)
    plt.yticks(np.arange(0.0,7.0,1)+0.5,('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun') )
    plt.xticks(np.arange(0,24,1)+0.5, np.arange(0,24,1))
    ax = plt.subplot(111)
    im = ax.imshow(heatmap, extent=extent, interpolation='nearest')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cb = plt.colorbar(im, cax=cax)
    cb.set_label("Number of the messages")
    plt.savefig('./heatmap_'+name+'.png', bbox_inches='tight')
    
    
sqldb = './output/'+username+'/stats.db'

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

html = """<html><body><table><tr><td><img src="heatmap_2008.png"></li></td></tr>
<tr><td><img src="heatmap_2009.png"></li></td></tr>
<tr><td><img src="heatmap_2010.png"></li></td></tr>
<tr><td><img src="heatmap_2011.png"></li></td></tr>
<tr><td><img src="heatmap_2012.png"></li></td></tr></table>
</body></html>"""

f = open('./stats.html', 'w')
f.write(html)
f.flush()
f.close()

