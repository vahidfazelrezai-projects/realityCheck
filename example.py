import realityCheck

# gets data from Facebookd download folder placed in the parent directory (see https://www.facebook.com/help/131112897028467/)
myHistory = realityCheck.getFacebookMessageHistory('../facebook-vahidfazelrezai')

# saves history in JSON format in parent directory
myHistory.toFile('../reality.json')

# prints out dictionary containing all authors and number of messages across the messaging history
print myHistory.allAuthorCounts()