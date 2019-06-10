#### 部署方法

1. Python版本
   - Python3.7

2. 创建虚拟环境
    - virtualenv -p python3 ~/venv_caipiao
  
3. 激活上面的虚拟环境
    - source ~/venv_caipiao/bin/activate

4. 安装第三方包
    - pip install -r requirements.txt

##### 数据库文件
- caipiao.db是数据库文件，可以暂时放在git里

##### sqllite建表语句
- create_table.sql

#### 定时任务运行方法
- 比赛前每隔5分钟抓一次数据存入sqlite
- 比赛结果数据每天早上6点存入result表

python3 schedule.py &


#### 批量插入结果的方法
- 一次性插入过去1个月的比赛结果数据

python3 create_result_last_month.py

