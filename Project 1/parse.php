#!/bin/env php7.3
<?php

//function deletes comments and blank lines from input

function clear_input(){

	while($input_line = fgets(STDIN)){

		
		$line = preg_replace("/#.*$/","", $input_line);
		if ($line!=$input_line) {
			$GLOBALS['comments']+=1;
		}
		$line = preg_replace("/^\s*$/","", $line);	//delete comments and blank lines
	
		$function_output .= $line;
		}
	return $function_output;
}

//function writes help

function write_help(){
	echo "program expect input in IPPcode19 on stdin and returns xml to stdout\n";
	echo "program supports multiple options\n";
	echo "both short and long versions of options are available\n";
	echo "--stats=$file_name is a mandatory option if user want to use parameters --loc, --labels, --comments or --jumps\n";
	echo "--stats=$file_name sets an outputfile where will be hopefully writen your stats\n";
	echo "--stats=$file_name can only be used in combination with one or more othese folowing options:\n";
	echo "\t--loc writes number of usefull lines of code in input\n";
	echo "\t--labels writes number of defined labels in input\n";
	echo "\t--comments writes nuber of comments used in input\n";
	echo "\t--jumps writes number of jump instructions in input\n";

	return;
}

//function control if given string is variable in IPPcode19

function check_var($token){
	if (preg_match("/\A(GF|LF|TF)@[\_\-\$\&\%\*\!\?a-zA-Z0-9]+\Z/", $token)){
		return True;
	}else{
		return False;
	}
}

//function control if given string is integer in IPPcode19

function check_int($token){
	if (preg_match("/\Aint@[0-9]*\Z/", $token)){
		return True;
	}else{
		return False;
	}
}

//function control if given string is boolean in IPPcode19

function check_bool($token){
	if (preg_match("/\Abool@(true|false)\Z/", $token)){
		return True;
	}else{
		return False;
	}
}

//function control if given string is string in IPPcode19

function check_string($token){

	$tmp_token=preg_replace("/\\\\\d{3}/", "", $token);
	if (preg_match("/\Astring@([^\\\\\s])*\Z/", $tmp_token)){
		return True;
	}else{
		return False;
	}
}

//function control if given string is nil in IPPcode19

function check_nil($token){
	if (preg_match("/\Anil@nil\Z/", $token)){
		return True;
	}else{
		return False;
	}
}

//function control if given string is type in IPPcode19

function check_type($token){
	if (preg_match("/\A(int|string|bool)\Z/", $token)){
		return True;
	}else{
		return False;
	}
}

//function control if given string is label in IPPcode19

function check_label($token){
	if (preg_match("/\A[\_\-\$\&\%\*\!\?a-zA-Z0-9]+\Z/", $token)){
		return True;
	}else{
		return False;
	}
}

//function controle if given file is okej

function check_file($token){

	if (preg_match("/\A([^\=])*\Z/", $token)){
		return True;
	}else{
		return False;
	}
}

//function control if given string is symbol in IPPcode19

function check_symb($token){
	return (check_var($token) or check_int($token) or check_bool($token) or check_string($token) or check_nil($token));
}

//function writes argument to xml object

function write_output_of_argument(...$arguments_atributes){


	xmlwriter_start_element($GLOBALS['xw'], 'arg'.$arguments_atributes[0]);
	xmlwriter_start_attribute($GLOBALS['xw'], 'type');
	if (preg_match("/(\A(GF|LF|TF)@)/", $arguments_atributes[1])) {
		xmlwriter_text($GLOBALS['xw'], 'var');
		xmlwriter_end_attribute($GLOBALS['xw']);
		xmlwriter_text($GLOBALS['xw'], $arguments_atributes[1]);
	}elseif (check_type($arguments_atributes[1])) {
		xmlwriter_text($GLOBALS['xw'], "type");
		xmlwriter_end_attribute($GLOBALS['xw']);
		xmlwriter_text($GLOBALS['xw'], $arguments_atributes[1]);
	}elseif ( check_label($arguments_atributes[1])) {
		xmlwriter_text($GLOBALS['xw'], "label");
		xmlwriter_end_attribute($GLOBALS['xw']);
		xmlwriter_text($GLOBALS['xw'], $arguments_atributes[1]);
		
	}else{
		if($splited_argument=preg_split("/@/", $arguments_atributes[1])){
			xmlwriter_text($GLOBALS['xw'], $splited_argument[0]);
			xmlwriter_end_attribute($GLOBALS['xw']);
			xmlwriter_text($GLOBALS['xw'], $splited_argument[1]);
		}else{
			
			exit(23);
		}
	}


	xmlwriter_end_element($GLOBALS['xw']);
	return;

}

//function writes line to xml object

