import realityCheck
from random import randint

# get data from Facebookd download folder placed in the parent directory (see https://www.facebook.com/help/131112897028467/)
myHistory = realityCheck.getFacebookMessageHistory('../facebook-vahidfazelrezai')

# save history in JSON format in parent directory
myHistory.toFile('../reality.json')

# loads history from saved file
myLoadedHistory = realityCheck.History.fromFile('../reality.json')
# myLoadedHistory is the same as myHistory

# print out dictionary containing all authors and number of messages across the messaging history
print myLoadedHistory.allAuthorCounts()

# get random thread
thread = myHistory.threads[randint(0, len(myHistory.threads))]

# print thread name
print thread.name

# print author counts
print thread.allAuthorCounts()

# print word statistics
for stat in thread.getSortedWords():
    print str('\'' + stat[0]) + '\': ' + str(stat[1])
