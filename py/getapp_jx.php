<?php
/*
getapp_jx.php?host=域名&key=getapp密钥&api=6d735c167eeda72b836cf382e4863f3f(parse_api)&v=
host: 域名 (结尾无需 / )
key: getapp数据解密key
api：加密的parse_api参数，抓包或解密详情页获取
type: 区分get1和get2-> 默认get1，type=2 即是get2
*/
error_reporting(0);
header('Content-type: text/json;charset=utf-8');
$v = $_GET['v']??die('链接为空');
$host = $_GET['host']??die('host为空');
$parse_api = $_GET['api']??die('parse为空');
$key = $_GET['key']??die('key为空');
$type = $_GET['type'];
$time = time();
$curl = curl_init();
$get_type = 'get';
if($type == '2'){ $get_type = 'qiji'; }
curl_setopt_array($curl, [
  CURLOPT_URL => $host.'/api.php/'.$get_type.'appapi.index/vodParse',
  CURLOPT_RETURNTRANSFER => 1,
  CURLOPT_SSL_VERIFYPEER => 0,
  CURLOPT_SSL_VERIFYHOST => 0,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'POST',
  CURLOPT_POSTFIELDS => 'parse_api='.$parse_api.'&url='.urlencode(encrypt($v,$key)).'&token=',
  CURLOPT_HTTPHEADER => [
    'User-Agent: okhttp/3.14.9',
    'Connection: Keep-Alive',
    'Accept-Encoding: gzip',
    'Content-Type: application/x-www-form-urlencoded',
    'app-version-code: 207',
    'app-ui-mode: light',
    'app-api-verify-time: '.$time,
    'app-api-verify-sign: '.encrypt($time,$key),
  ],
]);
$response = curl_exec($curl);
$err = curl_error($curl);
curl_close($curl);
if ($err) { die('cURL Error #:' . $err);}
$data = json_decode($response)->data;
if(!$data){die('源接口返回data为空');}
$data2 = decrypt($data,$key);
$data3 = json_decode($data2)->json;
die($data3);
function encrypt($data, $key) { return base64_encode(openssl_encrypt($data, 'aes-128-cbc', $key, 1, $key)); }
function decrypt($data, $key) { return openssl_decrypt($data, 'aes-128-cbc', $key, 0, $key); }