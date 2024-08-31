```
# 1k => 1000 bytes
# 1kb => 1024 bytes
# 1m => 1000000 bytes
# 1mb => 1024*1024 bytes
# 1g => 1000000000 bytes
# 1gb => 1024*1024*1024 bytes
```
# 网络
```
# 生产环境需要指定应用服务器的地址；如果服务器是需要远程访问的，需要将其注释掉或者指定为0.0.0.0
bind 127.0.0.1

; 设置保护模式，如果保护模式为yes，非本机客户端无法连接到redis服务器，如需连接需要设置为no
protected-mode yes

; 指定Redis监听端口，默认端口为6379
port 6379

; 设置tcp的backlog，backlog其实是一个连接队列，
; backlog队列总和=未完成三次握手队列 + 已经完成三次握手队列。
; 在高并发环境下需要一个高 backlog 值来避免慢客户端连接问题。
tcp-backlog 511

; 指定当客户端闲置多长时间后（单位：秒）断开连接，如果指定为0，表示关闭该功能，不自动断开连接
timeout 0

; 对已经连接的客户端进行心跳检测，每隔N秒检测一次，如果设置为0，则不会进行Keepalive检测，建议设置成60
tcp-keepalive
```
# 通用配置
```
; Redis默认不是以守护进程的方式运行，可以通过该配置项修改，设置为yes以守护进程方式后台启动
daemonize no

; 当Redis以守护进程方式运行时，Redis默认会把进程ID写入/var/run/redis.pid文件，也可以自定义路径和名字
pidfile /var/run/redis.pid

; 设置redis服务器的日志级别，一共有四个，由低到高分别为：debug、verbose、notice、warning，级别越高写到文件中的日志信息越少。
loglevel notice

; 设置日志的处理方式：打印到当前终端或者写入到磁盘文件，或者直接丢弃，如果需要经日志信息写入到磁盘可以指定文件的存储路径和名字。
# 服务器为非守护进程, 日志直接打印到终端
# 服务器为守护进程, 而这里又配置为日志记录方式为标准输出，则日志将会发送给/dev/null == 数据被丢弃
logfile stdout
logfile "/home/robin/redis.log"   # 服务器为守护进程,日志信息被写入到指定的磁盘文件中
logfile "/dev/null"               # 服务器为守护进程,日志信息被写入到空设备中 == 数据被丢弃

; 设置数据库的数量，默认redis自带16个数据库，数据库的ID分别为【0，1，2，3，…，15】
; 默认使用的数据库为0，可以在客户端使用SELECT <dbid>命令切换当前使用的数据库。
databases 16
```
# 安全配置
```
; 设置Redis连接密码，如果配置了连接密码，客户端在连接Redis时需要通过AUTH 命令提供该密码，
; 默认是关闭的，客户端可以直接连接redis服务器。
requirepass 123456

#把危险的命令给修改成其他名称。比如CONFIG命令可以重命名为一个很难被猜到的命令，这样用户不能使用，而
内部工具还能接着使用
# rename-command CONFIG b840fc02d524045429941cc15f59e41cb7be6c52

#设置成一个空的值，可以禁止一个命令
# rename-command CONFIG ""
```
# 限制配置
```
; 设置同一时间最大客户端连接数，默认无限制，Redis可以同时打开的客户端连接数为Redis进程可以打开的最大文件描述符数，
; 如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，
; Redis会关闭新的连接并向客户端返回 max number of clients reached 错误信息。
maxclients 128

指定Redis最大内存限制，Redis在启动时会把数据加载到内存中，达到最大内存后，Redis会先尝试清除已到期或即将到期的Key，
当此方法处理 后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。
建议必须设置，否则，将内存占满，造成服务器宕机。
1: 如果设置redis可以使用的内存量，一旦到达内存使用上限，redis将会试图移除内部数据，移除规则可以通过maxmemory-policy来指定。
2: 如果redis无法根据移除规则来移除内存中的数据，或者设置了“不允许移除”，那么redis则会针对那些需要申请内存的指令返回错误信息，
比如SET、LPUSH等。对于无内存申请的指令，仍然会正常响应，比如GET等。
3: 如果你的redis是主redis（说明你的redis有从redis），那么在设置内存使用上限时，需要在系统中留出一些内存空间给同步队列缓存，
只有在你设置的是 “不移除” 的情况下，才不用考虑这个因素。
maxmemory <bytes>

当设置的redis内存被写满之后，指定内存数据的移除策略，处理方式有一下六种：
volatile-lru：使用LRU（least recently used 最近最少使用）算法移除key，只对设置了过期时间的键；
allkeys-lru：在所有集合key中，使用LRU算法移除key
volatile-random：在过期集合中移除随机的key，只对设置了过期时间的键
allkeys-random：在所有集合key中，移除随机的key
volatile-ttl：移除那些TTL值最小的key，即那些最近要过期的key
noeviction：不进行移除。针对写操作，只是返回错误信息
maxmemory-policy noeviction

设置样本数量，LRU算法和最小TTL算法都并非是精确的算法，而是估算值，所以我们可以设置样本的大小，redis默认会检查设置的N个key，
并选择其中最近最少使用（LRU - Least Recently Used）的那个。一般设置3到7的数字，数值越小样本越不准确，但性能消耗越小。
maxmemory-samples 5

# 是否开启salve的最大内存
# replica-ignore-maxmemory yes
```

