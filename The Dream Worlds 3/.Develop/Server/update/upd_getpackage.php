<?php
	include '../php/dbconnector.php';
	include '../php/function.php';
	include '../php/global.php';
	$verList=array();
	if(isset($_GET['buildVersion'])){
		if(isset($_GET['istest']) && $_GET['istest']=='1'){
			$verlist=mysql_query("SELECT * FROM tdw3_version WHERE buildVersion>'$_GET[buildVersion]' ORDER BY id");
		}else{
			$verlist=mysql_query("SELECT * FROM tdw3_version WHERE buildVersion>'$_GET[buildVersion]' AND allowUpdate='1'  ORDER BY id");
		}
		if($verlist){
			while($vl = mysql_fetch_array($verlist)){
				array_push($verList,"update_$vl[mainVersion].$vl[buildVersion].$vl[dateVersion].$vl[updfileType]");
			}
			$verlistStr="";
			if(count($verList)>0){
				for($vi=0;$vi<count($verList);$vi++){
					$verlistStr=$verlistStr.$verList[$vi];
					if($vi!=count($verList)-1){
						$verlistStr=$verlistStr."|";
					}
				}
				echo $verlistStr;
			}else{
				echo 0;
			}
		}else{
			echo -1;
		}
	}else{
		echo -2;
	}
?>
