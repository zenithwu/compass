## Spiders

This project contains two spiders and you can list them using the `list`
command:

    $ scrapy list

Both spiders extract the same data from the same website, but `toscrape-css`
employs CSS selectors, while `toscrape-xpath` employs XPath expressions.

You can learn more about the spiders by going through the
[Scrapy Tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html).


## Running the spiders

You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl toscrape-css

If you want to save the scraped data to a file, you can pass the `-o` option:
    
    $ scrapy crawl toscrape-css -o quotes.json
## deploy 
     first run server  any where is ok:
       $ scrapyd   
     then run deploy client  at dir of some ad scrapy.cfg:
       $ scrapyd-deploy
       
   
   
调度爬虫:curl http://localhost:6800/schedule.json -d project=compass -d spider=weather-spider

带上参数:curl http://localhost:6800/schedule.json -d project=compass -d spider=weather-spider -d setting=DOWNLOAD_DELAY=2 -d arg1=val1

取消运行:curl http://localhost:6800/cancel.json -d project=compass -d job=2bffadb6ed6411e883454ccc6aa82f02

列出项目:curl http://localhost:6800/listprojects.json

列出版本:curl http://localhost:6800/listversions.json?project=compass

列出爬虫:curl http://localhost:6800/listspiders.json?project=compass

列出job:curl http://localhost:6800/listjobs.json?project=compass

删除版本:curl http://localhost:6800/delversion.json -d project=compass -d version==1542786769

删除项目:curl http://localhost:6800/delproject.json -d project=compass
