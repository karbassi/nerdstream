<?php
if ($_GET['u'] && !$_GET['t']) {
	$user = $_GET['u'];
	
	require_once('txtSQL.class.php'); 
	$sql = new txtSQL('data'); 
	$sql->connect('root', 'nerdstream') or die('Error occurred while connecting, txtSQL said: '.$sql->get_last_error());

	if ( !$sql->selectdb('nerdstream') ) {
		echo 'nerdstream could not be selected, txtSQL said: '.$sql->get_last_error(); 
	}

	$data = $sql->select(array( 
	'db' => 'nerdstream', 
	'table' => 'Users',
	'select' => array('first_name', 'last_name', 'job_title', 'start_time', 'end_time', 'interval', 'local_dir', 'local_delete', 'computer_name', 'last_update'),
	'where' => array('computer_name = ' . $user), 
	'limit' => '1'
	));
	$sql->disconnect();
	
	if (count($data) > 0) {
		echo "{";
	 	foreach ($data[0] as $key => $value) {
			echo "'$key':'$value', ";
		}
		echo "}";
	}
	
} elseif ($_GET['u'] && $_GET['t']) {
	
	$user = $_GET['u'];
	$update = $_GET['t'];

	require_once('txtSQL.class.php'); 
	$sql = new txtSQL('data'); 
	$sql->connect('root', 'nerdstream') or die('Error occurred while connecting, txtSQL said: '.$sql->get_last_error());

	if ( !$sql->selectdb('nerdstream') ) {
		echo 'nerdstream could not be selected, txtSQL said: '.$sql->get_last_error(); 
	}
	
	if ( !$sql->update(array('db' => 'nerdstream', 
	'table' => 'Users', 
	'where' => array('computer_name = ' . $user), 
	'values' => array('last_update' => $update), 
	'limit' => array(0))) ){ 
		die('An error occurred, txtSQL said: '.$sql->get_last_error()); 
	} else {
		// echo $update;
	}
	$sql->disconnect();
} else {
	header("HTTP/1.0 404 Not Found");
}
?>