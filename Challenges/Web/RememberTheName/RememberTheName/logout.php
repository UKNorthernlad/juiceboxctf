<?php
$cookie_name = "Warwick-CTF";
session_destroy();
unset($_COOKIE['$cookie_name']);
$res = setcookie($cookie_name, '', time() - 3600);
header("Location: /index.php");
exit();
?>
