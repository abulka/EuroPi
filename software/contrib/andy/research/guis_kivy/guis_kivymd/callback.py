handler = None

# create decorator for method fred
def fred_decorator(func):
    global handler

    def wrapper(self):
        print("before")
        func(self)
        print("after")
    handler = wrapper
    return wrapper


class A:
    @fred_decorator
    def fred(self):
        print("fred")

a = A()
a.fred()
handler(a) # aha - have to pass self in