# 持久化设置
```
设置以rdb方式进行数据持久化的频率（可以设置多个，为互补关系）
# 表示900秒（15分钟）内有1个更改，300秒（5分钟）内有10个更改以及60秒内有10000个更改，满足其中
# 任意一个条件就将内存数据同步到磁盘文件中
save 900 1 
save 300 10
save 60 10000

# 关闭 rdb 这种持久化方式
save ""

指定存储至本地数据库时是否压缩数据，默认为yes，Redis采用LZF压缩，如果为了节省CPU时间，
可以关闭该选项，但会导致数据库文件变的巨大
rdbcompression yes

如果使用rdb方式进行数据持久化，指定存储数据的磁盘文件名字，默认值为 dump.rdb
dbfilename dump.rdb

指定持久化过程中存储数据的磁盘文件（rdb and aof）的路径（可以是相对路径也可以是绝对路径），
dir ./


#在rdb保存的时候，如果打开了rdb-save-incremental-fsync开关，系统会每32MB执行一次fsync。这
对于把文件写入磁盘是有帮助的，可以避免过大的延迟峰值
rdb-save-incremental-fsync yes

# 已启用活动碎片整理
# activedefrag yes

# 启动活动碎片整理的最小碎片浪费量
# active-defrag-ignore-bytes 100mb

# 启动活动碎片整理的最小碎片百分比
# active-defrag-threshold-lower 10

# 我们使用最大努力的最大碎片百分比
# active-defrag-threshold-upper 100

# 以CPU百分比表示的碎片整理的最小工作量
# active-defrag-cycle-min 5

# 在CPU的百分比最大的努力和碎片整理
# active-defrag-cycle-max 75

#将从中处理的set/hash/zset/list字段的最大数目
#主词典扫描
# active-defrag-max-scan-fields 1000
```

