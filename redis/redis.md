## 验证
``` 
[root@redis-5 redis-7.4.0]# redis-cli -c -a 123456
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6379> set pp v234
-> Redirected to slot [14030] located at 10.244.0.129:6379
OK
10.244.0.129:6379> set yy v234
-> Redirected to slot [7551] located at 10.244.3.221:6379
OK
10.244.3.221:6379> 
```