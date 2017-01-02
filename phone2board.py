import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.auth
import tornado.escape
import os.path
import logging 
import sys
import urllib
import json

from uuid import uuid4

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


#to do - 
# check character set of inputs (not vital as 'block' added to each user). 
# scores?






#------------------------------------------------------------------------------Main app code-------------------------------------------

class Status (object):
    currentStatus = "waitingforstart"
    currentLoginStatus = "open"
    currentTime = 90
    currentQuestion = False
    currentQuestionType = False
    clientcallbacks = []
    users = {} # users is a dictionary - names are keys, each item is a dictionary of score and (if neccesary), current question and correct or not
    globalcallbacks = []
    controlcallbacks = []
    answercounter = 0
    quiztype = ""
    def registerclient(self, callback):
        print('register client---------------------------------------------------------')
        if (callback not in self.clientcallbacks):
            self.clientcallbacks.append(callback)

    def registerglobal(self, callback):
        print('register global----------------------------------------------------------')
        if (callback not in self.globalcallbacks):
            self.globalcallbacks.append(callback)


    def registercontrol(self, callback):
        print('register control----------------------------------------------------------')
        if (callback not in self.controlcallbacks):
            self.controlcallbacks.append(callback)

    def adduser(self, name):
        if self.getStatus()=="waitingforstart":
            self.users[tornado.escape.native_str(name)]={'qnum':0,'level':0,'complete':"false",'Score':0,'answerordinal':10000, 'block':"false",'finished':"false"}
        else: 
            self.users[tornado.escape.native_str(name)]={'qnum':0,'level':0,'complete':"false",'Score':0,'answerordinal':10000, 'block':"false",'finished':"false"}
#        self.users(tornado.escape.native_str(name))
        self.notifyAddUser()

    def removeuser(self, name):
        print('removing user')
        # self.users.remove(tornado.escape.native_str(name))
        delname = tornado.escape.native_str(name)
        if (delname in self.users):
            del self.users[delname]

    def setQuestion(self, question):
        print('setquestion')
        questtype = "open"
        jsonstring ='{"type":"question","question":"'+question+'"}'
        self.clearAnswers()
        self.currentQuestion = question
        self.currentQuestionType = questtype
        self.setStatus("waitingforanswer")
        self.setLoginStatus("closed")
        self.notifyGlobal(jsonstring)
        jsonstring ='{"type":"question","status":"waitingforanswer","loginstatus":"closed"}'
        
        self.notifyControl(jsonstring)
        jsonstring ='{"type":"questionasked","qtype":"'+questtype+'"}'
        self.notifyClient(jsonstring)
     # print ("what the hell")
     #   self.notifyAnswer()

        
     
