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

#### 定时任务运行方法,每隔5分抓一次数据存入sqllite
python3 schedule.py &
