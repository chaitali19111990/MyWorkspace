class Capture():
        
    @staticmethod
    def add_questions():
        Dict={}
        optionList=[]
        ques=input('Enter Your Question:')
        while True:
            try:
                for i in range(3):
                    option=input('Enter Your option:')
                    if not option.strip():
                        raise ValueError
                        break
                    optionList.append(option)
                break
            except ValueError:
                print('Empty string..Please provide some value!')
                continue

        while True:
            ans=input('Please enter correct answer:')
            isValid = lambda x : True if x in optionList else False
            if isValid(ans) == False:
                print('Please enter answer from option list only!')
                continue
            else:
                break

        Dict.update({'Question':ques})
        Dict.update({'Options':optionList})
        Dict.update({'Answer':ans})
        return Dict

    @staticmethod
    def def_func(p1,p2):
        Dict={}
        Dict.update({'Question':p2.values[p1][0]})
        Dict.update({'Options':p2.values[p1][1]})
        Dict.update({'Answer':p2.values[p1][2]})
        return Dict


        