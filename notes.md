# Questions

## For my understanding
1. The is well commented.
1. Are there different material on different channels? (need to tell the bigger picture)
2. What does the word combi stands for?
3. Does cycle means that you ran the experiment again?
4. PXRD? how much do you use it?
5. Is matthew still around?
6. what is specific capacities and energies in cellReader?
7.

## Requirement Questions
### Functional
1. load files and plot graph
2. save graph

### Non-functional
1. Desktop application? What about web?
2. Should it be cross platform?
3. Are you concerned with how the application looks. Is it worth spending time making it pretty.

### User Stories:
Need to list down all the features. Someone needs to seat down with me to list all the features? features are like user stories. small things like


# Problems:
* change address in the beginning filepath = 'C:\\Users\\Matt\\OneDrive - McGill University\\Work\\Cells\\'. This can be done during runtime.
* one wrong move and the program crashes (if running without the console)
* file error handling (at least in plateReader)
* ability to zoom into a graph. (x and y axis scaling)

# features:
## plateReader:
* load combi cells
* load mass files
* validate file format?
* load with out mass file
* can load multiple files, when you can specify which one to use.
* zoom able map.

# Software design steps:

* understanding the Problems
* coming up with user requirement?
* research finding tools which can help us achieve what we want
* Designing architecture of the project(over-engineering but important).
* setup CI (over-engineering)
* code
* Testing (unit testing. over engineering)
* Deployment
