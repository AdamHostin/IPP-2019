#!/bin/env php7.3
<?php
//Check file described alredy in parse.php
function check_file($token){

	if (preg_match("/\A([^\=])*\Z/", $token)){
		return True;
	}else{
		return False;
	}
}
//Check args very similar to parse.php 
//If file argument(s) was not givendefault value is assigned (see lines 67-72)
function check_args(array $argv){


	if (($argv[1]=="--help" or $argv[1]=="-help") and sizeof($argv)==2){
		write_help();
		exit(0);
	}

	#echo "pred cyklom\n";
	$i=0;
	for ($i=1; $i < sizeof($argv); $i++) { 
		
		$tmp_args=preg_split("/\=/", $argv[$i]);
	
		if ((sizeof($tmp_args)!=2)){
			if (($argv[$i]=="--recursive" or $argv[$i]=="-recursive")){
				$GLOBALS['recursive_test']=true;
			}elseif ($argv[$i]=="--parse-only" or $argv[$i]=="-parse-only") {
				$GLOBALS['parse_test']=true;
				if ($GLOBALS['int_test']) {
					exit(10);
				}
			}elseif ($argv[$i]=="--int-only" or $argv[$i]=="-int-only") {
				$GLOBALS['int_test']=true;
				if ($GLOBALS['parse_test']) {
					exit(10);
				}
			}else{
				exit(10);
			}

			
		}elseif ((sizeof($tmp_args)==2) or check_file($tmp_args[1])){
			if (($tmp_args[0]=="--directory") or ($tmp_args[0]=="-directory")) {

				$GLOBALS['directory']=$tmp_args[1];
				
			}elseif ((($tmp_args[0]=="--int-script") or ($tmp_args[0]=="-int-script"))) {
				
				$GLOBALS['int_script_path']=$tmp_args[1];
				
			}elseif ((($tmp_args[0]=="--parse-script") or ($tmp_args[0]=="-parse-script"))) {

				$GLOBALS['parse_script_path']=$tmp_args[1];		
			}

		}else{
			exit(10);
		}
		
		
	}
	
	if ($GLOBALS['directory']=="") {
		$GLOBALS['directory']=getcwd();
	}if ($GLOBALS['int_script_path']=="") {
		$GLOBALS['int_script_path']="interpret.py";
	}if ($GLOBALS['parse_script_path']=="") {
		$GLOBALS['parse_script_path']="parse.php";
	}
	#echo "directory is:".$GLOBALS['directory']."\n";
	return;
		
}

//Writes help to stdout and ends with exit code 0
function write_help(){
	echo "--recursive script search for tests recursively\n";
	echo "--int-only script starts tests only with interpret script\n";
	echo "--parse-only script starts tests only with parse script\n";
	echo "--directory= sets path where script starts searching for tests default value is current dir\n";
	echo "--int-script= sets path where interpret script is stored default value is interpret.py\n";
	echo "--parse-script= sets path where parse script is stored default value is parse.php\n";
	exit(0);
}



//Funcion handles single test for parse.php
function test_parse_in_globe($src_file){
	
	#echo "test_parse_in_globe";
	$file_name=substr($src_file, 0, -3);

	$handle=fopen($file_name."in", "r");
	if (!$handle) {
		$handle=fopen($file_name."in", "w");
	}
	fclose($handle);

	$handle=fopen($file_name."out", "r");
	if (!$handle) {
		$handle=fopen($file_name."out", "w");
	}
	fclose($handle);
	$expected_output_variable =  file_get_contents($file_name."out");

	$handle=fopen($file_name."rc", "r");
	if (!$handle) {
		$handle=fopen($file_name."rc", "w");
		fwrite($handle, "0");
	}
	fclose($handle);
	$expected_return_code = intval(file_get_contents($file_name."rc"));

	

	unset($output_variable);
	unset($return_code);
	#echo($GLOBALS['parse_script_path']);
	exec("php7.3 \"".$GLOBALS['parse_script_path']." \" < \"".$src_file."\"", $useless_var , $return_code);
	#var_dump($useless_var);
	foreach ($useless_var as $value) {
		$output_variable.=$value."\n";
	}
	#echo $expected_return_code."\n";
	#echo $return_code."\n";
	#var_dump( $expected_output_variable."\n");
	#echo($output_variable."\n");
	file_put_contents("output_variable_file",$output_variable);
	file_put_contents("expected_output_variable_file",$expected_output_variable);
	#unset($output_variable);
	exec("java -jar /pub/courses/ipp/jexamxml/jexamxml.jar output_variable_file expected_output_variable_file > tmp_file");
	unset($test_variable);
	$test_variable=  file_get_contents("tmp_file");
	#echo strlen($output_variable);
	#echo "som useles: ".$output_variable."\n";
	
	if (($return_code == $expected_return_code) and (strpos($test_variable,"Two files are identical")!=false)) {
		$GLOBALS['test_ok']++;
    	$GLOBALS['html'].= "<p style=\"color: green\">".substr($src_file, 0, -4)." : ok </p>";
    }
    else { 
    	$GLOBALS['test_fail']++;
    	$GLOBALS['html'].= "<p style=\"color: red\">".substr($src_file, 0, -4)." expected ".$expected_return_code." but ".$return_code." was returned : faile<br>expected output was: ".$expected_output_variable."<br>given output was: ".$output_variable."<br>based on: ".$test_variable."  </p>";
	}
	#echo "tu je to ok\n";
}
	
