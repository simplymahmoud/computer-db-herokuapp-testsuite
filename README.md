# computer-db-herokuapp-testsuite
My code to fulfil backbase assignment 

Requirements:
-------------
1- Please access the following sample aplication - http://computer-database.herokuapp.com/computers

2- Create a series of  manual test cases that cover the CRUD operation plus the edge cases. Make sure you give detailed instructions for each test case (pre conditions, steps, expected results). You can use any format you want.

3- Write scripts that would automate the manual test cases that you see fit to be included in a regression test set. You can use any scripting language and tools you want.

4- When the assessment is completed, please push the file containing the manual testcases and the automation project to github and provide us a link to the repository.

Documentation
-------------
Check file (GUI check.txt) for GUI checks, folder (Test Scenarios) for Test Scenarios, and file (Test Results.log) for Test Results.

Install Python Packages:
------------------------
Note That: you may use virtual env for this step
```
computer-db-herokuapp-testsuite$> pip install -r req.txt
```

Run the tests
---------------
```
computer-db-herokuapp-testsuite$> nosetests -xv testsuite
```