# 副本
```  
# 复制选项，slave复制对应的master。
# replicaof <masterip> <masterport>

#如果master设置了requirepass，那么slave要连上master，需要有master的密码才行。masterauth就是用来
配置master的密码，这样可以在连上master后进行认证。
# masterauth <master-password>

#当从库同主机失去连接或者复制正在进行，从机库有两种运行方式：
1) 如果slave-serve-stale-data设置为yes(默认设置)，从库会继续响应客户端的请求。
2) 如果slave-serve-stale-data设置为no，INFO,replicaOF, AUTH, PING, SHUTDOWN, REPLCONF, ROLE, 
CONFIG,SUBSCRIBE, UNSUBSCRIBE,PSUBSCRIBE, PUNSUBSCRIBE, PUBLISH, PUBSUB,COMMAND, POST, HOST: 
and LATENCY命令之外的任何请求都会返回一个错误”SYNC with master in progress”。
replica-serve-stale-data yes

#作为从服务器，默认情况下是只读的（yes），可以修改成NO，用于写（不建议）
#replica-read-only yes

# 是否使用socket方式复制数据。目前redis复制提供两种方式，disk和socket。
如果新的slave连上来或者重连的slave无法部分同步，就会执行全量同步，master会生成rdb文件。
有2种方式：disk方式是master创建一个新的进程把rdb文件保存到磁盘，再把磁盘上的rdb文件传递给slave。
socket是master创建一个新的进程，直接把rdb文件以socket的方式发给slave。
disk方式的时候，当一个rdb保存的过程中，多个slave都能共享这个rdb文件。
socket的方式就的一个个slave顺序复制。在磁盘速度缓慢，网速快的情况下推荐用socket方式。
repl-diskless-sync no

#diskless复制的延迟时间，防止设置为0。一旦复制开始，节点不会再接收新slave的复制请求直到下一个rdb传输。
所以最好等待一段时间，等更多的slave连上来
repl-diskless-sync-delay 5

#slave根据指定的时间间隔向服务器发送ping请求。时间间隔可以通过 repl_ping_slave_period 来设置，默认10秒。
# repl-ping-slave-period 10

# 复制连接超时时间。master和slave都有超时时间的设置。
master检测到slave上次发送的时间超过repl-timeout，即认为slave离线，清除该slave信息。
slave检测到上次和master交互的时间超过repl-timeout，则认为master离线。
需要注意的是repl-timeout需要设置一个比repl-ping-slave-period更大的值，不然会经常检测到超时
# repl-timeout 60


#是否禁止复制tcp链接的tcp nodelay参数，可传递yes或者no。默认是no，即使用tcp nodelay。如果
master设置了yes来禁止tcp nodelay设置，在把数据复制给slave的时候，会减少包的数量和更小的网络带
宽。但是这也可能带来数据的延迟。默认我们推荐更小的延迟，但是在数据量传输很大的场景下，建议选择yes
repl-disable-tcp-nodelay no

#复制缓冲区大小，这是一个环形复制缓冲区，用来保存最新复制的命令。这样在slave离线的时候，不需要完
全复制master的数据，如果可以执行部分同步，只需要把缓冲区的部分数据复制给slave，就能恢复正常复制状
态。缓冲区的大小越大，slave离线的时间可以更长，复制缓冲区只有在有slave连接的时候才分配内存。没有
slave的一段时间，内存会被释放出来，默认1m
# repl-backlog-size 1mb

# master没有slave一段时间会释放复制缓冲区的内存，repl-backlog-ttl用来设置该时间长度。单位为秒。
# repl-backlog-ttl 3600

# 当master不可用，Sentinel会根据slave的优先级选举一个master。最低的优先级的slave，当选master。
而配置成0，永远不会被选举
replica-priority 100

#redis提供了可以让master停止写入的方式，如果配置了min-replicas-to-write，健康的slave的个数小于N，mater就禁止写入。
master最少得有多少个健康的slave存活才能执行写命令。这个配置虽然不能保证N个slave都一定能接收到master的写操作，
但是能避免没有足够健康的slave的时候，master不能写入来避免数据丢失。设置为0是关闭该功能
# min-replicas-to-write 3

# 延迟小于min-replicas-max-lag秒的slave才认为是健康的slave
# min-replicas-max-lag 10

# 设置1或另一个设置为0禁用这个特性。
# Setting one or the other to 0 disables the feature.
# By default min-replicas-to-write is set to 0 (feature disabled) and
# min-replicas-max-lag is set to 10.
```

# 懒加载
```  
#以非阻塞方式释放内存
#使用以下配置指令调用了
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
```

