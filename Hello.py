import sys
import pandas as pd 
from ast import literal_eval
from InputData import captureData
from flask import Flask,render_template,request
app = Flask(__name__)

#answerList will hold list of correct answers
answerList=[]

class InputData():
    d={}
    ScoreDict={'Name':'Test Score'}
    name = 'temp'
    def __init__(self):
        self.classobject = captureData.Capture()

    #Function to accept defult data
    def no_choice(self):        
        try:
            dd = pd.read_csv("defaultData.csv",converters={"Options": literal_eval})
            for i in range(len(dd)):
                d = self.classobject.def_func(i,dd)
                answerList.append(d['Answer'])
                yield d
        except FileNotFoundError:
                print('defaultData.csv file not found at location..')
                sys.exit(0)
    
    #Function to accept user provided data
    def yes_choice(self):
        while True:
            try:    
                number_of_ques=int(input('Enter total number of questions:'))
                if number_of_ques <= 0:
                    raise ValueError
                    break
                for i in range (number_of_ques):
                    d = self.classobject.add_questions()
                    answerList.append(d['Answer'])
                    yield d
                break
            except ValueError:
                print('Please enter valid number!')
                continue        

def capture_answerlist_holdlist():
    ip = InputData()
    add_more_ques=input('Would you like to add your own questions:')   
    if add_more_ques=='N':
        holdList = [i for i in ip.no_choice()]                 
    elif add_more_ques == 'Y':
        holdList = [i for i in ip.yes_choice()]
    else:
        print('Please enter Y/N...')
        holdList = capture_answerlist_holdlist()
    return holdList

@app.route('/')
def hello():
    return render_template('Login.html')

@app.route('/pass',methods=['POST'])
def getvalue():
    InputData.name=request.form['Name']   
    return render_template('pass.html',n=InputData.name)

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
    InputData.ScoreDict.update({InputData.name:len(counter)})
    df = pd.DataFrame.from_dict(InputData.ScoreDict, orient="index")
    df.to_excel("output.xlsx")
    return render_template('result.html',s=len(counter))

if __name__ == "__main__":
    holdList = capture_answerlist_holdlist()
    app.run()
