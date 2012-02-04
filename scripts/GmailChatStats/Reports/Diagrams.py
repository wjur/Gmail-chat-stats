from datetime import date
import numpy as np
import numpy.random
#import matplotlib.figure
import matplotlib.pyplot as plt
import sqlite3
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import spline

from GmailChatStats.Reports.BaseReport import BaseReport

class Year(BaseReport):
    def __init__(self,sqldb, name, title="", year=None, yearmin=None, yearmax=None, month=None, monthmin=None, monthmax=None, day=None, daymin=None, daymax =None, hour=None, hourmin=None, hourmax=None, minute=None, minutemin=None, minutemax=None, second=None, secondmin=None, secondmax=None, direction=None, peopleInclude=None, peopleExclude=None):
        super(Year, self).__init__(sqldb=sqldb,name=name, title=title,year=year, yearmin=yearmin, yearmax=yearmax, month=month, monthmin=monthmin, monthmax=monthmax, day=day, daymin=daymin, daymax =daymax, hour=hour, hourmin=hourmin, hourmax=hourmax, minute=minute, minutemin=minutemin, minutemax=minutemax, second=second, secondmin=secondmin, secondmax=secondmax, direction=direction, peopleInclude=peopleInclude, peopleExclude=peopleExclude)
        """ Generates 2d histogram (day / hour) in selected year """	
        days = 366
        if (yearmin == yearmax and yearmin != None):
            first = date(yearmin, 1, 1)
            last = date(yearmin, 12, 31)
            year = last - first;
            days = year.days + 1
        
        heatmap = [0 for x in range(days+1)]
        for x in range(days+1):
            heatmap[x] = [0 for y in range(24)]

        conn = sqlite3.connect(self.sqldb)	
        query = "select strftime('%j',datetime),hour, count(*) from stats "+self.wheresql+" group by strftime('%j',datetime), hour order by hour;"
        cur = conn.cursor()
        cur.execute(query)
        for row in cur:
            # print row
            heatmap[(int(row[0]))][row[1]] = row[2]
        conn.close()

        extent = [0, 23, 0, days]
        plt.clf()
        plt.figure(num=None, figsize=(50, 50), facecolor='w', edgecolor='k') 
        plt.ylabel('Days')
        plt.xlabel('Hour')
        
        plt.yticks([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],['Jun', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.xticks(np.arange(0,24,1), np.arange(0,24,1))
        
        plt.imshow(heatmap, extent=extent, interpolation='nearest')
        plt.savefig(name+'.png', bbox_inches='tight')
        
class Hours(BaseReport):    
    def __init__(self,sqldb, name, title="", year=None, yearmin=None, yearmax=None, month=None, monthmin=None, monthmax=None, day=None, daymin=None, daymax =None, hour=None, hourmin=None, hourmax=None, minute=None, minutemin=None, minutemax=None, second=None, secondmin=None, secondmax=None, direction=None, peopleInclude=None, peopleExclude=None):
        super(Hours, self).__init__(sqldb=sqldb,name=name, title=title,year=year, yearmin=yearmin, yearmax=yearmax, month=month, monthmin=monthmin, monthmax=monthmax, day=day, daymin=daymin, daymax =daymax, hour=hour, hourmin=hourmin, hourmax=hourmax, minute=minute, minutemin=minutemin, minutemax=minutemax, second=second, secondmin=secondmin, secondmax=secondmax, direction=direction, peopleInclude=peopleInclude, peopleExclude=peopleExclude)
        
        x = [i for i in range(24)]
        y = [0 for i in range(24)]

        conn = sqlite3.connect(self.sqldb)	
        query = "select hour, count(*) from stats "+self.wheresql+" group by hour order by hour;"
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
    
class DaysHours(BaseReport):
    def __init__(self,sqldb, name, title="", year=None, yearmin=None, yearmax=None, month=None, monthmin=None, monthmax=None, day=None, daymin=None, daymax =None, hour=None, hourmin=None, hourmax=None, minute=None, minutemin=None, minutemax=None, second=None, secondmin=None, secondmax=None, direction=None, peopleInclude=None, peopleExclude=None):
        super(DaysHours, self).__init__(sqldb=sqldb,name=name, title=title,year=year, yearmin=yearmin, yearmax=yearmax, month=month, monthmin=monthmin, monthmax=monthmax, day=day, daymin=daymin, daymax =daymax, hour=hour, hourmin=hourmin, hourmax=hourmax, minute=minute, minutemin=minutemin, minutemax=minutemax, second=second, secondmin=secondmin, secondmax=secondmax, direction=direction, peopleInclude=peopleInclude, peopleExclude=peopleExclude)
        
        heatmap = [0 for x in range(7)]
        for x in range(7):
            heatmap[x] = [0 for y in range(24)]

        conn = sqlite3.connect(self.sqldb)	
        query = "select strftime('%w',datetime), hour, count(*) from stats "+self.wheresql+" group by hour, strftime('%w',datetime) order by count(*) desc;"
        cur = conn.cursor()
        cur.execute(query)
        for row in cur:
            heatmap[(6-int(row[0]) + 1)%7][row[1]] = row[2]
        conn.close()

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
        
class MonthsDaysHours(BaseReport):
    def __init__(self,sqldb, name, title="", year=None, yearmin=None, yearmax=None, month=None, monthmin=None, monthmax=None, day=None, daymin=None, daymax =None, hour=None, hourmin=None, hourmax=None, minute=None, minutemin=None, minutemax=None, second=None, secondmin=None, secondmax=None, direction=None, peopleInclude=None, peopleExclude=None):
        super(MonthsDaysHours, self).__init__(sqldb=sqldb,name=name, title=title,year=year, yearmin=yearmin, yearmax=yearmax, month=month, monthmin=monthmin, monthmax=monthmax, day=day, daymin=daymin, daymax =daymax, hour=hour, hourmin=hourmin, hourmax=hourmax, minute=minute, minutemin=minutemin, minutemax=minutemax, second=second, secondmin=secondmin, secondmax=secondmax, direction=direction, peopleInclude=peopleInclude, peopleExclude=peopleExclude)
        
        if year != None:
            yearmin = yearmax = year
            
        if month != None:
            monthmin = monthmax = month

        days = 31
        if (yearmin == yearmax and yearmin != None and monthmin == monthmax and monthmax != None):
            first = date(yearmin, monthmin, 1)
            last = date(yearmin if monthmin<12 else yearmin+1, monthmin+1 if monthmin+1 < 13 else 1 , 1)
            gap = last - first
            days = gap.days
        
        heatmap = [0 for x in range(days)]
        for x in range(days):
            heatmap[x] = [0 for y in range(24)]

        conn = sqlite3.connect(self.sqldb)
        query = "select day,hour, count(*) from stats "+self.wheresql+" group by day, hour order by hour;"
        cur = conn.cursor()
        cur.execute(query)
        for row in cur:
            heatmap[int(row[0])-1][row[1]] = row[2]
        conn.close()

        extent = [0, 24, 0, days]
        plt.clf()
        plt.ylabel('Days')
        plt.xlabel('Hour')
        plt.title('Distribution of the messages over days and hours' + title)
        names = np.arange(1, days++1, 1) 
        plt.yticks(np.arange(1,days+1,1), names[::-1])
        ax = plt.subplot(111)
        im = ax.imshow(heatmap, extent=extent, interpolation='nearest')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax)
        cb.set_label("Number of the messages")
        plt.savefig(name+'.png', bbox_inches='tight')
