# -*- coding: utf-8 -*-
import random;
import pylab;
import numpy as np;

# ******* Classes ************************

class GammaDistribution:
    """
    Mean of gamma distribution is shape * scale (+ shift)
    """
    def __init__(self, shape, scale, shift = 0):
        self.shape = shape
        self.scale = scale
        self.shift = shift

    def random(self):
        return self.shift + random.gammavariate(self.shape, self.scale);

    def mean(self):
        return self.shift + self.shape/self.scale   
           

class UserStory:
    
    def __init__(self, size = 1, description = ''):
        self.id = incrementCounter(1)
        
        if size < 0.25:
            self.size = 0;
            self.actualSize = 0;
        elif size < 0.6:
            self.size = 0.5
            self.actualSize = self.size + random.uniform(-0.25, 0.25)
        else:
            self.size = round(size,0)
            self.actualSize = self.size + random.uniform(-0.5, 0.5)
        
        self.desc = description;
        self.status = 'approved'
        self.assignedTo = []
   
    def getId(self):
        return self.id
         
    def getSize(self):
        return self.size;
        
    def getActualSize(self):
        return self.actualSize;
        
    def getAssignedTo(self):
        return self.assignedTo
    
    def getDescription(self):
        return self.description;
        
    def setStatus(self, status):
        self.status = status;
        
    def getTimeToComplete(self):
        if self.actualSize == 0:
            return 0;
        else:
            dist = GammaDistribution(2.0, self.actualSize * 0.5, 0.0);
            return dist.random();
            
    def isComplete(self):
        if self.status in ('closed','complete'):
            return True;
        else:
            return False
            

class Programmer:
    
    def __init__(self):
        self.id = incrementCounter(2)
        self.lastEventTime = 0
        self.assignedUserStory = None
        self.status = 'available'
        self.provisionalTime = 0
        self.assignedTime = 0
        self.completedTasks = 0
        
        self.productiveAssignedTime = 0
        self.wasteOverloadTime = 0
        self.unassignedTime = 0
        
    def getId(self):
        return self.id
    
    def isAssigned(self):
        if self.assignedUserStory == None:
            return False
        else:
            return True
        
    def assign(self, userStory, time):
        self.assignedUserStory = userStory.getId()
        self.assignedTime = time
        if self.lastEventTime != time:
            self.unassignedTime += time - self.lastEventTime
            self.lastEventTime = time;
        self.provisionalTime = userStory.getTimeToComplete()
        userStory.getAssignedTo().append(self)
        
    def unassign(self, time, commit = True):
        if commit == False:
            self.wasteOverloadTime += time - self.assignedTime 
        else:
            self.productiveAssignedTime += self.provisionalTime
            self.completedTasks += 1
        self.lastEventTime = time
        self.assignedUserStory = None
        self.provisionalTime = 0
    
    def getNextAvailability(self):
        return self.lastEventTime + self.provisionalTime
        
    def stop(self, time):
        if self.isAssigned():
            self.unassign(time, commmit = False)
        assert not self.isAssigned()
        if self.lastEventTime != time:
            self.unassignedTime += time - self.lastEventTime
            self.lastEventTime = time;
        
    def getAssignedUserStory(self):
        return self.assignedUserStory;
        
    def getProductiveAssignedTime(self):
        return self.productiveAssignedTime
        
    def getWasteTime(self):
        return self.wasteOverloadTime
        
    def getUnassignedTime(self):
        return self.unassignedTime
        
        
            
          
# ******* Reporting ************************

def plotResults(results):
    pylab.hist(results, bins = 30);
    pylab.xlim(0);
    pylab.show();

def printPercentiles(extendedResults, index = 0):
    print "<-- %5.1f" % np.percentile(extendedResults[:,index],0),;
    print "{{ %5.1f" % np.percentile(extendedResults[:,index],5),;
    print "{ %5.1f" % np.percentile(extendedResults[:,index],16),;
    print "[ %5.1f" % np.percentile(extendedResults[:,index],25),;
    print " %5.1f " % np.percentile(extendedResults[:,index],50),;
    print "%5.1f ]" % np.percentile(extendedResults[:,index],75),;
    print "%5.1f }" % np.percentile(extendedResults[:,index],85),;
    print "%5.1f }}" % np.percentile(extendedResults[:,index],95),;
    print "%5.1f -->" % np.percentile(extendedResults[:,index],100);

