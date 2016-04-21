#Doucument 

- pylimit成员名单
- 代码示例


##pylimit成员名单

### LimitError

继承至Exception，表示使用期间可能会触发的异常类型
    
### Const

常量类，其接受一个```int``` ， ```float``` ,   ```str```类型的值，构建后只能用value访问，如果试图修改
value则会触发```LimitError```


### type_limit

一个装饰器，使用其可以约束参数的类型，越违反约束，则会触发```LimitError```

### list_limit

一个装饰器，使用其可以限制一维列表的长度，若少于该长度，则会在列表中自动填充元素。
目的是为了防止在某些情况使用列表可能会触发越界异常。

填充的内容默认是None，你也可以指定```supp```字段进行改写。

注意，若参数中没有列表类型的参数，则不会使用限制。该函数不会触发```LimitError```

### lists_limit

一个装饰器，其功能是使得二维列表的每一个元素的长度保持和指定值一致。主要是为了某些算法而设计。

使用方式与```list_limit```相似

### list_type_limit

一个装饰器，限制每一个列表的元素类型。

注意，若某个列表型的参数长度超出了你限定的长度，超出的部分则会得不到约束。
如果约束部分违反了约束，则会触发```LimitError```


##代码示例

    from pylimit import type_limit
    
    @type_limit(int,int)
    def test(x,y):
        return x + y

当然你也可以对返回值也进行约束

    @type_limit(int,int,returnType = int)
    def test2(x,y):
        return x + y


如果调用test的时候不按照要求传参数的话，则会触发```LimitError```
    
    print(test(1,'2'))
    
    >>> pylimit.LimitError: The param 2 should be <class 'int'>,but it's <class 'str'> now!
    
正常情况下

    print(1,2)
    
    >>>  3

列表限制

    @list_limit("var","var2",var=10,var2 =2,supp = 0)
    def list_l(var,var2,var3):
        print(var)
        print(var2)
        print(var3)
    
    list_l(1,[1,2,3],[4])

    >>> 1
    [1, 2, 3, 0, 0, 0, 0, 0, 0, 0]
    [4, 0]


二维列表限制

    @lists_limit("var","var2",var=3,var2=5 ,supp = 0)
    def twoD(var ,var2,var3):
    	print(var)
    	print(var2)
    	print(var3)
    
    a = [
     	[1,2],
     	[1,2,3],
    	[1,2,3,4]
    ]
    b = [
    		[1,2],
    		[1,2,3],
    		[1,2,3,4]
    	]
    twoD("2D",a,b)
    
    Output:
    2D
    [[1, 2, 0], [1, 2, 3], [1, 2, 3, 4]]
    [[1, 2, 0, 0, 0], [1, 2, 3, 0, 0], [1, 2, 3, 4, 0]]
    
    
    
列表元素类型限制
    
    @list_type_limit("var","var2",var=[int,int,str],var2=[int,float])
    def function(var,var2):
        print(var)
        print(var2)
    
    function([1,2,"a"],[2,5.14444])
    output:
    [1,2,"a"]
    [2,5.14444]

