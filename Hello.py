import sys
import pandas as pd 
from ast import literal_eval
from InputDataFolder import capture
from flask import Flask,render_template,request
app = Flask(__name__)

#answerList will hold list of correct answers
answerList=[]

class InputDefaultData():
    ScoreDict={'Name':'Test Score'}
    name = 'temp'
    def __init__(self,classobject,d):
        self.classobject = classobject
        self.d = d

    def getObject(self):
        #self.classobject = capture.Capture()
        return self.classobject

    def __del__(self):  
        print('The destructor is called for base class')

    #Function to accept defult data
    def no_choice(self):        
        try:
            dd = pd.read_csv("defaultData.csv",converters={"Options": literal_eval})
            for i in range(len(dd)):
                self.d = self.classobject.def_func(i,dd)
                answerList.append(self.d['Answer'])
                yield self.d
        except FileNotFoundError:
                print('defaultData.csv file not found at location..')
                sys.exit(0)

    def display(self):
        print('Data captured from default data file...')
    
class InputUserData(InputDefaultData):
    def __init__(self,classobject,d,number_of_ques):
        super().__init__(classobject,d)     #use of super()
        self.number_of_ques = number_of_ques

    def __del__(self):  
        print('The destructor is called for parent class')

    #Function to accept user provided data
    def yes_choice(self):
        while True:
            try:    
                self.number_of_ques=int(input('Enter total number of questions:'))
                if self.number_of_ques <= 0:
                    raise ValueError
                    break
                for i in range (self.number_of_ques):
                    d = self.getObject().add_questions()
                    answerList.append(d['Answer'])
                    yield d
                break
            except ValueError:
                print('Please enter valid number!')
                continue
            
    def display(self):
        print('User data entered...')

def capture_answerlist_holdlist():
    ip = InputUserData(capture.Capture(),dict(),0) #demonstrating inheritance
    add_more_ques=input('Would you like to add your own questions:')   
    if add_more_ques=='N':
        holdList = [i for i in ip.no_choice()]  #using derived class object to access base class functions
        defaultData = InputDefaultData(capture.Capture(),dict())
        defaultData.display()   #method overriding
        del defaultData         #object destruction
        
    elif add_more_ques == 'Y':
        holdList = [i for i in ip.yes_choice()]
        ip.display()    #method overriding
        del ip          #object destruction
      
    else:
        print('Please enter Y/N...')
        holdList = capture_answerlist_holdlist()
    return holdList

@app.route('/')
def hello():
    return render_template('Login.html')

@app.route('/pass',methods=['POST'])
def getvalue():
    InputDefaultData.name=request.form['Name']
    return render_template('pass.html',n=InputDefaultData.name)

@app.route('/quiz')
def getquiz():
    return render_template('quiz.html',containerList=holdList)

@app.route('/result',methods=['POST'])
def getinput():
    
    #responselist is list of captured responses from user
    responselist=[]
    for i in range(len(answerList)):
        response=request.form[str(i)]
        responselist.append(response)    

    counter = [True for a,b in zip(answerList,responselist)if a==b]
    InputDefaultData.ScoreDict.update({InputDefaultData.name:len(counter)})
    df = pd.DataFrame.from_dict(InputDefaultData.ScoreDict, orient="index")
    df.to_excel("output.xlsx")
    return render_template('result.html',s=len(counter))


if __name__ == "__main__":
    holdList = capture_answerlist_holdlist()
    app.run()