def summarize(results, numProgrammers, numStoryPoints, description = '', graph = False):
    #print results
    extendedResults = np.matrix(np.asarray(results))
    print '****************  ' + description + ':'
    print ''
    
    print 'MEANS'
    printMeans(np.mean(extendedResults[:, 0]), np.std(extendedResults[:, 0]), 'Duration:        ')
    costsPlanned = extendedResults[:, 0] * numProgrammers /numStoryPoints
    printMeans(np.mean(costsPlanned), np.std(costsPlanned), 'Cost/planned usp:')
    costsPlanAdj = (extendedResults[:, 0] * numProgrammers - extendedResults[:, 2]) /numStoryPoints
    printMeans(np.mean(costsPlanAdj), np.std(costsPlanAdj), 'Adj cost/usp:    ')
    printMeans(np.mean(extendedResults[:, 1]), np.std(extendedResults[:, 1]), 'Assigned:        ')
    printMeans(np.mean(extendedResults[:, 2]), np.std(extendedResults[:, 2]), 'Unassigned       ')
    printMeans(np.mean(extendedResults[:, 3]), np.std(extendedResults[:, 3]), 'Waste:           ')
    print ''
    
    print 'PERCENTILES             min      5%      15%     25%   50%    75%     85%     95%     max'
    print 'Duration:        ', 
    printPercentiles(extendedResults, 0);
    print 'Totals:          '
    print 'Cost:            ',
    printPercentiles(extendedResults * numProgrammers, 0);
    print 'Assigned:        ', 
    printPercentiles(extendedResults, 1);
    print 'UnAssigned:      ', 
    printPercentiles(extendedResults, 2);
    print 'Waste:           ', 
    printPercentiles(extendedResults, 3);  
    print ''
    print ''
    
    if graph:
        plotResults(extendedResults,0);
        
        
# ******* Helper functions ************************    

def printMeans(mu, sigma, description):
    print description,
    print 'μ %.2f' % mu,'(σ %.2f' % sigma,
    if mu != 0:
        print '/%.2f)' % (sigma/mu)
    else:
        print '/undef)'  

def incrementCounter(i):
    if i == 1:
        incrementCounter.counter1 += 1
        return incrementCounter.counter1
    elif i == 2:
        incrementCounter.counter2 += 1
        return incrementCounter.counter2
  
incrementCounter.counter1 = -1
incrementCounter.counter2 = -1
    
def minIndex(times):
        earliest = 1000000000
        earliestIndex = -1
        
        for i in range(len(times)):
            if times[i] < earliest:
                earliest = times[i]
                earliestIndex = i;      
        
        return earliestIndex;
            
          
# ******* Setup functions ************************  
        
def getApprovedBacklog(sprintPoints):
    backlog = []
    total = 0
    
    while total < sprintPoints:
        usp = random.randrange(0, 10);
        if usp == 0:
            usp = 0.5

        if total + usp <= sprintPoints:
            backlog.append(usp)
            total += usp
        else:
            while total + 3 <= sprintPoints:
                backlog.append(3)
                total += 3
            while total + 1 <= sprintPoints:
                backlog.append(1)
                total += 1
            while total + 0.5 <= sprintPoints:
                backlog.append(0.5)
                total += 0.5
                
    return backlog  
    

def getUserStories(backlogSizes):
    userStories = []
    for size in backlogSizes:
        userStories.append(UserStory(size))
    
    return userStories
    
def getProgrammers(num):
    programmers = []
    for i in range(num):
        programmers.append(Programmer())
    
    return programmers
        
                
