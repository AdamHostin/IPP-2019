#!/usr/bin/env python3.6
from sys import *
import xml.etree.ElementTree as ET
import re
import fileinput

"""If argument type is not label exit with exit code 32"""
def check_if_label(argument):
	if argument.attrib["type"]!="label":
		exit(32)

"""Check if frame is given correctly also check ig LF is not empty and TF is inicialized"""
def check_frame(frame):
	if frame=="GF":
		return 
	elif frame=="LF":
		if LF:
			return
		else:
			exit(55)
	elif frame=="TF":
		if TF!=None:
			return
		else:
			exit(55)
	else:
		exit(32)


"""Check if correct type is given"""
def check_type(argument):
	if argument.attrib["type"]!="type":
		exit(32)
	if ((argument.text=="int") or (argument.text=="string") or (argument.text=="bool")):
		return argument.text
	else:
		exit(32)


"""Check if symb is bool. If symbol is type bool function returns python representation of bool else returns value of symbol"""
def check_if_bool(my_list):

	if my_list[0]=="bool":
		if my_list[1]=="true":			
			return True

		elif my_list[1]=="false":
			return False

		else:
			exit(32)
	else:
		return my_list[1]

"""Check if argument is variable and returns its type and value"""
def check_var(argument):
	
	if (('@' in argument.text) and (argument.attrib["type"]=="var")):
		splited_arg=argument.text.split("@",1)
		check_frame(splited_arg[0])
		if splited_arg[0]=="GF":
			if splited_arg[1] in GF:
				if GF[splited_arg[1]][0]=="int":

					try:
						my_return_int=int(GF[splited_arg[1]][1])
					except Exception:
						exit(32)
					
					return ["int",my_return_int]

				elif GF[splited_arg[1]][0]=="bool":
					if GF[splited_arg[1]][1]=="true":
						return [GF[splited_arg[1]][0],"true"]
					elif GF[splited_arg[1]][1]=="false":
						return [GF[splited_arg[1]][0],"false"]
					elif isinstance(argument.text, bool):
						return ["bool", argument.text.lower()]
					else:
						exit(32)

				elif GF[splited_arg[1]][0]=="string":
					return [GF[splited_arg[1]][0],GF[splited_arg[1]][1]]
				elif GF[splited_arg[1]][0]=="nil":
					return [GF[splited_arg[1]][0],GF[splited_arg[1]][1]]
				elif GF[splited_arg[1]][0]=="":
					return ["",""]
				else:
					exit(32)
			else:
				exit(54)

		elif splited_arg[0]=="LF":
			if splited_arg[1] in LF[-1]:
				if LF[-1][splited_arg[1]][0]=="int":
					return ["int",int(LF[-1][splited_arg[1]][1])]
				elif LF[-1][splited_arg[1]][0]=="bool":
					if LF[-1][splited_arg[1]][1]=="true":
						return [LF[-1][splited_arg[1]][0],"true"]
					elif LF[-1][splited_arg[1]][1]=="false":
						return [LF[-1][splited_arg[1]][0],"false"]
					elif isinstance(argument.text, bool):
						return ["bool", argument.text]
					else:
						exit(32)
				elif LF[-1][splited_arg[1]][0]=="string":
					return [LF[-1][splited_arg[1]][0],LF[-1][splited_arg[1]][1]]
				elif LF[-1][splited_arg[1]][0]=="nil":
					return [LF[-1][splited_arg[1]][0],LF[-1][splited_arg[1]][1]]
				elif LF[-1][splited_arg[1]][0]=="":
					return ["",""]
				else:
					exit(32)
			else:
				exit(54)

		elif splited_arg[0]=="TF":
			if splited_arg[1] in TF:
				if TF[splited_arg[1]][0]=="int":
					return ["int",int(TF[splited_arg[1]][1])]
				elif TF[splited_arg[1]][0]=="bool":
					if TF[splited_arg[1]][1]=="true":
						return [TF[splited_arg[1]][0],"true"]
					elif TF[splited_arg[1]][1]=="false":
						return [TF[splited_arg[1]][0],"false"]
					elif isinstance(argument.text, bool):
						return ["bool", argument.text]
					else:
						exit(32)
				elif TF[splited_arg[1]][0]=="string":
					return [TF[splited_arg[1]][0],TF[splited_arg[1]][1]]
				elif TF[splited_arg[1]][0]=="nil":
					return [TF[splited_arg[1]][0],TF[splited_arg[1]][1]]
				elif TF[splited_arg[1]][0]=="":
					return ["",""]
				else:
					exit(32)
			else:
				exit(54)
	else:
		exit(32)

