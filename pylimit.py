
#异常类
class LimitError(Exception):
	def __init__(self,message):
		self._message = str(message)

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return self._message

#常熟类
class Const:

	def __init__(self,value):
		if not isinstance(value, (int, str, float)):
			raise LimitError("You only can set the value of int ,float or str!")
		self._value = value

	@property
	def value(self):
	    return self._value

	@value.setter
	def value(self,value):
		raise LimitError("You can't change the value!")
	
#利用装饰器限制python的参数数据类型
def type_limit(*typeLimit,**returnType):
	def test_value_type(func):
		def wrapper(*param,**kw):
			length = len(typeLimit)
			if length != len(param):
				raise LimitError("The list of typeLimit and param must have the same length")
			for index in range(length):
				t = typeLimit[index]
				p = param[index]
				if not isinstance(p,t):
					raise LimitError("The param %s should be %s,but it's %s now!"%(str(p),type(t()),type(p)))  
			res = func(*param,**kw)
			if "returnType" in returnType:
				limit = returnType["returnType"]
				if  not isinstance(res,limit):
					raise LimitError("This function must return a value that is %s,but now it's %s"%(limit,type(res) ) )
			return res
		return wrapper
	return test_value_type


#使用装饰器指定某个以列表或元组为参数时，限制指定长度，不够长则自动补充，可指定补充的元素
#info[value] =  length
#info[supp] = None #补充元素
#*var指定的次序跟参数中list出现的次序一样
def list_limit(*var,**info):
	default = info.get("supp",None)
	var_name_list = [ value  for value in var]
	def test_length(func):
		def wrapper(*param,**kw):
			var_index = 0
			for v in param:
				var_value = v
				if isinstance(var_value,list) and var_index < len(var_name_list[var_index]):
					var_name = var_name_list[var_index]
					var_index += 1
					#最小长度限制
					min_length = info.get(var_name,0)
					now_length = len(var_value)
					if now_length < min_length:
						var_value += [default for num in range(min_length-now_length)]
			return func(*param,**kw)
		return wrapper
	return test_length

