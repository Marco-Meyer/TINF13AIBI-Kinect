"""
Module for handling game events.

Usage:

>>> manager = Manager() #intialize an event manager.
>>> manager.register_event("on_test") #adding a new event that functions can be attached to
>>> def pridouble(x):
...     print (x*2)
>>> manager.register_function("on_test", pridouble) #calls pridouble when "on_test" is triggered
>>> manager.dispatch("on_test", 5)
10
>>> def pritriple(x):
...     print (x*3)
>>> manager.register_function("on_test", pritriple) #multiple funcitons can be attached to one event
>>> manager.dispatch("on_test", 3)
6
9
>>> manager.poll_event("on_test")#ask if event exists
True
>>> manager.poll_event("on_derped")
False
>>> manager.unregister_function("on_test", pridouble) #remove pridouble from "on_test" event
>>> manager.unregister_event("on_test") #unregister an event and all it's functions
>>> manager.register_event("quicktest", [pridouble, pritriple]) #when registering an event, functions can be passed optionally
>>> manager.poll_all()#retuns dict of all eventname : list of functions, this is not a copy
{'quicktest': [<function pridouble at 0x02E9C858>, <function pritriple at 0x02EB02B8>]}
>>> def kwtest(x = 2): #keywords are supported
...     print (x)
>>> manager.register_event("key", [kwtest])
>>> manager.dispatch("key")
2
>>> manager.dispatch("key", x = 5)
5
"""

from collections import defaultdict

class Manager():
    """Handles events by mapping functions to event names.
    Event names are strings describing the event and are registered at runtime.
    The class can be used to register functions to events and to invoke those events.
    Invoking an event calls all functions registered to it and passes to them all of the args passed to the invoke function.
    
    """
    __slots__ = {"events", "argnames"}
    
    def __init__(self):
        self.events = {}
        self.argnames = defaultdict(lambda : "Unknown")
        
    def register_function(self, event, function):
        """Registers a function to an event."""
        self.events[event].append(function)
        
    def register_event(self, event, functions = [], argnames = None):
        """Registers an event an optionally adds functions to it."""
        self.events[event] = functions
        if argnames:self.argnames[event] = str(argnames)
    
    def unregister_function(self,event, function):
        """Removes a callback function from an event"""
        self.events[event].remove(function)
        
    def poll_event(self, event):
        """Returns all of the current functions for the event specified."""
        return event in self.events
    
    def unregister_event(self, event):
        """Removes an event entirely."""
        del(self.events[event])
        
    def poll_all(self):
        """Returns the whole events dictionary."""
        return self.events
    
    def dispatch(self, event, *args, **kwargs):
        """Calls all functions associated with an event using the arguments passed to this function."""
        [function(*args, **kwargs) for function in self.events[event]]
    def __repr__(self):
        info = "EventManager:\n"
        for e in self.events:
            info += "Event: "+e+" Args: "+self.argnames[e]+"\n"
        return info
            
manager = Manager()
if __name__ == "__main__":
    manager = Manager()#intialize an event manager.
    manager.register_event("on_test")#adding a new event that functions can be attached to
    def pridouble(x):print (x*2)
    manager.register_function("on_test", pridouble)#calls pridouble when "on_test" is triggered
    manager.dispatch("on_test", 5) #prints 10
    def pritriple(x):print (x*3)
    manager.register_function("on_test", pritriple)#multiple funcitons can be attached to one event
    manager.dispatch("on_test", 3)#prints 6 then 9

    #we can ask if events exist
    manager.poll_event("on_test")#returns true
    manager.poll_event("on_derped")#returns false

    manager.unregister_function("on_test", pridouble)#remove pridouble from "on_test" event
    manager.unregister_event("on_test")#unregister an event and all it's functions

    manager.register_event("quicktest", [pridouble, pritriple])#when registering an event, functions can be passed optionally

    print(manager.poll_all())#retuns dict of all eventname : list of functions, this is not a copy
    def kwtest(x = 2):print (x)#keywords are supported
    manager.register_event("key", [kwtest])
    manager.dispatch("key")#prints 2
    manager.dispatch("key", x = 5)#prints 5
