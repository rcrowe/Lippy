<?php

define('LIP_PORT', 50000);

$data2 = array(
    'lvl'  => 5,
    'msg'  => 'This is a test message number 2',
    'data' => array(
        'name' => 'Rob Crowe',
        'age'  => 23
    )
);

include 'Lip.php';

Lip::debug('test');
Lip::info('test');
Lip::warning('test');
Lip::error('test');
Lip::critical('test', $data2);

?>