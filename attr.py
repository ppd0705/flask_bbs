class C(object):
    a = 'abc'

    def __getattribute__(self, *args, **kwargs):
        print("__getattribute__() is called")
        return object.__getattribute__(self, *args, **kwargs)

    #        return "haha"
    def __getattr__(self, name):
        print("__getattr__() is called ")
        return name + " from getattr"

    def __get__(self, instance, owner):
        print("__get__() is called", instance, owner)
        return self

    def foo(self, x):
        print(x)


class C2(object):
    d = C()



class locker:
    def __init__(self):
        print("locker.__init__() should be not called.")

    @staticmethod
    def acquire():
        print("locker.acquire() called.（这是静态方法）")

    @staticmethod
    def release():
        print("  locker.release() called.（不需要对象实例）")

def deco(cls):
    '''cls 必须实现acquire和release静态方法'''
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, cls))
            cls.acquire()
            try:
                return func()
            finally:
                cls.release()
        return __deco
    return _deco


@deco(locker)
def myfunc():
    print(" myfunc() called.")


def deco(func):
    def warpper(*args, **kw):
        print("start")
        result = func(*args, **kw)
        # 纪录结果
        print ("end")
        # return result
    #返回
    return warpper

@deco
def myfun1(param):

    print('233', 2*param)
    return 2**param

if __name__ == '__main__':
    # c = C()
    # c2 = C2()
    # print(c.a)
    # print(c.zzzzzzzz)
    # c2.d
    # print(c2.d.a)
    # a =  myfunc()
    print('-------------')
    print(myfun1(3))