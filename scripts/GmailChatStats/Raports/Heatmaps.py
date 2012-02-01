import numpy as np
import numpy.random
#import matplotlib.figure
import matplotlib.pyplot as plt
import sqlite3
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import spline

class Year:
	def __generateWhere(self, yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people=None):
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
		return wheresql

	
	def __init__(self,sqldb, name, yearmin=None, yearmax=None, monthmin=None, monthmax=None, daymin=None, daymax=None, hourmin=None, hourmax=None, direction=None, people=None, title=""):
		wheresql = self.__generateWhere(yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people)
		""" Generates 2d histogram (day / hour) in selected year """
		#I should check how many days the year has but I'm too lazy to do it.
		heatmap = [0 for x in range(367)]
		for x in range(367):
			heatmap[x] = [0 for y in range(24)]

		conn = sqlite3.connect(sqldb)	
		query = "select strftime('%j',datetime),hour, count(*) from stats "+wheresql+" group by strftime('%j',datetime), hour order by hour;"
		cur = conn.cursor()
		cur.execute(query)
		for row in cur:
			# print row
			heatmap[(int(row[0]))][row[1]] = row[2]
		conn.close()

		# Same here. I should check but.. whatever! None cares 
		extent = [0, 24, 0, 366]
		plt.clf()
		plt.figure(num=None, figsize=(50, 50), dpi=80, facecolor='w', edgecolor='k') 
		plt.ylabel('Days')
		plt.xlabel('Hour')
		ax = plt.subplot(111)
		im = ax.imshow(heatmap, extent=extent, interpolation='nearest')

		plt.savefig(name+'.png', bbox_inches='tight')
		
class Hours:
	def __generateWhere(self, yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people=None):
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
		return wheresql

	
	def __init__(self,sqldb, name, yearmin=None, yearmax=None, monthmin=None, monthmax=None, daymin=None, daymax=None, hourmin=None, hourmax=None, direction=None, people=None, title=""):
		wheresql = self.__generateWhere(yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people)
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
		plt.clf()
		plt.plot(x,y)
		plt.axis([0, 24, 0, 1.1*float(m)])
		
		plt.ylabel('Number of messages')
		plt.xlabel('Hours')
		plt.title('Distribution of the messages over hours' + title)
		plt.xticks(np.arange(0,24,1), np.arange(0,24,1))
		#plt.show()
		plt.savefig(name+'.png', bbox_inches='tight')
    
class DaysHours:
	def __generateWhere(self, yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people=None):
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
		return wheresql

	
	def __init__(self,sqldb, name, yearmin=None, yearmax=None, monthmin=None, monthmax=None, daymin=None, daymax=None, hourmin=None, hourmax=None, direction=None, people=None, title=""):
		wheresql = self.__generateWhere(yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people)
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
		plt.savefig(name+'.png', bbox_inches='tight')
		
class MonthsDaysHours:
	def __generateWhere(self, yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people=None):
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
		return wheresql

	
	def __init__(self,sqldb, name, yearmin=None, yearmax=None, monthmin=None, monthmax=None, daymin=None, daymax=None, hourmin=None, hourmax=None, direction=None, people=None, title=""):
		wheresql = self.__generateWhere(yearmin, yearmax, monthmin, monthmax, daymin, daymax, hourmin, hourmax, direction, people)
		heatmap = [0 for x in range(32)]
		for x in range(32):
			heatmap[x] = [0 for y in range(24)]

		conn = sqlite3.connect(sqldb)	
		query = "select day,hour, count(*) from stats "+wheresql+" group by day, hour order by hour;"
		cur = conn.cursor()
		cur.execute(query)
		for row in cur:
			heatmap[int(row[0])][row[1]] = row[2]
		conn.close()
		#print heatmap
		extent = [0, 24, 0, 31]
		plt.clf()
		plt.ylabel('Days')
		plt.xlabel('Hour')
		plt.title('Distribution of the messages over days and hours' + title)
		#plt.yticks(np.arange(0.0,7.0,1)+0.5,('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun') )
		#plt.xticks(np.arange(0,24,1)+0.5, np.arange(0,24,1))
		ax = plt.subplot(111)
		im = ax.imshow(heatmap, extent=extent, interpolation='nearest')
		divider = make_axes_locatable(ax)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		cb = plt.colorbar(im, cax=cax)
		cb.set_label("Number of the messages")
		plt.savefig(name+'.png', bbox_inches='tight')
