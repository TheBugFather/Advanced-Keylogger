## Contributing to the project

---
### Coding Conventions
- Biggest rule is to **comment your code**!
  - Provide a brief description of line of code in sentence format without periods and avoiding fluff words
  - Also consider what the purpose the line code has in relation to the function it resides in
  - Not necessarily everything needs to be commented, say for example a bunch of regular expressions are being compiled.
    Instead of commenting every one, logically group them and have a single comment at the top of that grouping

  <br>
- For the most part my code has very tight pep8 compliance
- A few things I do different on personal projects:
  - Wrap comments # like this #
  - 100 character max lines, pylint is fine with it but there are recommendations for 79 character lines
  
  <br>
- To better understand my formatting, check out any of my projects
- No dead / commented out code should be in a pull request under any circumstances
- Put a space between chunks of logic, also do not put logic on the same line like "if foo == bar: print('foobar')"
- Confirm formatting with Pylint, does not have to be perfect and false positives can occur with 
  list comprehensions and when external imports are not installed, usually in the 9/10 area is good
- The goal is to achieve maximum readability and documentation

### New code / feature suggestions
- Code improvements are welcomed with things to keep in mind
  - Not looking for major changes that deviate from the original concept
  - Not looking for "clever" features that are unnecessarily complex
  - New features should not cause issues with current ones and should be able to integrate without major changes 

### What to do after experiencing bug
- Open the issues tab and make sure it does not already exist
- If it does not exit open a new issue:
  - Make sure to provide as much information as possible
  - Suggest steps for replication of the bug

### What to do if you decided to fix a bug
- Open up a pull request
  - ensure full context of the nature of the bug, the cause, and how it is fixed are provided