# aof 
```  
#Redis 默认不开启。它的出现是为了弥补RDB的不足（数据的不一致性），所以它采用日志的形式来记录每个写
操作，并追加到文件中。Redis 重启的会根据日志文件的内容将写指令从前到后执行一次以完成数据的恢复工作
默认redis使用的是rdb方式持久化，这种方式在许多应用中已经足够用了。但是redis如果中途宕机，会导致可
能有几分钟的数据丢失，根据save来策略进行持久化，Append Only File是另一种持久化方式，可以提供更好的
持久化特性。Redis会把每次写入的数据在接收后都写入 appendonly.aof 文件，每次启动时Redis都会先把这
个文件的数据读入内存里，先忽略RDB文件。若开启rdb则将no改为yes
appendonly no

指定本地数据库文件名，默认值为 appendonly.aof
appendfilename "appendonly.aof"


#aof持久化策略的配置
#no表示不执行fsync，由操作系统保证数据同步到磁盘，速度最快
#always表示每次写入都执行fsync，以保证数据同步到磁盘
#everysec表示每秒执行一次fsync，可能会导致丢失这1s数据
# appendfsync always
appendfsync everysec
# appendfsync no

# 在aof重写或者写入rdb文件的时候，会执行大量IO，此时对于everysec和always的aof模式来说，执行
fsync会造成阻塞过长时间，no-appendfsync-on-rewrite字段设置为默认设置为no。如果对延迟要求很高的
应用，这个字段可以设置为yes，否则还是设置为no，这样对持久化特性来说这是更安全的选择。设置为yes表
示rewrite期间对新写操作不fsync,暂时存在内存中,等rewrite完成后再写入，默认为no，建议yes。Linux的
默认fsync策略是30秒。可能丢失30秒数据
no-appendfsync-on-rewrite no

#aof自动重写配置。当目前aof文件大小超过上一次重写的aof文件大小的百分之多少进行重写，即当aof文件
增长到一定大小的时候Redis能够调用bgrewriteaof对日志文件进行重写。当前AOF文件大小是上次日志重写得
到AOF文件大小的二倍（设置为100）时，自动启动新的日志重写过程
auto-aof-rewrite-percentage 100

#设置允许重写的最小aof文件大小，避免了达到约定百分比但尺寸仍然很小的情况还要重写
auto-aof-rewrite-min-size 64mb

#aof文件可能在尾部是不完整的，当redis启动的时候，aof文件的数据被载入内存。重启可能发生在redis所
在的主机操作系统宕机后，尤其在ext4文件系统没有加上data=ordered选项（redis宕机或者异常终止不会造
成尾部不完整现象。）出现这种现象，可以选择让redis退出，或者导入尽可能多的数据。如果选择的是yes，
当截断的aof文件被导入的时候，会自动发布一个log给客户端然后load。如果是no，用户必须手动redis-
check-aof修复AOF文件才可以

#加载redis时，可以识别AOF文件以“redis”开头。
#字符串并加载带前缀的RDB文件，然后继续加载AOF尾巴
aof-use-rdb-preamble yes

#在aof重写的时候，如果打开了aof-rewrite-incremental-fsync开关，系统会每32MB执行一次fsync。这
对于把文件写入磁盘是有帮助的，可以避免过大的延迟峰值
aof-rewrite-incremental-fsync yes
```
# lua
```
# 如果达到最大时间限制（毫秒），redis会记个log，然后返回error。当一个脚本超过了最大时限。只有
SCRIPT KILL和SHUTDOWN NOSAVE可以用。第一个可以杀没有调write命令的东西。要是已经调用了write，只能
用第二个命令杀
lua-time-limit 5000
```
# 集群
```  
# 集群开关，默认是不开启集群模式
# cluster-enabled yes

#集群配置文件的名称，每个节点都有一个集群相关的配置文件，持久化保存集群的信息。这个文件并不需要手动
配置，这个配置文件有Redis生成并更新，每个Redis集群节点需要一个单独的配置文件，请确保与实例运行的系
统中配置文件名称不冲突
# cluster-config-file nodes-6379.conf

#节点互连超时的阀值。集群节点超时毫秒数
# cluster-node-timeout 15000

#在进行故障转移的时候，全部slave都会请求申请为master，但是有些slave可能与master断开连接一段时间
了，导致数据过于陈旧，这样的slave不应该被提升为master。该参数就是用来判断slave节点与master断线的时
间是否过长。判断方法是：
#比较slave断开连接的时间和(node-timeout * slave-validity-factor) + repl-ping-slave-period
#如果节点超时时间为三十秒, 并且slave-validity-factor为10,假设默认的repl-ping-slave-period是10
秒，即如果超过310秒slave将不会尝试进行故障转移
# cluster-replica-validity-factor 10

# master的slave数量大于该值，slave才能迁移到其他孤立master上，如这个参数若被设为2，那么只有当一
个主节点拥有2 个可工作的从节点时，它的一个从节点会尝试迁移
# cluster-migration-barrier 1

#默认情况下，集群全部的slot有节点负责，集群状态才为ok，才能提供服务。设置为no，可以在slot没有全
部分配的时候提供服务。不建议打开该配置，这样会造成分区的时候，小分区的master一直在接受写请求，而
造成很长时间数据不一致
# cluster-require-full-coverage yes
```
# 其他
``` 
#*群集公告IP
#*群集公告端口
#*群集公告总线端口
# Example:
#
# cluster-announce-ip 10.1.1.5
# cluster-announce-port 6379
# cluster-announce-bus-port 6380

# slog log是用来记录redis运行中执行比较慢的命令耗时。当命令的执行超过了指定时间，就记录在slow log
中，slog log保存在内存中，所以没有IO操作。
#执行时间比slowlog-log-slower-than大的请求记录到slowlog里面，单位是微秒，所以1000000就是1秒。注
意，负数时间会禁用慢查询日志，而0则会强制记录所有命令。
slowlog-log-slower-than 10000

#慢查询日志长度。当一个新的命令被写进日志的时候，最老的那个记录会被删掉。这个长度没有限制。只要有足
够的内存就行。你可以通过 SLOWLOG RESET 来释放内存
slowlog-max-len 128

#延迟监控功能是用来监控redis中执行比较缓慢的一些操作，用LATENCY打印redis实例在跑命令时的耗时图表。
只记录大于等于下边设置的值的操作。0的话，就是关闭监视。默认延迟监控功能是关闭的，如果你需要打开，也
可以通过CONFIG SET命令动态设置
latency-monitor-threshold 0
```