# could be named better as is doing the marking
    def setControlAnswer(self, answer):
         print('set control answer')
         answers = answer.split('/')
         print(len(answers))
         for user in self.users.keys():
            if ('answer' in self.users[user]):
                if (self.users[user]['answer']in answers):
                    self.users[user]['mark']="correct"
                else:
                    self.users[user]['mark']="incorrect"
         self.notifyGlobalAnswer()
         self.notifyUserAllAnswers()
                    
    def setCorrectFromControl(self, user):
        if (self.users[user]):
            self.users[user]['mark']="correct"
            print("does it workd")
            print(self.users[user]['mark'])
            self.notifyGlobalAnswer()
            self.notifyUserAnswerCorrect(user)

    def setIncorrectFromControl(self, user):
        if (self.users[user]):
            self.users[user]['mark']="incorrect"
            print(self.users[user]['mark'])
            self.notifyGlobalAnswer()
            self.notifyUserAnswerIncorrect(user)

    def setBlockFromControl(self, user):
        if (self.users[user]):
            self.users[user]['block']="true"
            self.notifyGlobalAnswer()
        
    def setUnblockFromControl(self, user):
        if (self.users[user]):
            self.users[user]['block']="false"
            self.notifyGlobalAnswer()

    def toggleLoginStatus(self):
        if (self.getLoginStatus()=="closed"):
            self.setLoginStatus("open")
        else:
            self.setLoginStatus("closed")
        self.notifyControlLoginStatus()

    def toggleStatus(self):
        if (self.getStatus()=="waitingforanswer"):
            self.setStatus("answersclosed")
        else:
            self.setStatus("waitingforanswer")
        self.notifyControlStatus()

    def resetGame(self):
        jsonstring = '{"type":"reset"}'
        print("what the hell")
        self.notifyClient(jsonstring)

    def setAnswer(self, answer, user):
        print('getting answer')
        print (answer)
        print (user)
        self.users[user]['answer'] = answer
        self.users[user]['answerordinal']=self.answercounter
        self.users[user]['mark']="notmarked"
        self.answercounter=self.answercounter + 1
        self.notifyAnswer()

    def setClientResult(self, level, qnum, finished, user):
        print ('gotten result')
        print (level)
        print (qnum)
        print (user)
        print (finished)
        self.users[user]['level']=int(level)
        self.users[user]['qnum']=int(qnum)
        self.users[user]['finished']=finished
        self.notifyAnswer()    
        
    def clearAnswers(self):
        self.answercounter = 0
        for user in self.users.keys():
            if ('answer' in self.users[user]):
                del self.users[user]['answer']
                self.users[user]['answerordinal']=10000
                self.users[user]['mark']="notmarked"

    def setStatus(self, status):
        self.currentStatus = status


    def setQuizType(self, quiztype):
        self.quiztype = quiztype


        
    def setLoginStatus(self, status):
        self.currentLoginStatus = status

    def setTime(self, time):
        print("SETTING TIMER________________")
        self.currentTime = time
        self.notifyGlobalTimeChange(time)
        self.notifyUserTimeChange(time)

    def notifyAddUser(self):
        print("notify add user")
        jsonstring = '{"type":"users","users":['
        print (self.users)
        for c in self.users.keys():
            jsonstring = jsonstring+'"'+c+'",'
        
        jsonstring = jsonstring[:-1]
        jsonstring = jsonstring+']}'
        self.notifyGlobal(jsonstring)
        self.notifyControlAnswer()





    def notifyAnswer(self):
        print ("notify answer")
        self.notifyGlobalAnswer()
        self.notifyControlAnswer()
        
    def notifyGlobalAnswer(self):
        print ("notify gloabla answer")
        jsonstring = '{"type":"answers","answers":['
        answerarray = self.makeAnswerArrayString()
        jsonstring = jsonstring+answerarray
        jsonstring = jsonstring+']}'
        self.notifyGlobal(jsonstring)
                
    def notifyUserAnswerCorrect(self, markedusername):
        jsonstring = '{"type":"mark","mark":"correct","markeduser":"'
        jsonstring = jsonstring+markedusername+'"}'
        self.notifyClient(jsonstring)

    def notifyUserAnswerIncorrect(self, markedusername):
        jsonstring = '{"type":"mark","mark":"incorrect","markeduser":"'
        jsonstring = jsonstring+markedusername+'"}'
        self.notifyClient(jsonstring)

    def notifyUserTimeChange(self, time):
        print ("notify user time")
        jsonstring = '{"type":"time","time":'
        jsonstring = jsonstring+time
        jsonstring = jsonstring+'}'
        self.notifyClient(jsonstring)

        
    def notifyGlobalTimeChange(self, time):
        print ("notify gloabl time")
        jsonstring = '{"type":"time","time":'
        jsonstring = jsonstring+time
        jsonstring = jsonstring+'}'
        self.notifyGlobal(jsonstring)
        
        
    def notifyUserAllAnswers(self):
        print ("notify all users")
        jsonstring = '{"type":"alluseranswers","answers":['
        answerarray = self.makeAnswerArrayString()
        jsonstring = jsonstring+answerarray
        jsonstring = jsonstring+']}'
        self.notifyClient(jsonstring)

        
    def notifyControlAnswer(self):
        print ("notify contorl answer")
        jsonstring = '{"type":"answers","answers":['
        controlanswerarray = self.makeControlArrayString()
        jsonstring = jsonstring+controlanswerarray
        jsonstring = jsonstring+']'
 #       jsonstring = jsonstring+ ',"status":"'
