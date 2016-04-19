
#异常类
class LimitError(Exception):
	def __init__(self,message):
		self._message = str(message)

	def __str__(self):
		return self._message

	def __repr__(self):
		return self._message

#利用装饰器限制python的参数数据类型
def LimitType(*typeLimit,**returnType):
	def testValueType(func):
		def wrapper(*param,**kw):
			length = len(typeLimit)
			if length != len(param):
				raise LimitError("The list of typeLimit and param must have the same length")
			for index in range(length):
				t = typeLimit[index]
				p = param[index]
				if not isinstance(p,t):
					raise LimitError("The param %s should be %s,but it's %s now!"%(str(p),type(t),type(p)))  
			res = func(*param,**kw)
			if "returnType" in returnType:
				limit = returnType["returnType"]
				if  not isinstance(res,limit):
					raise LimitError("This function must return a value that is %s,but now it's %s"%(limit,type(res) ) )
			return res
		return wrapper
	return testValueType