"""Check if argument is symbol and returns its type and value"""
def check_symb(argument, from_function="default"):
	
	if ((argument.attrib['type']=="nil") and argument.text=="nil") :
		if argument.text==None:
			return exit(32)
		return ["nil","nil"]
	elif (argument.attrib['type']=="bool"):
		if argument.text==None:
			return exit(32)
		if (argument.text=="true") :
			return ["bool","true"]
		elif  (argument.text=="false"):
			return ["bool","false"]
		elif isinstance(argument.text, bool):
			return ["bool", argument.text]
		else:
			exit(32)
	elif (argument.attrib['type']=="string"):
		if argument.text==None:
			return ["string",""]
		tmp_symb = argument.text
		tmp_symb = re.sub(r"(\\\d{3})", "", tmp_symb)
		if re.sub(r"[^#\\\s]+", "", tmp_symb) != "":
			exit(32)
		else:
			try:
				tmp_symb = argument.text
				
				tmp_escape_seqence_list=re.findall(r"(\\\d{3})", tmp_symb)
				for i in range(0,len(tmp_escape_seqence_list)):
					tmp_escape_seqence_list[i]= re.sub(r"\\","",tmp_escape_seqence_list[i])
				tmp_splited_string = re.split(r"\\\d{3}", tmp_symb)
				i=1
				string=tmp_splited_string[0]
				
				for number in tmp_escape_seqence_list:
					if number=="":
						continue
					else:
						my_integer=int(number)
						string+= chr(my_integer) + tmp_splited_string[i]
						i+=1
				return ["string",string]
			except Exception:
				return ["string", argument.text]

	elif (argument.attrib['type']=="int"):
		if argument.text==None:
			return exit(32)
		if re.sub(r"[-]?[\d]+", "", argument.text) != "":
			exit(32)
		return ["int",int(argument.text)]
	else:
		my_list= check_var(argument)
		if from_function=="TYPE":
			return my_list

		if ((my_list[0]!="string") and (my_list[1]=="")):
			exit(56)
		else:
			return my_list





"""Has no input create string from a file"""
def create_my_string_from_STDIN():
	string=""
	while True:
		line = stdin.readline()
		string+=line
		if not line:
			break
	return (string)

"""If --input= option was given function returns file name else function returns string with content of a file"""
def create_my_string_from_file(option):
	
	for arg in argv[1:]:
		if (re.match(option + ".*",arg))!=None:
			
			splited_arg=arg.split("=",1)
			file_name=splited_arg[1]
			if option=="--input=":
				return file_name
		
			try:
				with open(file_name , 'r') as file:
					string=""
					for line in file:
						string+= line
					
					return (string)
			except Exception:
				exit(11)
	exit(10)
	
"""Function prepares label dictionary and instruction dictionary"""
def prepare_dicts(my_source_string):
	
	program=ET.fromstring(my_source_string)
	if ((program.tag!="program") or (program.attrib['language']!="IPPcode19")):
		exit(32)
	i=0;
	orders=[]
	for instruction in program:
		if int(instruction.attrib['order']) in orders:
			exit(32)
		else:
			orders.append(int(instruction.attrib['order']))
			
		if (int(instruction.attrib['order'])>i):
			i=int(instruction.attrib['order'])

		instruction_dict.update({int(instruction.attrib["order"]):instruction})


		if (instruction.attrib['opcode'].upper()=="LABEL"):
			if (len(instruction)==1):
				if (instruction[0].text) in label_dict:
					exit(52)
				elif instruction[0].attrib['type']!="label":
					exit(32)
				else:
					label_dict[(instruction[0].text)]=instruction.attrib['order']
	return (i)