//Funcion handles single test for interpret.py
function test_int_in_globe($src_file){
	#echo "test_int_in_globe";
	$file_name=substr($src_file, 0, -3);

	$handle=fopen($file_name."in", "r");
	if (!$handle) {
		$handle=fopen($file_name."in", "w");
	}
	fclose($handle);

	$handle=fopen($file_name."out", "r");
	if (!$handle) {
		$handle=fopen($file_name."out", "w");
	}
	fclose($handle);
	$expected_output_variable =  file_get_contents($file_name."out");

	$handle=fopen($file_name."rc", "r");
	if (!$handle) {
		$handle=fopen($file_name."rc", "w");
		fwrite($handle, "0");
	}
	fclose($handle);
	$expected_return_code = intval(file_get_contents($file_name."rc"));

	

	unset($output_variable);
	unset($return_code);
	#echo($GLOBALS['int_script_path'])."\n";
	exec("python3.6 \"".$GLOBALS['int_script_path']."\" --input=\"".$file_name."\"in --source=\"".$src_file."\"> output_variable_file", $useless_var , $return_code);
	
	file_put_contents("expected_output_variable_file",$expected_output_variable);
	#unset($output_variable);
	exec("diff expected_output_variable_file output_variable_file > tmp_file");
	unset($test_variable);
	$test_variable=  file_get_contents("tmp_file");
	#echo strlen($output_variable);
	#echo "som useles: ".$output_variable."\n";
	
	if (($return_code == $expected_return_code) and ($test_variable=="")) {
		$GLOBALS['test_ok']++;
    	$GLOBALS['html'].= "<p style=\"color: green\">".substr($src_file, 0, -4)." : ok </p>";
    }
    else { 
    	$GLOBALS['test_fail']++;
    	$GLOBALS['html'].= "<p style=\"color: red\">".substr($src_file, 0, -4)." expected ".$expected_return_code." but ".$return_code." was returned : faile <br>expected output was: ".$expected_output_variable."<br>given output was: ".$output_variable." <br>based on: ".$test_variable."  </p>";
	}
	#echo "tu je to ok\n";
}	

//starts tests for interpret one by one
function run_int_tests($dir){
	#echo "interoret\n";
	#echo $GLOBALS['recursive_test']."\n";
	#echo $dir."\n";
	if (substr($dir,-1)!="/") {
		$dir.="/";
	}
	
	if ($GLOBALS['recursive_test']){
		#echo "rec\n";

		$files=recursion_function($dir."*.src");
		#var_dump($files);
		foreach ($files as $src_file) {
			#echo "som tu\n";
			
			test_int_in_globe($src_file);
			
		}
	}else{
		#echo "non\n";
		foreach (glob($dir."*.src") as $src_file) {

			#echo "som tu\n";
			test_int_in_globe($src_file);
			
		}
	}

	
}
//Function handles recursive searching for files and returns array of files
function recursion_function($pattern) {
    $files = glob($pattern); 
    #echo "bol som tu";

    foreach (glob(dirname($pattern).'/*', GLOB_ONLYDIR|GLOB_NOSORT) as $dir) {
        $files = array_merge($files, recursion_function($dir.'/'.basename($pattern)));
        #echo "bol som tu";
    }
    return $files;
}
//starts tests for parse.php one by one
function run_parse_tests($dir){
	#echo "parse\n";
	#echo $GLOBALS['recursive_test']."\n";
	#echo $dir."\n";
	if (substr($dir,-1)!="/") {
		$dir.="/";
	}
	if ($GLOBALS['recursive_test']){
		#echo "rec";

		$files=recursion_function($dir."*.src");
		#var_dump($files);
		foreach ($files as $src_file) {
			#echo "som tu\n";
			
			test_parse_in_globe($src_file);
			
		}
	}else{
		#echo "non\n";
		foreach (glob($dir."*.src") as $src_file) {
			#echo "som tu\n";
			test_parse_in_globe($src_file);
			
		}
	}
}
$handle=fopen("tmp_file", "w");
fclose($handle);

$test_ok=0;
$test_fail=0;
$html ="<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>test.php output</title></head><body>";
$recursive_test=false;
$int_test=false;
$parse_test=false;

$directory="";
$int_script_path="";
$parse_script_path="";
check_args($argv);
#echo "main\n";
#cho substr($directory, -1);
#echo $directory."\n";
if ($int_test) {
	$html.="<h1>interpret tests</h1>";
	run_int_tests($directory);
}
if ($parse_test) {
	$html.="<h1>parse tests</h1>";
	run_parse_tests($directory);
}

$tests_together=$test_fail+$test_ok;
$percentage=($test_ok/$tests_together)*100;
$percentage=round($percentage,2);
$html.="<p>Result: ".$percentage."%<br>".$test_ok." of ".$tests_together." passed</p></body></html>";
#echo $test_ok."\n";
#echo $test_fail."\n";
echo $html;
?>