#        jsonstring = jsonstring+self.application.status.getstatus()+'"'
        jsonstring = jsonstring+'}'
        self.notifyControl(jsonstring)

    def notifyControlLoginStatus(self):
        print(self.getLoginStatus())
        jsonstring = '{"type":"loginstatus","loginstatus":"'
        jsonstring = jsonstring+self.getLoginStatus()
        jsonstring = jsonstring + '"}'
        self.notifyControl(jsonstring)

    def notifyControlStatus(self):
        print(self.getStatus())
        jsonstring = '{"type":"status","status":"'
        jsonstring = jsonstring+self.getStatus()
        jsonstring = jsonstring + '"}'
        self.notifyControl(jsonstring)


    def makeAnswerArrayString (self):
        if self.quiztype == "multiq":
            sortedlist = self.getMultiqSortedUserList()
        else:    
            sortedlist = self.getSortedUserList()
        jsonstring = ""
        #for c in self.users.keys():
        #self.application.quiztype
        for c in sortedlist:
            if self.quiztype == "multiq":
                jsonstring = jsonstring+'['
                jsonstring = jsonstring+'"'+c[0]+'",'
                jsonstring = jsonstring+'"no answer",'
                jsonstring = jsonstring+'"'+str(c[1]['answerordinal'])+'",'
                jsonstring = jsonstring+'"'+str(c[1]['level'])+'",'
                jsonstring = jsonstring+'"'+str(c[1]['block'])+'",'
                jsonstring = jsonstring+'"'+str(c[1]['qnum'])+'",'
                jsonstring = jsonstring+'"'+str(c[1]['finished'])+'"],'
            else:
                if ('answer' in c[1]):
                    jsonstring = jsonstring+'['
                    jsonstring = jsonstring+'"'+c[0]+'",'
                    jsonstring = jsonstring+'"'+c[1]['answer']+'",'
                    jsonstring = jsonstring+'"'+str(c[1]['answerordinal'])+'",'
                    jsonstring = jsonstring+'"'+c[1]['mark']+'",'
                    jsonstring = jsonstring+'"'+str(c[1]['block'])+'"],'
        jsonstring = jsonstring[:-1]
        return jsonstring

    def getSortedUserList (self):
        print("-------------------------------------")
        listfromusers = self.users.items()
        print(listfromusers)
        sortedlist = sorted(listfromusers, key=lambda usered: usered[1]['answerordinal'])
        print(sortedlist)
        return sortedlist

    def getMultiqSortedUserList (self):
        listfromusers = self.users.items()
        sortedlist = sorted(listfromusers, key=lambda usered: (usered[1]['level'], usered[1]['qnum'],usered[1]['answerordinal']), reverse = True)
        print(sortedlist)
        return sortedlist

    
    def makeControlArrayString (self): 
        jsonstring = ""
        if self.quiztype == "multiq":
            jsonstring = self.makeMultiqControlArrayString()
        else:
            sortedlist = self.getSortedUserList()
            for c in sortedlist:
                jsonstring = jsonstring+'['
                jsonstring = jsonstring+'"'+c[0]+'",'
                if ('answer' in c[1]):
                    jsonstring = jsonstring+'"'+c[1]['answer']+'",'
                    jsonstring = jsonstring+'"'+str(c[1]['answerordinal'])+'",'
                    jsonstring = jsonstring+'"'+c[1]['mark']+'",'
                    jsonstring = jsonstring+'"'+str(c[1]['block'])+'"],'
                else: 
                    jsonstring = jsonstring+'"noanswer",'
                    jsonstring = jsonstring+'"'+str(c[1]['answerordinal'])+'",'
                    jsonstring = jsonstring+'"nomark",'
                    jsonstring = jsonstring+'"'+str(c[1]['block'])+'"],'
            jsonstring = jsonstring[:-1]
        return jsonstring

    def makeMultiqControlArrayString (self):
        jsonstring = ""
        sortedlist = self.getSortedUserList()
        for c in sortedlist:
            jsonstring = jsonstring+'['
            jsonstring = jsonstring+'"'+c[0]+'",'
            if ('answer' in c[1]):
                jsonstring = jsonstring+'"'+c[1]['answer']+'",'
                jsonstring = jsonstring+'"'+str(c[1]['answerordinal'])+'",'
                jsonstring = jsonstring+'"'+c[1]['mark']+'",'
                jsonstring = jsonstring+'"'+str(c[1]['block'])+'"],'
            else: 
                jsonstring = jsonstring+'"noanswer",'
                jsonstring = jsonstring+'"'+str(c[1]['answerordinal'])+'",'
                jsonstring = jsonstring+'"'+str(c[1]['level'])+'",'
                jsonstring = jsonstring+'"'+str(c[1]['block'])+'",'
                jsonstring = jsonstring+'"'+str(c[1]['qnum'])+'"],'
        jsonstring = jsonstring[:-1]
        print (jsonstring)
        print ("make controll array string")
        return jsonstring





        
    def notifyGlobal(self, message):
        for c in self.globalcallbacks:
            print('globalcallbacks')
            print(message)
            print(c)
            c(message)

        self.globalcallbacks=[]

    def notifyControl(self, message):
        for c in self.controlcallbacks:
            print('controlcallbacks')
            print(message)
            print(c)
            c(message)

        self.controlcallbacks=[]

    def notifyClient(self, message):
        for c in self.clientcallbacks:
            print('controlcallbacks')
            print(message)
            print(c)
            c(message)

        self.clientcallbacks=[]

    def getUsers(self):
        return self.users.keys()

    def getStatus(self):
        return self.currentStatus

    def getTime(self):
        return self.currentTime

    def getLoginStatus(self):
        return self.currentLoginStatus

    def getQuestion(self):
        return self.currentQuestion

    def getQuizType(self):
        return self.quizType
    
    def getQuestionType(self):
        return self.currentQuestionType






