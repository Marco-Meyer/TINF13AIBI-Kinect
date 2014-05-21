class EventManager:
    """
    Init EventManager, creates empty event list.
    """
    def __init__(self)
        self._events = []

    """
    Adds an event of the specified type to the eventlist.
    
    (Example) Types:
    0 - Userevent
    1 - Gameevent
    """
    def addEvent(self, e, type)
        self._events.append((e, type))

    """
    Returns all events in the event list. Clears event list

    (Example) Types:
    0 - Userevent
    1 - Gameevent
    """
    def popEvents(self, type)
        e = self.peekEvents(type)
        self._events = []
        
        return e
        
    """
    Returns all events in the event list. Does not clear the event list
    """
    def peekEvents(self, type)
        returnEvents = []
        for item in self._events:
            event, eventType = item
            if type == eventType
                returnEvents.append(event)
        
        return returnEvents

    """
    Returns a boolean telling if an event of the given type exists

    (Example) Types:
    0 - Userevent
    1 - Gameevent
    """
    def existsEvent(self, type)
        return len(self.peekEvents(type)) > 0