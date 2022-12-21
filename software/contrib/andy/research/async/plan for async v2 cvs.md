# Plan for async v2 cvs

whenever you set the value of e.g. cv 1:
- create a task to do an event_cv1.set()

in the ui each led has its own task def which loops:
- waits for event_cv1
- sets the led colour according to the value of cv1
- clears the event_cv1

However this does risk the cv's coming on independently and not all as one
block.  I think this is ok though. We'll see.

