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