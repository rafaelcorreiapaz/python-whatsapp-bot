import urllib
import json as m_json
import modules
import time

bot=None

def google(terms): # !google <search term>
    '''Returns the link and the description of the first result from a google
    search
    '''
    #query = raw_input ( 'Query: ' )
    query=terms
    print "going to google %s" % query
    query = urllib.urlencode ( { 'q' : query } )
    response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
    json = m_json.loads ( response )
    results = json [ 'responseData' ] [ 'results' ]
    returnval=""
    for result in results:
        title = result['title']
        url = result['url']   # was URL in the original and that threw a name error exception
        #print ( title + '; ' + url )
        title=title.translate({ord(k):None for k in u'<b>'})
        title=title.translate({ord(k):None for k in u'</b>'})
        returnval += title + ' ; ' + url + '\n'
        
    print "returning %s" %returnval
    return returnval

def AI(jid,query,querer,group):
	time.sleep(0.2)
	global bot
	clientinfo=bot.clientsinfo[jid]
	if clientinfo['okaytotalk']:
		query=query[len("google "):]
		result=google(query)
		if group:
			result=querer+": \n"+result
		modules.sender.message_queue(jid,result)

def onMessageReceived(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
	if messageContent.lower().startswith("google "):
		AI(jid,messageContent,pushName,None)
		
def onGroupMessageReceived(messageId, jid, msgauthor, messageContent, timestamp, wantsReceipt, pushName):
	if messageContent.lower().startswith("google "):
		AI(jid,messageContent,pushName,msgauthor)

def setup(parent):
	parent.signalsInterface.registerListener("message_received", onMessageReceived)
	parent.signalsInterface.registerListener("group_messageReceived", onGroupMessageReceived)
	global bot
	bot=parent