#----------------------------------------------------------status handlers-------------------------
# these handle the asynch hooks from the pages and sending messages to the pages
# a lot of shared code here - I'm sure this could be better!

class ClientStatusHandler(tornado.web.RequestHandler):
     @tornado.web.asynchronous
     @tornado.gen.engine
     def get(self):
         print("register client")
         self.application.status.registerclient(self.on_message)

     def on_message(self, message):
         print("client message sent")
         print(message)
         self.write(message)
         self.finish()

class GlobalStatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        print("reggister gloabl")
        self.application.status.registerglobal(self.on_message)

    def on_message(self, message):
        print("global message sent")
        print(message) 
        self.write(message)
        self.finish()

class ControlStatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        print("registeredd control")          
        self.application.status.registercontrol(self.on_message)

    def on_message(self, message):
        print("control message sent")
        print(message)
        self.write(message)
        self.finish()

# message handlers - recieves messages from the pages (currently only control and client)




class ControlMessageHandler(tornado.web.RequestHandler):
    def get(self):
        messagetype = self.get_argument("type")
        if messagetype=="question":
            question = urllib.parse.unquote(self.get_argument("question"))
            self.application.status.setQuestion(question)
        if messagetype=="time":
            time = urllib.parse.unquote(self.get_argument("time"))
            self.application.status.setTime(time)
        if messagetype=="controlanswer":
            answer = urllib.parse.unquote(self.get_argument("answer"))
            self.application.status.setControlAnswer(answer)
        if messagetype=="markcorrect":
            name = urllib.parse.unquote(self.get_argument("id"))
            self.application.status.setCorrectFromControl(name)
        if messagetype=="markincorrect":
            name = urllib.parse.unquote(self.get_argument("id"))
            self.application.status.setIncorrectFromControl(name)
        if messagetype=="block":
            name = urllib.parse.unquote(self.get_argument("id"))
            self.application.status.setBlockFromControl(name)
        if messagetype=="unblock":
            name = urllib.parse.unquote(self.get_argument("id"))
            self.application.status.setUnblockFromControl(name)
        if messagetype=="toggleloginstatus":
            self.application.status.toggleLoginStatus()
        if messagetype=="togglestatus":
            self.application.status.toggleStatus()
        if messagetype=="resetgame":
            self.application.status.resetGame();
        self.finish()


