#### 当当网爬取图书内容要求

1. 要求将`url='http://book.dangdang.com/'`的图书分类数据进行爬取，
2. 爬取内容如下：
    - 书本的分类（category）
    - 书本的名称(book_title)
    - 书本的价格(book_price)
    - 书本的描述(book_desc)
    - 书本的图片(book_img)
    - 书本详情页链接(book_href)
    - 书本的出版商(book_pub)
    - 书本的评论条数(comment_nums)
    - 书本的评论(book_comment)
 3. 使用scrapy_redis进行爬取
 4. 内容存储再redis和本地
 
 
 #### 爬虫操作
 ##### 基本操作流程
 - 进入目录文件，使用`scrapy startproject projectname`,创建一个爬虫项目
 - 使用`cd projectname`命令进行项目文件，在命令行:
    - 使用`scrapy genspider spidername allow_domain`创建普通爬虫
    - 使用`scrapy genspider -t crawl spidername allow_domain`
 - 在spider文件目录生成的py文件进行编程
    - 普通爬虫
    - 分布式爬虫
 - `scrapy_redis`去重
    - 函数继承的是`from scrapy_redis.spiders import RedisSpider`
    - 文件去除原有的`start_url`，加入`redis_key = xxx`
    - 执行文件：`scrapy crawl spidername`,系统运行到等待执行的url状态，
    - 在redis命令行中输入：`lpush redis_key_name allow_domain`命令，开始爬取数据。
 ##### 配置文件说明
 - settings文件
    - 日志配置
    - redis数据库及去重配置
    - piplines配置
    - middlewares配置
    - user_agent配置
    - ...
 - pipelines文件
 - items文件
 - middlewares文件