#AntColony

[Simplechaindb](https://github.com/BUAANLSDE/Simplechaindb)的数据恢复程序。

## queenAnt

   中心节点恢复程序 。

   默认监听 9000 端口，接收各个节点的数据。

## workenAnt

   节点响应程序

   默认监听 9000 端口，接收中心节点广播消息。

## Dependencies

[leveldb](http://git.oschina.net/buaalining/AntColony/issues/1)  

[gevent](https://github.com/gevent/gevent)

## Instruction

### nodes-list 

 配置集群节点，每行一个节点IP。

### 运行

 首先启动所有的workenAnt
 
 python3 Worken.py
 
 然后启动 quennAnt
 
 python3 Broadcaster.py Ant.config
  
  