"""Writes help and exit with exit code 0"""
def print_help():
	print("Brief descriotion of script otptions")
	print("--source= sets destination of a file with source code, sorce code is xml\n")
	print("--input= sets destination of a file with input for interpreted code\n")
	print("  Note:At least one of the otptions above has to be set. If one option is missing script alter it with input from stdin\n")
	print("--stats= sets destination for stats. If user want to use stati extension options it is a mandatory option\n")
	print("--insts writes number of interpreted instructions to a file seted in --stats= option\n")
	print("--vars writes number of maximum initialized variables in all frames together\n")
	exit(0)


#1 = input from stdin
#2 = source from stdin
#3 = input and sorce are given in files
"""Check if argument combination is valid. Returns numbers above."""
def check_args():

	stats_file_check=False
	statp_chceck=False
	check_source=False
	check_input=False

	if (len(argv)>6):
		exit(10)
	if ((len(argv)==2) and (argv[1]=="--help")):
		print_help()

	for arg in argv[1:]:
		if (re.fullmatch("--source=.*",arg)!=None):		
			check_source=True
			pass
		elif (re.fullmatch("--input=.*",arg)!=None):
			check_input=True
			pass
		elif ((arg=="--insts") or (arg=="--vars")):
			statp_chceck=True
		elif (re.fullmatch("--stats=.*",arg)!=None):
			stats_file_check=True
			pass
		else:
			exit(10)
	if (stats_file_check != statp_chceck):		
		exit(10)
	if ((check_source==True) and (check_input==False)):
		return(1)
	elif ((check_source==False) and (check_input==True)):
		return(2)
	elif ((check_source==True) and (check_input==True)):
		return(3)
	else:
		exit(10)
"""Function handles DEFVAR"""
def defvar_function():
	if (('@' in instruction_dict[i][0].text) and (instruction_dict[i][0].attrib["type"]=="var")):
		splited_arg = instruction_dict[i][0].text.split("@",1)
		if (splited_arg[0]=="GF"):
			if splited_arg[1] not in GF:
				GF[splited_arg[1]]=["",""]
			else:
				exit(52)
		elif (splited_arg[0]=="LF"):
			if LF:
				if splited_arg[1] not in LF[-1]:
					LF[-1][splited_arg[1]]=["",""]
				else:
					exit(52)
			else:
				exit(55)

		elif (splited_arg[0]=="TF"):
			if TF!=None:
				if splited_arg[1] not in TF:
					TF[splited_arg[1]] = ["",""]
				else:
					exit(52)
			else:
				exit(55)
		else:
			exit(32)
	else:
		exit(32)
"""STATI extension function counts number of inicialiazed variables in each frame."""
def count_variables(curent_max):
	curent_value=0
	x=0
	y=0
	z=0
	try:
		for key, value in GF.items():
			try:
				if ((value[0]!="") and (value[0])!=""):
					x+=1
			except Exception:
				pass
	except Exception:
		x=0
	try:
		for dictionary in LF:
			for key,value in dictionary:
				
				try:
					if ((value[0]!="") and (value[1])!=""):
						y+=1
				except Exception:
					pass
	except Exception:
		y=0
	try:
		for key, value in TF.items():
			try:
				if ((value[0]!="") and (value[0])!=""):
					z+=1
			except Exception:
				pass
	except Exception:
		z=0
	curent_value=x+y+z
	if curent_value>curent_max:
		return curent_value
	else:
		return curent_max
		
"""STATI output handler"""
def STATI_output(inits_output,vars_output):
	for file_arg in argv[1:]:
		if (re.match("--stats=.*",file_arg))!=None:
			
			splited_arg=file_arg.split("=",1)
			file_name=splited_arg[1]
		
			try:
				with open(file_name, 'w') as file:
					for arg in argv[1:]:
						if (arg=="--insts"):
							file.write(str(inits_output) + "\n")
						elif (arg=="--vars"):
							file.write(str(vars_output) + "\n")
						else:
							pass
			except Exception:
				exit(11)
			return



label_dict={}
instruction_dict={}
GF={}
LF=[]
zasobnik_volani=[]
datovy_zasobnik=[]
TF=None
read_counter=0
number_of_interpreted_instructions=0
number_of_variables=0

