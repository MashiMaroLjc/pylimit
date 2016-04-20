
#异常类
class LimitError(Exception):
	def __init__(self,message):
		self._message = str(message)

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return self._message

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
def list_limit(*var,**info):
	default = info.get("supp",None)
	var_name_list = [ value  for value in var]
	def test_length(func):
		def wrapper(*param,**kw):
			param_length = len(param)
			if param_length != len(var_name_list):
				raise LimitError("The number of param in this function must same length as "\
				    "the number of param that you want to limit!")
			for index in range(param_length):
				var_name = var_name_list[index]
				#最小长度限制
				min_length = info.get(var_name,0)
				var_value = param[index]
				if not isinstance(var_value,list):
					raise LimitError("You can only limit the param,which is a list!Type of %s"\
					        " is %s"%(var_value,type(var_value)))
				#print("name: %s  value: %s   min_length:%s"%(var_name,var_value,min_length))
				now_length = len(var_value)
				if now_length < min_length:
					var_value += [default for num in range(min_length-now_length)]
			return func(*param,**kw)
		return wrapper
	return test_length