# ******* Run Trials ************************                                                                         
                                                
                                                                                                                                                                               
def runTrialsBacklogMPersons(backlog, m, sequence = 'default', overload = 1, numTrials = 1000):   

    def getNextAvailableProgrammer():

        for p in programmers:
            if not p.isAssigned():
                return p;
        
        return None
        
    def getNextUserStoryToFinish():
        """
        find the first active programmer to become available
        """      
        firstToFinish = None
        firstFinishTime = 2E09
        
        for p in programmers:
            if not p.isAssigned():
                continue;
                
            finish = p.getNextAvailability()
            if firstToFinish == None or finish < firstFinishTime:
                firstToFinish = p;
                firstFinishTime = finish
        
        return firstToFinish.getAssignedUserStory(), firstToFinish, firstFinishTime;
    
    def isBacklogComplete():
        for userStory in userStories:
            if not userStory.isComplete():
                return False
        
        return True;
    
    def getNextUserStory(maxAssign = 1):
        if sequence == 'default': 
            return getNextStoryOrderByGivenSequence(maxAssign)
        else:
            return getNextStoryOrderBySizeDesc(maxAssign)
        
        
    def getNextStoryOrderByGivenSequence(maxAssign = 1):
        minAssignedUserStories = [];
        minAssignedValue = 2E03;
        
        for userStory in userStories:
            if userStory.isComplete():
                continue
                
            numProgrammers = len(userStory.getAssignedTo())
            if numProgrammers == 0:
                return userStory
            
            if numProgrammers < minAssignedValue:
                minAssignedValue = numProgrammers
                minAssignedUserStories = [userStory]
            elif numProgrammers == minAssignedValue:
                minAssignedUserStories.append(userStory)
        
        if minAssignedValue < maxAssign:
            return random.choice(minAssignedUserStories)
        else:
            return None
    
    def getNextStoryOrderBySizeDesc(maxAssign = 1):
        priorityDict = {}
        for userStory in userStories:
            if not userStory.isComplete() and len(userStory.getAssignedTo()) < maxAssign:
                priority = userStory.getSize() / (len(userStory.getAssignedTo()) + 1)
                
                if priority in priorityDict:
                    priorityDict[priority].append(userStory)
                else:
                    priorityDict[priority] = [userStory]
        
        if len(priorityDict.keys()) == 0:
            return None
            
        maxPriority = max(priorityDict.keys())
        maxPriorityList = priorityDict[maxPriority]
        
        return random.choice(maxPriorityList)
            
    def getProgrammersAssignedToUserStory(userStoryId):
        ps = []
        for p in programmers:
            if p.getAssignedUserStory() == userStoryId:
                ps.append(p)
        return ps;
        
    def getUserStoryById(storyId):
        for us in userStories:
            if us.getId() == storyId:
                return us;
                
    def numAssignedProgrammers():
        countP = 0
        for p in programmers:
            if p.isAssigned():
                countP += 1
        return countP
        
    def showAssignments():
        print 'Assignments', numAssignedProgrammers(),
        for p in programmers:
            if p.isAssigned():
                print '%d' % p.getAssignedUserStory(),
                print '(%d)' % p.getId(),
        print ''
        
    def getProductiveAssignedTime():
        productiveAssignedTime = 0
        for p in programmers:
            productiveAssignedTime += p.getProductiveAssignedTime()
        return productiveAssignedTime
        
    def getUnassignedTime():
        unassignedTime = 0
        for p in programmers:
            unassignedTime += p.getUnassignedTime()
        return unassignedTime
        
    def getWastedTime():
        wastedTime = 0
        for p in programmers:
            wastedTime += p.getWasteTime()
        return wastedTime
            
    results = []
    for i in range(numTrials):
        
        userStories = getUserStories(backlog)     
        programmers = getProgrammers(m)        
        lastTime = 0;
        tasksCompleted = 0;
        
        while not isBacklogComplete():

            # assign available programmers
            while True:
                userStory = getNextUserStory(overload)
                programmer = getNextAvailableProgrammer()
                    
                # every programmer assigned or no stories to assign
                if programmer ==  None or userStory == None:
                    break;
   
                programmer.assign(userStory, lastTime)
            
            #showAssignments()

            nextUserStoryToFinish, finishProgrammer, finishTime = getNextUserStoryToFinish();
            assert nextUserStoryToFinish != None
            
            #print 'Completed', tasksCompleted, nextUserStoryToFinish, '%.1f' % finishTime
            lastTime = finishTime
            getUserStoryById(nextUserStoryToFinish).setStatus('complete')
            tasksCompleted += 1
            
            for p in getProgrammersAssignedToUserStory(nextUserStoryToFinish):
                if p == finishProgrammer:
                    p.unassign(finishTime)
                else:
                    p.unassign(finishTime, False)                 
        
        for p in programmers:
            p.stop(lastTime);
        
        for p in programmers:
            assert abs(p.getProductiveAssignedTime() + p.getWasteTime() + p.getUnassignedTime() - lastTime) < 0.01
        
        assert len(backlog) == tasksCompleted       
        assert abs(getProductiveAssignedTime() + getWastedTime() + getUnassignedTime() - lastTime * len(programmers)) < 0.01
        results.append((lastTime, getProductiveAssignedTime(), getUnassignedTime(), getWastedTime()))
    
    return results 
      

