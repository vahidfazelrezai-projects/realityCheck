import realityCheck

myHistory = realityCheck.getFacebookMessageHistory('../facebook-vahidfazelrezai')
myHistory.toFile('../reality.json')

print myHistory.allAuthorCounts()