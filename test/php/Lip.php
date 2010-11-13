<?php

define('LIP_HOST', '127.0.0.1');
define('LIP_PORT', 8080);

class Lip
{
    private static $instance;
    
    public $socket = false;
    public $host;
    public $port;
    
    const DEBUG    = 1;
    const INFO     = 2;
    const WARNING  = 3;
    const ERROR    = 4;
    const CRITICAL = 5;
    
    private function __construct()
    {
        $this->host = LIP_HOST;
        $this->port = LIP_PORT;
    }
    
    public static function instance()
    {
        if(!isset(self::$instance)) {
        
            self::$instance = new Lip;
        }
        
        return self::$instance;
    }
    
    private function connect()
    {
        if($this->socket === false) {
        
            $this->socket = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        
            if(!@socket_connect($this->socket, $this->host, $this->port)) {
                
                $this->socket = false;
            }
        }
        
        return true;
    }
    
    public static function send($lvl, $msg, $data, $close)
    {
        $lip = self::instance();
        
        if(!$lip->connect())
        {
        
            return false;
        }
        
        $json_data = array(
            'lvl' => $lvl,
            'msg' => $msg
        );
        
        if(!empty($data) && is_array($data))
        {
            $json_data['data'] = $data;
        }
        
        @socket_write($lip->socket, json_encode($json_data));
        
        if($close) {
        
            @socket_close($lip->socket);
            $lip->socket = false;
        }
    }
    
    public static function debug($msg, $data = false, $close = true)
    {
        self::send(self::DEBUG, $msg, $data, $close);
    }
    
    public static function info($msg, $data = false, $close = true)
    {
        self::send(self::INFO, $msg, $data, $close);
    }
    
    public static function warning($msg, $data = false, $close = true)
    {
        self::send(self::WARNING, $msg, $data, $close);
    }
    
    public static function error($msg, $data = false, $close = true)
    {
        self::send(self::ERROR, $msg, $data, $close);
    }
    
    public static function critical($msg, $data = false, $close = true)
    {
        self::send(self::CRITICAL, $msg, $data, $close);
    }
}