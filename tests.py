import unittest
import pandas as pd
from ast import literal_eval
from InputDataFolder import capture
import Hello

class tests(unittest.TestCase):

    def test_A(self):
        pass

    #Reading default data from csv file
    def test_def_fun(self):
        d1 = {'Question': 'How many days in week', 'Options': ['4', '6', '7'], 'Answer': '7'}
        dd = pd.read_csv("defaultData.csv",converters={"Options": literal_eval})
        d2 = capture.Capture.def_func(0,dd)
        self.assertDictEqual(d1,d2)
     
    #Validating keys of dictionary received from add_question()
    def test_add_questions(self):
        d = capture.Capture.add_questions()     
        self.assertIn('Question', d.keys())
        self.assertIn('Options', d.keys())
        self.assertIn('Answer', d.keys())

    #check whether output file is empty
    def test_IsOutputFileEmpty(self):
        d = pd.read_excel("output.xlsx",engine='openpyxl');
        self.assertEqual(d.empty,False)

if __name__ == '__main__':
    unittest.main()