# ******* Main ************************                                                                         

                

backlog = [1] 
print 'Benchmark 1 story 1 story point, 1 programmer'
print 'Backlog', 1, 'story points in', len(backlog), 'stories'
summarize(runTrialsBacklogMPersons(backlog, 1, overload = 1, numTrials = 1000), 1, 1, '1 point 1 developer 1 overload')
print ''
print ''

STORYPOINTS = 100

backlog = [1] * STORYPOINTS
print 'Backlog', STORYPOINTS, 'story points in', len(backlog), 'stories'
print ''

summarize(runTrialsBacklogMPersons(backlog, 1, overload = 1, numTrials = 1000), 1, 100, '100 * 1 points 1 developer')
summarize(runTrialsBacklogMPersons(backlog, 5, overload = 1, numTrials = 1000), 5, 100, '100 * 1 points 5 developers 1 overload')
summarize(runTrialsBacklogMPersons(backlog, 5, overload = 4, numTrials = 1000), 5, 100, '100 * 1 points 5 developers 4 overload')
summarize(runTrialsBacklogMPersons(backlog, 10, overload = 1, numTrials = 1000), 10, 100, '100 * 1 points 10 developers 1 overload')
summarize(runTrialsBacklogMPersons(backlog, 10, overload = 4, numTrials = 1000), 10, 100, '100 * 1 points 10 developers 4 overload')
summarize(runTrialsBacklogMPersons(backlog, 10, overload = 10, numTrials = 1000), 10, 100, '100 * 1 points 10 developers 10 overload')
print ''
print ''

backlog = getApprovedBacklog(STORYPOINTS)
print 'Backlog', STORYPOINTS, 'story points in', len(backlog), 'stories'
print backlog
print ''

summarize(runTrialsBacklogMPersons(backlog, 1, overload = 1, numTrials = 1000), 1, 100, '100 mixed points 1 developer')
summarize(runTrialsBacklogMPersons(backlog, 5, overload = 1, numTrials = 1000), 5, 100, '100 mixed points 5 developers 1 overload')
summarize(runTrialsBacklogMPersons(backlog, 5, overload = 4, numTrials = 1000), 5, 100, '100 mixed points 5 developers 4 overload')
summarize(runTrialsBacklogMPersons(backlog, 10, overload = 1, numTrials = 1000), 10, 100, '100 mixed points 10 developers 1 overload')
summarize(runTrialsBacklogMPersons(backlog, 10, overload = 4, numTrials = 1000), 10, 100, '100 mixed points 10 developers 4 overload')
summarize(runTrialsBacklogMPersons(backlog, 10, overload = 10, numTrials = 1000), 10, 100, '100 mixed points 10 developers 10 overload')

print ''
print ''

print 'Backlog', STORYPOINTS, 'story points in', len(backlog), 'stories prioritised by size'
print ''

summarize(runTrialsBacklogMPersons(backlog, 1, sequence = 'size', overload = 1, numTrials = 1000), 1, 100, '100 mixed points 1 developer order by Size')
summarize(runTrialsBacklogMPersons(backlog, 5, sequence = 'size', overload = 1, numTrials = 1000), 5, 100, '100 mixed points 5 developers 1 overload order by Size')
summarize(runTrialsBacklogMPersons(backlog, 5, sequence = 'size', overload = 4, numTrials = 1000), 5, 100, '100 mixed points 5 developers 4 overload order by Size')
summarize(runTrialsBacklogMPersons(backlog, 10, sequence = 'size', overload = 1, numTrials = 1000), 10, 100, '100 mixed points 10 developers 1 overload order by Size')
summarize(runTrialsBacklogMPersons(backlog, 10, sequence = 'size', overload = 4, numTrials = 1000), 10, 100, '100 mixed points 10 developers 4 overload order by Size')
summarize(runTrialsBacklogMPersons(backlog, 10, sequence = 'size', overload = 10, numTrials = 1000), 10, 100, '100 mixed points 10 developers 10 overload order by Size')