class ClientMessageHandler(tornado.web.RequestHandler):
    def get(self):
        messagetype = self.get_argument("type")
        if messagetype=="answer":
            currentstatus = self.application.status.getStatus()
            if (currentstatus=="waitingforanswer"):
                answer = urllib.parse.unquote(self.get_argument("answer"))
                user = tornado.escape.native_str(self.get_secure_cookie("username"))
                self.application.status.setAnswer(answer,user)
        if messagetype=="clientmarked":
            currentstatus = self.application.status.getStatus()
            if (currentstatus=="waitingforanswer"):
                user = tornado.escape.native_str(self.get_secure_cookie("username"))
                level = self.get_argument("level");
                qnum = self.get_argument("qnum");
                finished = self.get_argument("finished");
                self.application.status.setClientResult(level, qnum, finished, user);
        self.finish()



class GlobalMessageHandler(tornado.web.RequestHandler):
    def get(self):
        messagetype = self.get_argument("type")
        if messagetype=="requestanswers":
            self.application.status.notifyAnswer()
        self.finish()

     
# -   template handlers -------------  pages that are actually called by the browser. 
       
class ClientPageHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get(self):
        session = uuid4()
        


class LoginHandler(ClientPageHandler):
    def get(self):
        #print (self.application.gamefile)
        #print (self.application.gamefile["quiztype"])
        if self.application.status.getLoginStatus()=="open":
            self.render('login.html')
        elif self.get_secure_cookie("username"):
            print(self.application.status.getStatus())
            self.redirect("/")
        else:
            print(self.application.status.getStatus())
            self.render('gamestarted.html')

    def post(self):
        # if client already has a username set, remove it from the list before creating a new username
        if self.get_secure_cookie("username"):
            self.application.status.removeuser(self.current_user)   
        # create new user
        self.set_secure_cookie("username",self.get_argument("username"),expires_days=1)
        self.redirect("/")

class ClientWelcome(ClientPageHandler):
    @tornado.web.authenticated
    def get(self):
        session = uuid4()
        self.application.status.adduser(self.current_user)
        currentstatus = self.application.status.getStatus()
        currenttime = self.application.status.getTime()
        questionarray = self.application.questionarray
        currentquestiontype = self.application.status.getQuestionType()
        clientpage = self.application.quiztypes[self.application.quiztype]['client_page']
        self.render(clientpage,session=session,user=self.current_user, status=currentstatus, questiontype=currentquestiontype,time=currenttime, levels = questionarray)

class ControlPageHandler(tornado.web.RequestHandler):
    def get(self):
     #   users = self.application.status.getUsers()
      #  userstring = "','".join(str(thisuser) for thisuser in users)
        controlstring = self.application.status.makeControlArrayString()
        currentstatus = self.application.status.getStatus()  
        currentloginstatus = self.application.status.getLoginStatus()
        currenttime = self.application.status.getTime()
        quiztype = "'" + self.application.quiztype + "'"
        questionarray = self.application.questionarray
        answerarray = self.application.answerarray
        page = self.application.quiztypes[self.application.quiztype]["control_page"]
        self.render(page,teams="["+str(controlstring)+"]", status=currentstatus, loginstatus=currentloginstatus, time=currenttime, quiztype = quiztype, questionarray = questionarray, answerarray = answerarray)

     
