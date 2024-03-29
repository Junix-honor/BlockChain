# WalleX——可跨链区块链钱包

## 一、安装环境要求

1. 操作系统：**Linux系统**（Ubuntu等）
2. 软件服务：Python 3.0、Truffle等

## 二、安装过程

1. 安装Python3.0和Truffle；
2. 根据requirements.txt文件安装运行所需的模块；
   ````
   pip install -r requirements.txt
   ````

## 三、经典使用流程

1. 本地搭建以太坊私有网络
    - 使用Ganache在本地搭建以太坊私有网络
2. 运行WalleX系统
    - 启动WEB服务器
        - 在文件的根目录，执行下述命令启动WEB服务器：
            ````
            export FLASK_APP=blockchain.py
            flask run
            ````
    - 进入WalleX系统界面
        - 服务器运行时，在Web浏览器的地址栏中输入服务器运行地址，即可进入WalleX系统界面。
 
## 四、数据库重置
1. 在文件的根目录，执行下述命令进入python shell：
   ````
    export FLASK_APP=blockchain.py
    flask shell
   ````
2. 在shell中执行下属命令重置数据库：
   ````
   from app import db
   db.drop_all()
   db.create_all()
   ````