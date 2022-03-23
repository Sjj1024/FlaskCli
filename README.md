# FlaskCli
flask 项目脚手架，集成日志，认证，自动注册蓝图，sas模块等功能

#### 1.花木ETL任务：

仓库地址：https://gitlab.idatatlas.com/datamap-backend/petal_tasks

![img](https://img-blog.csdnimg.cn/9ae3f720bf134922b5ec77867d15f26d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

##### 花木自免疫案件：HuaMuZMY

1.从花木数据库获取
2.部分字段重命名
3.转存储到Collector



##### 花木自免疫流转：HuaMuFlow

1.取Collector里面的所有数据，获取最后更新时间updatetime

2.获取花木数据库中的数据，获取比更新时间updatetime 大的数据

3.将筛选后的数据存储到Collector里面



##### 花木电梯地址清洗：HuaMuEle

1.对源电梯表和目标电梯表数据进行比对
2.匹配到的数据进行修改
3.没匹配到的数据进行追加



#### 2.雅居乐插件

仓库地址：https://gitlab.idatatlas.com/datamap-backend/collector_plugins/-/tree/yjl-test

分支：yjl-test

功能：数据经过土地信息-temp表同步更新到土地信息表，只更新部分字段。

![img](https://img-blog.csdnimg.cn/e561a02d34ca457ab1e617ca7fbc7ab9.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

接口示例：

```
curl --location --request POST 'https://abctest.agile.com.cn/public/api/data/d175599c-7980-4bb4-b1c7-a7e5244f1e4a' \
--header 'content-type: application/json;charset=UTF-8' \
--header 'authorization: key=yajule&nonce=5973076471ef11ec92bcacde48001122&ts=1641803335&token=ed686883acb26ffd96632c9301e0da9d' \
--data-raw '{
    "extra": {
        "投资项目名称": "投资项目名称",
        "GUID": "caebc451-c962-4dbe-9845-7524a7928a50",
        "land_uuid": "345e9d0853b69788a010f25615162269",
        "is_new": false
    }
}'
```

更新成功后，会在土地信息临时表中生成一条记录，类似于log日志，同时会将：投资项目名称，GUID，land_uuid更新到土地信息表中。



#### 3.长三角智慧选址

项目地址：https://www.maicedata.com/statics/csj_zhihuixuanzhi/#/examination

![img](https://img-blog.csdnimg.cn/1d34803ee34740148d93489b03867d85.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

智慧选址collector地址：长三角示范区 开头的表，目前有19张表

https://www.maicedata.com/statics/collector_manager/#/

![img](https://img-blog.csdnimg.cn/e0d553a0e0064dcb8698641cb207df0f.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

数据来源：

从业务人员手里接的csv表格，特殊字段可能需要处理一下，比如是否，打表不达标等

暂时没有定时任务。

私有化后的地址：http://10.90.5.39:8081/statics/collector_manager/#/
账号：admin
密码：Abc@123!



#### 4.长三角智慧选址-用户认证服务

仓库地址：https://gitlab.idatatlas.com/haute-couture/digit-city-shanghai/csj_zhihuixuanzhi_server

项目部署：打包docker镜像部署，客户方是ARM架构的服务器。

启动之后，用的Nginx代理到了8089端口

服务功能和逻辑：解析用户信息并返回对应Collector用户的token

接收传递的id_token，通过publick_key解析出用户信息，根据用户信息中的ouId去表《长三角示范区-用户认证》查询是否存在对应的Collector用户，存在即生成token，不存在就创建一个默认的管理员用户，并生成token，最终将解析出来的用户信息和token返回给前端。![img](https://img-blog.csdnimg.cn/6e7fe2084d6242f3a01d3fc00f424b63.png)

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

Curl：

```
curl --location --request GET 'localhost:8084/token?id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5OTUxOTE3NTQyMDI1MTg1MTEifQ.eyJlbWFpbCI6IjEzMjM0MjFAcXEuY29tIiwibmFtZSI6Im1haWNlIiwibW9iaWxlIjpudWxsLCJleHRlcm5hbElkIjoiODk2OTM3MDYzMjU0MTE2MjEzIiwidWRBY2NvdW50VXVpZCI6ImQ4Nzc1NDBhN2E3N2Y0NzI5NmVjZmY5OTA3OTQzNzQ0U2tOYnhVTEptNXkiLCJvdUlkIjoiMjMyMDE4OTI4MDc2MDk5MzY1MSIsIm91TmFtZSI6IumVv-S4ieinkiIsIm9wZW5JZCI6bnVsbCwiaWRwVXNlcm5hbWUiOiJtYWljZSIsInVzZXJuYW1lIjoibWFpY2UiLCJhcHBsaWNhdGlvbk5hbWUiOiLmmbrog73pgInlnYBf6KeE5YiS566h55CGIiwiZW50ZXJwcmlzZUlkIjoiaWRhYXMiLCJpbnN0YW5jZUlkIjoiaWRhYXMiLCJhbGl5dW5Eb21haW4iOiIiLCJleHRlbmRGaWVsZHMiOnsidGhlbWVDb2xvciI6ImdyZWVuIiwiYXBwTmFtZSI6IuaZuuiDvemAieWdgF_op4TliJLnrqHnkIYifSwiZXhwIjoxNjQ2Mjc3MzA3LCJqdGkiOiJiMEkxMDBkbS1QYkdFdlpkZjN3S2lRIiwiaWF0IjoxNjQ2Mjc2NzA3LCJuYmYiOjE2NDYyNzY2NDcsInN1YiI6Im1haWNlIiwiaXNzIjoiaHR0cDovLzEwLjkwLjUuOTAvIiwiYXVkIjoiaWRhYXNwbHVnaW5fand0MTQifQ.LBs2fNgGDBAA4u7IJL66qsBQDaGx_txGFj0zSryp2yLEoQuB-3WwP_ael4vyBEqdpcnHFwRgcNfppO2q3VsHnCJ4M4VNcMSIaZsmWCzeXjG_p9b3wVObMJhQcvM1MzYWyCRwZ8aaZ5PRoHZYpmSfh2gQsg4Xaz-lzJQXzeb6y05v_I80HXygbQHaKCqKbAoZu_S6XR-GvVTl1RErx7OxjcP-koKHUTB15VDFWQmElaSWuBvv-eIJvLKgl6flENtaZoRxHSge3abkQeJWykoe_JAKm_TItbGQj9Dq_Do96y1-BALoLOOsqzLOycd-xufkxVLzfnpFx9bSmq4kDDgHYQ'
```

返回结果：

```
{
    "rs": 0,
    "token": "f927f2f8-2544-463b-b96d-25d2f3a0c348",
    "user_info": {
        "aliyunDomain": "",
        "applicationName": "智能选址_规划管理",
        "aud": "idaasplugin_jwt14",
        "email": "1323421@qq.com",
        "enterpriseId": "idaas",
        "exp": 1646277307,
        "extendFields": {
            "appName": "智能选址_规划管理",
            "themeColor": "green"
        },
        "externalId": "896937063254116213",
        "iat": 1646276707,
        "idpUsername": "maice",
        "instanceId": "idaas",
        "iss": "http://10.90.5.90/",
        "jti": "b0I100dm-PbGEvZdf3wKiQ",
        "mobile": null,
        "name": "maice",
        "nbf": 1646276647,
        "openId": null,
        "ouId": "2320189280760993651",
        "ouName": "长三角",
        "sub": "maice",
        "udAccountUuid": "d877540a7a77f47296ecff9907943744SkNbxULJm5y",
        "username": "maice"
    }
}
```





#### 5.静安数据同步

项目分支：petal_tasks -> jingan_v2分支

项目路径：src/petal_tasks/jingan_v2/data_merge

![img](https://img-blog.csdnimg.cn/1e37006cc64c47559e69f369da75123d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

ETL任务的逻辑：从Collector里面提取数据，并清洗出来静安需要的字段，再将数据批量映射过去

需要注意的点：全量企业这里面的数据量比较大，大概有10W多条，可能处理比较慢，需要3分钟左右才可以同步完成。类名称：QuanLiangQiYe

Collector地址：https://jabm.jingan.gov.cn/statics/collector_manager/#/

Airflow地址：https://jabm.jingan.gov.cn/airflow/home

![img](https://img-blog.csdnimg.cn/20e0e53d884149b5a2e3c5ae4ab0300d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)