# TODO: implement __str__

import json
import os
import datetime
from xml.dom.minidom import parseString


##### OBJECT CLASSES #####


# entire history of all messages
class History:
    def __init__(self, name, threads):
        self.name = name # string
        self.threads = threads # list of Thread objects

    # string representation
    def __str__(self):
        historyString = self.name + '\n\n\n'
        for thread in self.threads:
            historyString += '-----\n' + str(thread) + '\n\n'
        return historyString

    # returns History object from dictionary
    @classmethod
    def fromDict(cls, historyDict):
        history = cls('', []) # empty initialization
        history.name = historyDict['name']
        for threadDict in historyDict['threads']:
            history.threads.append(Thread.fromDict(threadDict))
        return history

    # returns History object from JSON file
    @classmethod
    def fromFile(cls, pathToJSON):
        f = open(pathToJSON, 'r')
        history = json.load(f)
        f.close()
        return cls.fromDict(history)

    # returns dict containing history information
    def toDict(self):
        historyDict = {}
        historyDict['name'] = self.name
        historyDict['threads'] = []
        for thread in self.threads:
            historyDict['threads'].append(thread.toDict())
        return historyDict

    # saves history information as JSON file (returns nothing)
    def toFile(self, pathToJSON):
        f = open(pathToJSON, 'w')
        json.dump(self.toDict(), f)
        f.close()

    # returns list of all authors with messages across all threads in history
    def getAuthors(self):
        authors = []
        for thread in self.threads:
            for author in thread.getAuthors():
                if author not in authors:
                    authors.append(author)
        return authors

    # returns integer count of number of messages by author
    def singleAuthorCount(self, author):
        authorCount = 0
        for thread in self.threads:
            authorCount += thread.singleAuthorCount(author)
        return authorCount
    
    # returns dict of author/count key/val pairs
    def allAuthorCounts(self):
        allAuthorCounts = dict.fromkeys(self.getAuthors(), 0)
        for author in allAuthorCounts.keys():
            allAuthorCounts[author] = self.singleAuthorCount(author)
        return allAuthorCounts



# single thread of messages
class Thread:
    def __init__(self, name, messages):
        self.name = name # string
        self.messages = messages # list of Message objects

    # string representation
    def __str__(self):
        threadString = self.name + '\n\n'
        for message in self.messages:
            threadString += str(message)
        return threadString

    # returns Message object from dictionary
    @classmethod
    def fromDict(cls, threadDict):
        thread = cls('', []) # empty initialization
        thread.name = threadDict['name']
        for messageDict in threadDict['messages']:
            thread.messages.append(Message.fromDict(messageDict))
        return thread

    # returns dict containing thread information
    def toDict(self):
        threadDict = {}
        threadDict['name'] = self.name
        threadDict['messages'] = []
        for message in self.messages:
            threadDict['messages'].append(message.toDict())
        return threadDict

    # returns list of authors with messages in thread
    def getAuthors(self):
        authors = []
        for message in self.messages:
            if message.author not in authors:
                authors.append(message.author)
        return authors

    # returns integer count of number of messages by author
    def singleAuthorCount(self, author):
        authorCount = 0
        for message in self.messages:
            if message.author == author:
                authorCount += 1
        return authorCount

    # returns dict of author/count key/val pairs
    def allAuthorCounts(self):
        allAuthorCounts = dict.fromkeys(self.getAuthors(), 0)
        for author in allAuthorCounts.keys():
            allAuthorCounts[author] = self.singleAuthorCount(author)
        return allAuthorCounts



# series of messages in a thread grouped by proximity in time (to be implemented)
class Conversation:
    def __init__(self, messages):
        self.messages = messages



# series of consercutive messages from same author (to be implemented)
class Strand:
    def __init__(self, messages):
        self.messages = messages



# single message
class Message:
    def __init__(self, author, time, text):
        self.author = author # string
        self.time = time # datetime object
        self.text = text # string

    # string representation
    def __str__(self):
        return self.time.isoformat() + ', ' + self.author + ": " + self.text + '\n'

    # returns Message object from dictionary
    @classmethod
    def fromDict(cls, messageDict):
        message = cls('', datetime.datetime.now(), '') # empty initialization
        message.author = messageDict['author']
        message.time = datetime.datetime.strptime(messageDict['time'], '%A, %B %d, %Y at %I:%M%p')
        message.text = messageDict['text']
        return message

    # returns dict containing message information
    def toDict(self):
        messageDict = {}
        messageDict['author'] = self.author
        messageDict['time'] = self.time.strftime('%A, %B %d, %Y at %I:%M%p')
        messageDict['text'] = self.text
        return messageDict

    # returns list of words in message text
    def getWords(self):
        return self.text.split(' ')




##### FACEBOOK DATA #####

# returns History object from Facebook's data archive folder
def getFacebookMessageHistory(pathToFacebookData):
    # opens messages.htm file in Facebook data archive folder
    print 'Reading data...'
    fin = open(os.path.join(pathToFacebookData, 'html/messages.htm'), 'r')
    rawRemaining = fin.read()

    # remove non-utf-8 characters (otherwise can't parse into DOM)
    rawRemaining = ''.join([i if ord(i) < 128 else ' ' for i in rawRemaining])

    # gets div with class="contents" using known file format
    print 'Parsing data...'
    (beginning, openContents, rawRemaining) = rawRemaining.partition("<div class=\"contents\">")
    (rawRemaining, closeContents, ending) = rawRemaining.partition("</div><div class=\"footer\">")
    facebookDOM = parseString("<document>" + rawRemaining + "</document>").firstChild    

    print 'Processing data...'
    # name of user
    historyName = facebookDOM.firstChild.firstChild.nodeValue

    # loops through threads spread across several thread groups to get list of threads
    threads = []
    for threadGroupDOM in facebookDOM.childNodes[1:]:
        for threadDOM in threadGroupDOM.childNodes:
            
            # loops through message divs to get list of messages
            messages = []
            for node in threadDOM.childNodes:
                if node.localName == 'div':

                    author = node.firstChild.firstChild.firstChild.nodeValue
                    
                    if (node.nextSibling.firstChild):
                        text = node.nextSibling.firstChild.nodeValue
                    else:
                        text =  "" # in case message is empty
                    
                    # converts time from string to datetime object
                    timeText = node.firstChild.lastChild.firstChild.nodeValue
                    time = datetime.datetime.strptime(timeText, '%A, %B %d, %Y at %I:%M%p %Z')
                    
                    messages.append(Message(author, time, text))

            # sets thread name to list of participants provided by Facebook
            threadParticipants = threadDOM.firstChild.nodeValue
            threadName = "Participants: " + str(threadParticipants)

            threads.append(Thread(threadName, messages))

    return History(historyName, threads)