my_input_resolver=check_args()
#1 = input nacitaj zo standarnteho vstupu
#2 = source nacitaj zo stdin
#3 = vsetko je ok
#print(my_input_resolver)
if (my_input_resolver==1):
	my_source_string=create_my_string_from_file("--source=")
	input_flag=True
	pass
elif (my_input_resolver==2):
	my_input_string=create_my_string_from_file("--input=")
	my_source_string=create_my_string_from_STDIN()
	input_flag=False
	pass
elif (my_input_resolver==3):
	my_source_string=create_my_string_from_file("--source=")
	my_input_string=create_my_string_from_file("--input=")
	input_flag=False

read_counter=0

number_of_instructions=prepare_dicts(my_source_string)

i=int(1)
while (i < (number_of_instructions+1)):
	

	if (i) not in instruction_dict:
		
		exit(32)
		continue
	
	
	if (int(instruction_dict[i].attrib['order'])==i):

		number_of_interpreted_instructions+=1
		if (len(instruction_dict[i])==0):
			if (instruction_dict[i].attrib['opcode'].upper()=='RETURN'):

				try:
					i=zasobnik_volani[-1]
					zasobnik_volani.pop()
				except Exception:
					exit(56)
				continue
				
			elif  (instruction_dict[i].attrib['opcode'].upper()=='CREATEFRAME'):
				TF={}

			elif (instruction_dict[i].attrib['opcode'].upper()=='POPFRAME'):
				if LF:
					TF=LF.pop()
				else:
					exit(55)
				
			elif (instruction_dict[i].attrib['opcode'].upper()=='BREAK'):
				useless_val= stderr.write("pozicia v kodu: " + str(i))
			elif  (instruction_dict[i].attrib['opcode'].upper()=='PUSHFRAME'):
				if TF!=None:
					LF.append(TF)
					TF=None
				else:
					exit(55)
			else:
				exit(32)


		elif (len(instruction_dict[i])==1):


			if (instruction_dict[i].attrib['opcode'].upper()=='DEFVAR'):
				defvar_function()
		
				
			elif (instruction_dict[i].attrib['opcode'].upper()=='LABEL'):
				pass
			elif  (instruction_dict[i].attrib['opcode'].upper()=='CALL'):
				check_if_label(instruction_dict[i][0])
				zasobnik_volani.append(i+1)
				try:
					i=int(label_dict[instruction_dict[i][0].text])+1
				except Exception:
					exit(52)
				continue
				
			elif (instruction_dict[i].attrib['opcode'].upper()=='JUMP'):
				check_if_label(instruction_dict[i][0])
				try:
					i=int(label_dict[instruction_dict[i][0].text])
				except Exception:
					exit(52)
				continue

				
			elif (instruction_dict[i].attrib['opcode'].upper()=='PUSHS'):
				check_symb(instruction_dict[i][0])
				try:
					datovy_zasobnik.append([instruction_dict[i][0].attrib['type'],instruction_dict[i][0].text])
				except Exception:
					exit(32)
			elif  (instruction_dict[i].attrib['opcode'].upper()=='POPS'):
				check_var(instruction_dict[i][0])
				if len(datovy_zasobnik)==0:
					exit(56)
				splited_arg = datovy_zasobnik[-1][1].split("@",1)
				
				if splited_arg[0]=="GF":
					datovy_zasobnik[-1][0]=GF[splited_arg[1]][0]
					datovy_zasobnik[-1][1]=GF[splited_arg[1]][1]
					
				elif splited_arg[0]=="LF":
					datovy_zasobnik[-1][0]=LF[-1][splited_arg[1]][0]
					datovy_zasobnik[-1][1]=LF[-1][splited_arg[1]][1]
				elif splited_arg[0]=="TF":
					datovy_zasobnik[-1][0]=TF[splited_arg[1]][0]
					datovy_zasobnik[-1][1]=TF[splited_arg[1]][1]
				else:
					pass

				splited_arg = instruction_dict[i][0].text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=[datovy_zasobnik[-1][0],datovy_zasobnik[-1][1]]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=[datovy_zasobnik[-1][0],datovy_zasobnik[-1][1]]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=[datovy_zasobnik[-1][0],datovy_zasobnik[-1][1]]
				else:
					exit(32)
				del datovy_zasobnik[-1]
			elif  (instruction_dict[i].attrib['opcode'].upper()=='EXIT'):
				number_of_variables=count_variables(number_of_variables)
				STATI_output(number_of_interpreted_instructions,number_of_variables)
				if (instruction_dict[i][0].attrib["type"]=="int"):

					try:
						int_code=int(instruction_dict[i][0].text)
					except Exception:
						exit(32)
					
					
					if ((int_code>=0) and (int_code < 50)):
						exit(int_code)
					else:
						exit(57)
					
				elif (instruction_dict[i][0].attrib["type"]=="var"):
					var_content=check_var(instruction_dict[i][0])
					if var_content!=None:
						if var_content[0]=="int":
							int_code=var_content[1]
							if ((int_code>=0) and (int_code < 50)):
								exit(int_code)
							else:
								exit(57)
						elif ((var_content[0]=="") and (var_content[1]=="")):
							exit(56)
						else:
							exit(57)
					else:
						exit(54)
				else:
					exit(53)

			elif (instruction_dict[i].attrib['opcode'].upper()=='DPRINT'):
				symb_content=check_symb(instruction_dict[i][0])
				if symb_content!=None:
					useless_val=stderr.write("pozicia v kodu: " + str(i))
				else:
					exit(54)
			elif (instruction_dict[i].attrib['opcode'].upper()=='WRITE'):
				symb_content=check_symb(instruction_dict[i][0])

				if symb_content[1]=="nil" and symb_content[0]=="nil" :
					pass
				elif symb_content[1]!=None:
					print (symb_content[1], end='')
				else:
					exit(54)
			else:
				exit(32)

		elif (len(instruction_dict[i])==2):
			for argument in (instruction_dict[i]):
				if argument.tag=="arg1":
					argument1=argument
				elif argument.tag=="arg2":
					argument2=argument
				else:
					exit(32)

			if  (instruction_dict[i].attrib['opcode'].upper()=='MOVE'):
				check_var(argument1)
				symb_content=check_symb(argument2)

				if symb_content==None:
					exit(54)
				else:
					splited_arg=argument1.text.split("@",1)
					if splited_arg[0]=="GF":
						GF[splited_arg[1]]=symb_content
					elif splited_arg[0]=="LF":
						LF[-1][splited_arg[1]]=symb_content
					elif splited_arg[0]=="TF":
						TF[splited_arg[1]]=symb_content
					else:
						exit(32)

			elif (instruction_dict[i].attrib['opcode'].upper()=='STRLEN'):
				var_content=check_var(argument1)
				if var_content==None:
					exit(32)
				symb_content=check_symb(argument2)
				if symb_content[0]=="string":
					strlen_counter=0
					for char in symb_content[1]:
						strlen_counter+=1

					splited_arg=argument1.text.split("@",1)
					if splited_arg[0]=="GF":
						GF[splited_arg[1]]=["int",strlen_counter]
					elif splited_arg[0]=="LF":
						LF[-1][splited_arg[1]]=["int",strlen_counter]
					elif splited_arg[0]=="TF":
						TF[splited_arg[1]]=["int",strlen_counter]
					else:
						exit(32)
				else:
					exit(53)
					
			elif (instruction_dict[i].attrib['opcode'].upper()=='TYPE'):

				check_var(argument1)
				symb_content=check_symb(argument2,"TYPE")
				if symb_content==None:
					exit(32)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["string",symb_content[0]]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["string",symb_content[0]]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["string",symb_content[0]]
				else:
					exit(32)
				print
			elif  (instruction_dict[i].attrib['opcode'].upper()=='INT2CHAR'):
				check_var(argument1)
				symb_content =check_symb(argument2)
				if symb_content[0]!="int":
					exit(53)
				if not ((symb_content[1]>=0) and (symb_content[1]<1114112)):
					exit(58)
				print
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["string",chr(int(symb_content[1]))]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["string",chr(int(symb_content[1]))]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["string",chr(int(symb_content[1]))]
				else:
					exit(32)

			elif  (instruction_dict[i].attrib['opcode'].upper()=='NOT'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				if (symb_content1[0]!="bool"):
					exit(53)
				try:
					if not (check_if_bool(symb_content1)):
						new_value = "true"
					else:
						new_value = "false"
						
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["bool",new_value]
				else:
					exit(32)

			elif (instruction_dict[i].attrib['opcode'].upper()=='READ'):
				check_var(argument1)
				type_content=check_type(argument2)
				new_value=""

				if input_flag:
					try:
						if type_content=="int":
							new_value=int(input())
						elif type_content=="string":
							new_value=input()
						elif type_content=="bool":
							new_value=input().lower()
							if new_value=="true":
								new_value=new_value
							else:
								new_value="false"
					except Exception:
						if type_content=="int":
							new_value=0
						elif type_content=="string":
							new_value=""
						elif type_content=="bool":
							new_value="false"
				else:

					try:
						tmp_counter=0
						line=""
						with open(my_input_string , 'r') as file:
							while True:
								tmp=file.readline()
								if tmp[-1]=="\n":
									line=tmp[:-1]
								else:
									line=tmp
								tmp_counter+=1
								if tmp_counter>read_counter:
									break
							
							tmp_counter+=1
							read_counter+=1
							try:
								if type_content=="int":
									new_value=int(line)
								elif type_content=="string":
									new_value=line
								elif type_content=="bool":
									new_value=line.lower()
									if new_value=="true":
										pass
									else:
										new_value="false"
								else:
									exit(32)
							except Exception:
								if type_content=="int":
									new_value=0
								elif type_content=="string":
									new_value=""
								elif type_content=="bool":
									new_value="false"
								else:
									exit(32)
					except Exception:
						if type_content=="int":
							new_value=0
						elif type_content=="string":
							new_value=""
						elif type_content=="bool":
							new_value="false"
						else:
							exit(32)

				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=[type_content,new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=[type_content,new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=[type_content,new_value]
				else:
					exit(32)



		elif (len(instruction_dict[i])==3):
			for argument in (instruction_dict[i]):
				if argument.tag=="arg1":
					argument1=argument
				elif argument.tag=="arg2":
					argument2=argument
				elif argument.tag=="arg3":
					argument3=argument
				else:
					exit(32)

			if (instruction_dict[i].attrib['opcode'].upper()=='ADD'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="int") or (symb_content2[0]!="int")):
					exit(53)
				try:
					new_value=symb_content1[1]+symb_content2[1]
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["int",new_value]
				else:
					exit(32)

				
			elif (instruction_dict[i].attrib['opcode'].upper()=='SUB'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="int") or (symb_content2[0]!="int")):
					exit(53)
				try:
					new_value=symb_content1[1]-symb_content2[1]
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["int",new_value]
				else:
					exit(32)
				
			elif  (instruction_dict[i].attrib['opcode'].upper()=='MUL'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)

				if ((symb_content1[0]!="int") or (symb_content2[0]!="int")):
					exit(53)
				try:
					new_value=symb_content1[1]*symb_content2[1]
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["int",new_value]
				else:
					exit(32)
			elif (instruction_dict[i].attrib['opcode'].upper()=='IDIV'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="int") or (symb_content2[0]!="int")):
					exit(53)
				try:
					new_value=symb_content1[1] // symb_content2[1]
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["int",new_value]
				else:
					exit(32)
				
			elif (instruction_dict[i].attrib['opcode'].upper()=='LT'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]=="nil") or (symb_content2[0]=="nil")):
					if (symb_content1[0]=="nil") and (symb_content2[0]=="nil"):
						new_value="true"
					else:
						new_value="false"
				if ((symb_content1[0]!=symb_content2[0])):
					exit(53)
				try:
					if(check_if_bool(symb_content1) < check_if_bool(symb_content2)):
						new_value="true"
					else:
						new_value="false"
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["bool",new_value]
				else:
					exit(32)
				
			elif  (instruction_dict[i].attrib['opcode'].upper()=='GT'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				
				if ((symb_content1[0]!=symb_content2[0])):
					exit(53)
				try:
					if(check_if_bool(symb_content1) > check_if_bool(symb_content2)):
						new_value="true"
					else:
						new_value="false"
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["bool",new_value]
				else:
					exit(32)
			elif (instruction_dict[i].attrib['opcode'].upper()=='EQ'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]=="nil") or (symb_content2[0]=="nil")):
					if (symb_content1[0]=="nil") and (symb_content2[0]=="nil"):
						new_value="true"
					else:
						new_value="false"
				elif (symb_content1[0]!=symb_content2[0]):
					exit(53)
				try:
					if(symb_content1[1] == symb_content2[1]):
						new_value="true"
					else:
						new_value="false"
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["bool",new_value]
				else:
					exit(32)
				
			elif (instruction_dict[i].attrib['opcode'].upper()=='OR'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="bool") or (symb_content2[0]!="bool")):
					exit(53)
				try:
					if(check_if_bool(symb_content1) or check_if_bool(symb_content2)):
						new_value="true"
					else:
						new_value="false"
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["bool",new_value]
				else:
					exit(32)
			elif (instruction_dict[i].attrib['opcode'].upper()=='AND'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)

				if ((symb_content1[0]!="bool") or (symb_content2[0]!="bool")):
					exit(53)
			
				if((check_if_bool(symb_content1)) and (check_if_bool(symb_content2))):
					new_value="true"
				else:
					new_value="false"
				
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["bool",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["bool",new_value]
				else:
					exit(32)
			
			elif (instruction_dict[i].attrib['opcode'].upper()=='CONCAT'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="string") or (symb_content2[0]!="string")):
					exit(53)
				try:
					new_value= symb_content1[1] + symb_content2[1]
				except Exception:
					exit(53)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["string",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["string",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["string",new_value]
				else:
					exit(32)
			
			elif (instruction_dict[i].attrib['opcode'].upper()=='GETCHAR'):
				check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="string") or (symb_content2[0]!="int")):
					exit(53)
				try:
					new_value= symb_content1[1][symb_content2[1]]
				except Exception:
					exit(58)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["string",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["string",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["string",new_value]
				else:
					exit(32)

				
			elif  (instruction_dict[i].attrib['opcode'].upper()=='SETCHAR'):
				var_content=check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="int") or (symb_content2[0]!="string") or (var_content[0]!="string")):
					exit(53)
				
				if ((len(var_content[1])<=symb_content1[1]) or (symb_content1[1]<0)):
					exit(58)
				if symb_content2[1]=="":
					exit(58)
				new_value=""
				j=0
				for c in var_content[1]:
					if j==symb_content1[1]:
						new_value+=symb_content2[1][0]
					else:
						new_value+=c
					j+=1
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["string",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["string",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["string",new_value]
				else:
					exit(32)
			
			elif (instruction_dict[i].attrib['opcode'].upper()=='STRI2INT'):
				var_content=check_var(argument1)
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)
				if ((symb_content1[0]!="string") or (symb_content2[0]!="int")):
					exit(53)
				try:
					tmp_string=symb_content1[1][symb_content2[1]]
				except Exception:
					exit(58)
				new_value = ord(tmp_string)
				splited_arg=argument1.text.split("@",1)
				if splited_arg[0]=="GF":
					GF[splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="LF":
					LF[-1][splited_arg[1]]=["int",new_value]
				elif splited_arg[0]=="TF":
					TF[splited_arg[1]]=["int",new_value]
				else:
					exit(32)
				
			elif  (instruction_dict[i].attrib['opcode'].upper()=='JUMPIFNEQ'):
				check_if_label(argument1)

				try:
					jump_order=label_dict[argument1.text]
				except Exception:
					exit(52)
				
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)

				if (symb_content1[0]!=symb_content2[0]):
					exit(53)
				if (symb_content1[1]!=symb_content2[1]):
					i=int(jump_order)
					continue

			elif (instruction_dict[i].attrib['opcode'].upper()=='JUMPIFEQ'):
				check_if_label(argument1)
				try:
					jump_order=label_dict[argument1.text]
				except Exception:
					exit(52)
				
				symb_content1=check_symb(argument2)
				symb_content2=check_symb(argument3)

				if (symb_content1[0]!=symb_content2[0]):
					exit(53)
				if (symb_content1[1]==symb_content2[1]):
					i=int(jump_order)
					continue
			else:
				exit(32)
		else:
			exit(32)
	number_of_variables=count_variables(number_of_variables)
	i=i+1
STATI_output(number_of_interpreted_instructions,number_of_variables)
