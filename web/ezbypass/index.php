<?php

$test=$_GET['test'];

if(!preg_match("/[0-9]|\~|\`|\@|\#|\\$|\%|\^|\&|\*|\（|\）|\-|\=|\+|\{|\[|\]|\}|\:|\'|\"|\,|\<|\.|\>|\/|\?|\\\\|implode|phpinfo|localeconv|pos|current|print|var|dump|getallheaders|get|defined|str|split|spl|autoload|extensions|eval|phpversion|floor|sqrt|tan|cosh|sinh|ceil|chr|dir|getcwd|getallheaders|end|next|prev|reset|each|pos|current|array|reverse|pop|rand|flip|flip|rand|content|session_id|session_start|echo|readfile|highlight|show|source|file|assert/i", $test)){
    eval($test);
}
else{
    echo "oh nonono hacker!";
}

highlight_file(__FILE__);