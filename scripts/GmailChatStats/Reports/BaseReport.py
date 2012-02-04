
class BaseReport(object):
    def __init__(self, name, sqldb, title="", year=None, yearmin=None, yearmax=None, month=None, monthmin=None, monthmax=None, day=None, daymin=None, daymax =None, hour=None, hourmin=None, hourmax=None, minute=None, minutemin=None, minutemax=None, second=None, secondmin=None, secondmax=None, direction=None, peopleInclude=None, peopleExclude=None):
        self.name = name
        self.sqldb = sqldb
        self.title = title
        
        where = []
        if year != None:
            where.append('year = '+ str(year))
        else:
            if yearmin != None: where.append('year >= '+ str(yearmin))
            if yearmax != None: where.append('year <= '+ str(yearmax))
        
        if month != None:
            where.append('month = '+str(month))
        else:
            if monthmin != None: where.append('month >= '+str(monthmin))
            if monthmax != None: where.append('month <= '+str(monthmax))
            
        if day != None: 
            where.append('day = '+str(day))
        else:
            if daymin != None: where.append('day >= '+str(daymin))
            if daymax != None: where.append('day <= '+str(daymax))
        
        if hour != None: 
            where.append('hour = '+str(hour))
        else:
            if hourmin != None: where.append('hour >= '+str(hourmin))
            if hourmax != None: where.append('hour <= '+str(hourmax))
            
        if minute != None: 
            where.append('minute = '+str(minute))
        else:
            if minutemin != None: where.append('minute >= '+str(minutemin))
            if minutemax != None: where.append('minute <= '+str(minutemax))
            
        if second != None: 
            where.append('second = '+str(second))
        else:
            if secondmin != None: where.append('second >= '+str(secondmin))
            if secondmax != None: where.append('second <= '+str(secondmax))
            
        
        if direction != None: where.append('dir='+str(direction))
        
        datesql = None
        if where != None and len(where) > 0:
            datesql = ' and '.join(where)
            #print datesql
            
        pplsql = None
        if peopleInclude != None and len(peopleInclude) > 0:
            ppl = ["person = '"+p+"'" for p in peopleInclude]
            pplsql = ' or '.join(ppl)
            pplsql = '(' + pplsql + ')'
            
        pplexclsql = None
        if peopleExclude != None and len(peopleExclude) > 0:
            ppl = ["person != '"+p+"'" for p in peopleExclude]
            pplexclsql = ' and '.join(ppl)
            pplexclsql = '(' + pplexclsql + ')'
            
            
        where = []
        
        if (datesql != None or pplsql != None):
            wheresql = " where "
            
        if (datesql != None):
            where.append(datesql)
        
        if (pplsql != None):
            where.append(pplsql)
            
        if (pplexclsql != None):
            where.append(pplexclsql)
        
        wheresql = ""    
        if len(where) > 0:
            wheresql = " where " + ' and '.join(where)
        self.wheresql = wheresql