function write_output_of_a_line(...$function_input){

	switch ((string)sizeof($function_input)) {
		case '2':
			
			xmlwriter_start_element($GLOBALS['xw'], 'instruction');
			xmlwriter_start_attribute($GLOBALS['xw'], 'order');
			xmlwriter_text($GLOBALS['xw'], $function_input[0]);
			xmlwriter_start_attribute($GLOBALS['xw'], 'opcode');
			xmlwriter_text($GLOBALS['xw'], $function_input[1]);

			xmlwriter_end_element($GLOBALS['xw']);
			
			break;
		case '3':
			xmlwriter_start_element($GLOBALS['xw'], 'instruction');
			xmlwriter_start_attribute($GLOBALS['xw'], 'order');
			xmlwriter_text($GLOBALS['xw'], $function_input[0]);
			xmlwriter_start_attribute($GLOBALS['xw'], 'opcode');
			xmlwriter_text($GLOBALS['xw'], $function_input[1]);
			write_output_of_argument(1,$function_input[2]);
			
			xmlwriter_end_element($GLOBALS['xw']); 
			break;
		case '4':
			xmlwriter_start_element($GLOBALS['xw'], 'instruction');
			xmlwriter_start_attribute($GLOBALS['xw'], 'order');
			xmlwriter_text($GLOBALS['xw'], $function_input[0]);
			xmlwriter_start_attribute($GLOBALS['xw'], 'opcode');
			xmlwriter_text($GLOBALS['xw'], $function_input[1]);

			write_output_of_argument(1,$function_input[2]);
			write_output_of_argument(2,$function_input[3]);


			xmlwriter_end_element($GLOBALS['xw']); 

			break;
		case '5':
			xmlwriter_start_element($GLOBALS['xw'], 'instruction');
			xmlwriter_start_attribute($GLOBALS['xw'], 'order');
			xmlwriter_text($GLOBALS['xw'], $function_input[0]);
			xmlwriter_start_attribute($GLOBALS['xw'], 'opcode');
			xmlwriter_text($GLOBALS['xw'], $function_input[1]);

			write_output_of_argument(1,$function_input[2]);
			write_output_of_argument(2,$function_input[3]);
			write_output_of_argument(3,$function_input[4]);

			xmlwriter_end_element($GLOBALS['xw']); 
			break;
		
		default:
			exit(23);
			break;

	}
	return;	

}

//function controls arguments

function check_args(array $argv){
	
	$file_name="\=";
	if (($argv[1]=="--help" or $argv[1]=="-help") and sizeof($argv)==2){
	write_help();
	exit(0);
	}elseif (sizeof($argv)==1) {
		return $file_name;
	}
	$check_param=false;
	$check_stats=false;
	for ($i=1; $i < sizeof($argv); $i++) { 
		switch ($argv[$i]) {
			case '--loc':
			case '-loc':
			case '--comments':
			case '-comments':
			case '-labels':
			case '--labels':
			case '-jumps':
			case '--jumps':
			$check_param=true;
				break;
			
			default:
				$check_stats=true;
				$tmp_args=preg_split("/\=/", $argv[$i]);
				$tmp=((!preg_match("/--stats/", $tmp_args[0])) and (!preg_match("/-stats/", $tmp_args[0])));
			
				echo $tmp ? "true\n" : "false\n";
				if ($tmp or !check_file($tmp_args[1]) or (sizeof($tmp_args)!=2)){
					echo "zomrel som";
					exit(10);
				}else{
					$file_name=$tmp_args[1];
				}
		}
	}
	if (!$check_stats || !$check_param) {
		exit(10);
	}
	return $file_name;
}

// function handles STATP output to file

function STATP_output(array $argv,$file_name,$loc_result,$comments_result,$labels_result,$jumps_result){
try{
	$f=fopen($file_name,"w");

	for ($i=1; $i < sizeof($argv); $i++) { 
		switch ($argv[$i]) {
			case '-loc':
			case '--loc':
				fwrite($f,$loc_result."\n");
				break;
			case '-comments':
			case '--comments':
				fwrite($f,$comments_result."\n");
				break;
			case '-labels':
			case '--labels':
				fwrite($f,$labels_result."\n");
				break;
			case '-jumps':	
			case '--jumps':
				fwrite($f, $loc_result."\n");
				break;
			
		}
	}
	fclose($f);
	return;
}
catch(Exception $e){
	exit(12);
}
}

//main

$file_name=check_args($argv);

$comments=0;
$loc=0;
$labels=0;
$jumps=0;

$my_input =clear_input();

$order = 0;

// iterate trough lines of input