class GlobalPageHandler(tornado.web.RequestHandler):
    def get(self):
        users = self.application.status.getUsers()
        userstring = '","'.join(str(thisuser) for thisuser in users)
        currentstatus = self.application.status.getStatus()  
        currentquestion = self.application.status.getQuestion()
        currentanswers = self.application.status.makeAnswerArrayString()
        currenttime = self.application.status.getTime()
        globalpage = self.application.quiztypes[self.application.quiztype]["global_page"]
        # should add extra [ ] for current answers string (as in teams) - currently done in javascript
        self.render(globalpage,teams='["'+str(userstring)+'"]', status=currentstatus, question=currentquestion, answers=currentanswers,time=currenttime)



class Application(tornado.web.Application):
    def __init__(self):
        self.status = Status()
#        self.gametype = "default"
        print('init')
        handlers = [
            (r'/',ClientWelcome),
            (r'/control',ControlPageHandler),
            (r'/global',GlobalPageHandler),
            (r'/login',LoginHandler),
            (r'/clientstatus',ClientStatusHandler),
            (r'/globalstatus',GlobalStatusHandler),
            (r'/controlstatus',ControlStatusHandler),
            (r'/controlmessage',ControlMessageHandler),
            (r'/clientmessage',ClientMessageHandler),
            (r'/globalmessage',GlobalMessageHandler),


        ]

        settings = {
            'template_path':'./templates',
            'static_path':'./static',

            'cookie_secret':'123456',
            'login_url':'/login',
            'xsft_cookies':True,
            'debug':True,
        }

        ## states which pages should be served for each type of quiz. 
        self.quiztypes = {
            'default':{"client_page":"default_client.html",
                       "global_page":"default_global.html",
                       "control_page":"default_control.html"},
            'fixed_answers':{"client_page":"default_client.html",
                             "global_page":"default_global.html",
                             "control_page":"default_control.html"},
            'open_answers':{"client_page":"default_client.html",
                            "global_page":"default_global.html",
                            "control_page":"default_control.html"},
            'fixed_timed':{"client_page":"timed_client.html",
                           "global_page":"timed_global.html",
                           "control_page":"timed_control.html"},
            'open_timed':{"client_page":"timed_client.html",
                           "global_page":"timed_global.html",
                           "control_page":"timed_control.html"},
            'multiq':{"client_page":"multiq_client.html",
                           "global_page":"multiq_global.html",
                           "control_page":"multiq_control.html"}



        }
        
        tornado.web.Application.__init__(self, handlers,**settings)


if __name__ == '__main__':
#   tornado.options.parse_command_line()
    def set_defaults():
        app.quiztype = "default"
        app.notes = "Open ended questions can be entered in control pages. Answers can be marked individualy or by entering an answer in the control page."
        app.questionarray = "{}"
        app.answerarray = "{}"

    
    app = Application()
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1]) as json_data:
                app.gamefile = json.load(json_data)
                json_data.close()
                app.quiztype = app.gamefile["quiztype"]
                if "notes" in app.gamefile:
                    app.notes = app.gamefile["notes"]
                if "questionarray" in app.gamefile:
                    app.questionarray = app.gamefile["questionarray"]
                else:
                    app.questionarray = "{}"
                if "answerarray" in app.gamefile:
                    app.answerarray = app.gamefile["answerarray"]
                else:
                    app.answerarray = "{}"    
        except:
            print("not a valid json file, using defaults")
            set_defaults()
    else:
        print("no file given - using defaults")
        set_defaults()
        
    app.status.setQuizType(app.quiztype)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



