# GSA-Github Social Analytics

## 项目部署（ubuntu)
### 1.依赖工具准备
- 安装mysql：
  ```
    sudo apt install mysql-server mysql-client　libmysqlclient-dev
  ```
- 安装python操作mysql的包MySQLdb：
  ```
    pip install mysql-python
  ```
- 安装flask：
  ```
    pip install Flask
  ```
- 安装scrapy：
  ```
    pip install scrapy
  ```
- 安装boto3：
  ```
    pip install boto3
  ```
  注：以上用pip安装的python包可能需要sudo权限，建议使用virtualenv工具．

### 2.环境变量准备
- sqs服务准备：
  * 在home目录下新建.aws文件夹
  * 在.aws下创建文件配置config，内容为：
    ```
      [default]
      region=cn-north-1
      output=json
    ```
  * 在.aws下创建身份认证文件credentials，内容为：
    ```
      [default]
      aws_access_key_id=your_key_id
      aws_secret_access_key=your_access_key
    ```
- mysql登录系统变量准备：
  在~/.bashrc文件末尾增加登录mysql的用户名与密码的环境变量：
  ```
    export MYSQL_USER=your_user_name
    export MYSQL_PWD=your_password
  ```
- 爬取github网站的token准备：
  登录github网站，找到setting->Personal access tokens创建自己的token，也可以用不同的帐号创建多个不同的token，将其添加在~/.bashrc文件末尾：
  ```
    export GITHUB_TOKENS=token1:token2:token3
  ```
### 3.部署运行
- 用命令行在mysql中创建了名为”gsa”的数据库；
- 到目录data/data/database下，运行脚本初始化数据库：
  ```
    python init_database.py
  ```
- 到目录data/data下，运行脚本清空sqs队列，再运行脚本开启sqs接收监控进程：
  ```
    python sqs_receive.py clear
    python sqs_receive.py
  ```
- 到目录/data/data/spiders下，新建log目录，运行脚本开启爬虫进程：
  ```
    mkdir log
    ./run.sh
  ```
  注：爬虫为后台进程，可用命令ps aux |grep scrapy查看进程信息，若要关闭爬虫请在新的窗口中使用./kill.sh（也在该目录下）脚本关闭，另外log文件在/data/data/spiders/log目录下．　
- 到目录/web下，运行脚本开启web服务：
  ```
    python main.py
  ```
- 在firefox或chrome浏览器中输入127.0.0.1:5000，若能正确接收到home页面的信息，并且数据库中基本信息正确的话，部署完成．
