
__author__ = "fat_rabbit"
__version__ = "0.5"


class LimitError(Exception):
	"""
	The Exception maybe will be raise during you use pylimit.
	"""
	def __init__(self,message):
		self._message = str(message)

	def __str__(self):
		return self._message

	def __repr__(self):
		return self._message




class Const:
	"""
	The class of const.But only can build it for int ,float or str
	"""

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


def type_limit(*typeLimit,**returnType):
	"""

	:param typeLimit: object  you want to is limited by the type of the parameters,
	will be testing in sequence
	:param returnType: object  you want to is limited by the type of the value that will be return
	"""
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



def list_limit(*var,**info):
	"""

	:param var: str The name of key in the info which is dict
	:param info: The length of the list of restrictions.
	The value of key named "supp" is a value which will be supplement when the list less than you requirement.
	That default value is None

	For example:
	@list_limit("var","var2",var=3,var2 =2,supp = 0)
	def function(var,var2,var3):
		print(var)
		print(var2)
		print(var3)

	function([1],[1],[1])

	 output:
	 [1,0,0]
	 [1,0]
	 [1]
	"""
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



def lists_limit(*var,**info):
	"""

	:param var: str The name of key in the info which is dict
	:param info: The length of each dimension in 2D list of restrictions.
	The value of key named "supp" is a value which will be supplement when the 1D list less than you requirement.
	That default value is None

	Example:
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
	"""
	default = info.get("supp", None)
	var_name_list = [value for value in var]
	def test_length(func):
		def wrapper(*param, **kw):
			var_index = 0
			for var_value in param:
				if isinstance(var_value, list) and var_index < len(var_name_list[var_index]):
					var_name = var_name_list[var_index]
					var_index += 1
					min_length = info.get(var_name, 0)
					for child_list in var_value:
						if not isinstance(child_list,list):
							raise LimitError("You can only limit a list ,which is 2D!")
						now_length = len(child_list)
						if now_length < min_length:
							child_list += [default for num in range(min_length-now_length)]

			return func(*param, **kw)
		return wrapper
	return test_length


def list_type_limit(*key,**info):
	"""

	:param var: str  The name of key in the info which is dict
	:param info: dict var=[type1,type2] Give  a list of parameters of the same length and you
	need to limit, each element is one-to-one

	For example:
	@list_type_limit("var","var2",var=[int,int,str],var2=[int,float])
	def function(var,var2):
		print(var)
		print(var2)

	function([1,2,"a"],[2,5.14444])
	output:
	[1,2,"a"]
	[2,5.14444]
	"""
	length = len(key)
	def test(func):
		def wrapper(*param, **kw):
			index = 0
			for par in  param:
				if isinstance(par,(list,tuple)) and index < length:
					name = key[index]
					limit_list = info.get(name,[])
					index_max = min(len(limit_list),len(par))
					for limit_index in range(index_max):
						limit = limit_list[limit_index]
						var = par[limit_index]
						if not isinstance(var,limit):
							raise LimitError("The %s don't conform to the requirements!"\
							                 "  You requirements is %s"%(par,limit_list))
			return func(*param,**kw)
		return wrapper
	return test