foreach(preg_split("/((\r?\n)|(\r\n?))/", $my_input) as $line)  {


	//check and create header
	
	if (($order==0)and(preg_match("/\s*.IPPcode19\s*/i", $line))) {

				
		$xw = xmlwriter_open_memory();
		xmlwriter_set_indent($xw, 1);
		$res = xmlwriter_set_indent_string($xw, "\t");

		xmlwriter_start_document($xw, '1.0', 'UTF-8');

		
		xmlwriter_start_element($xw, 'program');

		
		xmlwriter_start_attribute($xw, 'language');
		xmlwriter_text($xw, 'IPPcode19');
		xmlwriter_end_attribute($xw);
		
		


		$order = $order + 1;
		continue;

	}elseif ( ($order==0) and (!preg_match("/\s*.IPPcode19\s*/i", $line))) {
		
		exit(21);
	}
	$loc+=1;

	// split line to op code and single arguments 
	
 	$line_words=preg_split("/[\s]+/", " ".$line." ");

	 	
 	switch (strtoupper($line_words[1])) {
 		case 'MOVE':
 			if (check_var($line_words[2]) and check_symb($line_words[3]) and sizeof($line_words)==5){
 				write_output_of_a_line($order,$line_words[1],$line_words[2],$line_words[3]);
 			}else{
 				
 				exit(23);
 			}

 			break;
 		case 'RETURN':
 			$jumps+=1;

 		case 'CREATEFRAME':
 			
 		case 'POPFRAME':

 		case 'RETURN':

 		case 'BREAK':
 			
 		case 'PUSHFRAME':

 			
 			if (sizeof($line_words)==3){
 				
 				write_output_of_a_line($order,$line_words[1]);
 			}else{
 				
 				exit(23);
 			}
 			break;
 		case 'DEFVAR':
 			
 			if (check_var($line_words[2]) and sizeof($line_words)==4){
 				write_output_of_a_line($order,$line_words[1],$line_words[2]);
 			}else{
 				
 				exit(23);
 			}
 			break;

 		case 'LABEL':
 			
 			$labels+=1;
 			if (check_label($line_words[2]) and sizeof($line_words)==4){
 				write_output_of_a_line($order,$line_words[1], $line_words[2]);
 			}else{
 				
 				exit(23);
 			}
 			break;

 		case 'CALL':

 		case 'JUMP':
 			
 			$jumps+=1;
 			if (check_label($line_words[2]) and sizeof($line_words)==4){
 				
 				write_output_of_a_line($order,$line_words[1], $line_words[2]);
 			}else{
 				
 				exit(23);
 			}
 			
 			break;

 		case 'PUSHS':
 			if (check_symb($line_words[2]) and sizeof($line_words)==4){
 				write_output_of_a_line($order,$line_words[1], $line_words[2]);
 			}else{
 				
 				exit(23);
 			}
 			break;
 		case 'POPS':
 			if (check_var($line_words[2]) and sizeof($line_words)==4){
 				write_output_of_a_line($order,$line_words[1], $line_words[2]);
 			}else{
 				
 				exit(23);
 			}
 			break;
 		case 'ADD':
 
 		case 'SUB':

 		case 'MUL':

 		case 'IDIV':

 		case 'LT':

 		case 'GT':

 		case 'EQ':

 		case 'AND':

 		case 'OR':

 		case 'NOT':
 			if (check_var($line_words[2]) and check_symb($line_words[3]) and check_symb($line_words[4]) and sizeof($line_words)==6){
 				write_output_of_a_line($order,$line_words[1],$line_words[2],$line_words[3],$line_words[4]);
 			}else{
 				
 				exit(23);
 			}
 			break;

 		case 'STRLEN':

 		case 'TYPE':
 			
 		case 'INT2CHAR':
 			if (check_var($line_words[2]) and check_symb($line_words[3]) and sizeof($line_words)==5){
 				write_output_of_a_line($order,$line_words[1],$line_words[2],$line_words[3]);
 			}else{
 				
 				exit(23);
 			}

 			break;
 		case 'CONCAT':

 		case 'GETCHAR':
 			
 		case 'SETCHAR':
 			
 		case 'STRI2INT':
 			if (check_var($line_words[2]) and check_symb($line_words[3]) and check_symb($line_words[4]) and sizeof($line_words)==6){
 				write_output_of_a_line($order,$line_words[1],$line_words[2],$line_words[3],$line_words[4]);
 			}else{
 				
 				exit(23);
 			break;
 			}
 		case 'READ':
 			if (check_var($line_words[2]) and check_type($line_words[3]) and sizeof($line_words)==5){
 				write_output_of_a_line($order,$line_words[1],$line_words[2],$line_words[3]);
 			}else{
 				
 				exit(23);
 			}
 			break;
 		case 'EXIT':
 			
 		case 'DPRINT':
 			
 		case 'WRITE':
 			if (check_symb($line_words[2]) and sizeof($line_words)==4){
 				write_output_of_a_line($order,$line_words[1],$line_words[2]);
 			}else{
 				
 				exit(23);
 			}
 			break;			
 		
 		case 'JUMPIFNEQ':
 			
 		case 'JUMPIFEQ':
 			$jumps+=1;
 			if (check_label($line_words[2]) and check_symb($line_words[3]) and check_symb($line_words[4]) and sizeof($line_words)==6){
 				write_output_of_a_line($order,$line_words[1],$line_words[2],$line_words[3],$line_words[4]);
 			}else{
 				
 				exit(23);
 			}
 			break;
		
 		default:
 			if (preg_match("/\A\s*\Z/", $line)) {
 				
 				break;
 			}
 			
 			exit(22);
 			break;
 	}

 	$order = $order + 1;
} 	

xmlwriter_end_element($xw);
xmlwriter_end_document($xw);

echo xmlwriter_output_memory($xw);

if ($file_name!="\=") {
	STATP_output($argv,$file_name,$loc,$comments,$labels,$jumps);
}



?>