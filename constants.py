list_of_user_agents = [
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 
   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36', 
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36', 
   'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36', 
   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36', 
   'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060310 Linux Mint/6 (Felicia) Firefox/3.0.11', 
   'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.0.11) Gecko/2009060214 Firefox/3.0.11', 
   'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.11) Gecko/2009062218 Gentoo Firefox/3.0.11',
   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729) FirePHP/0.3', 
   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)', 
   'Mozilla/5.0 (Windows; U; Windows NT 6.0; sr; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12', 
   'Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)'
]

list_xpaths = [("//div[contains(@class,'flex-change')]//h2",'clarin'),
('(//h1)|(//h2)|(//h3)//a[(@class="com-link")][@title]','lanacion'),
('(//div[@class="news-article__title"]//h2)|(//h1[@class="news-article__title"])','c5n'),
('//div[@class="titulo"]//h2//a','eldestape'),
('//h2[contains(@class,"cst_hl dkt_fs")]//span','infobae'),
('//h3//a[@title and not(@class)][@title]','tn'),
('(//h1)|(//h2)//a[@title][@title]','lavoz'),
('//div[contains(@class, "article-title")]//a[not(@class)]','pagina12')]

media_urls = ["https://www.clarin.com/",
             "https://www.lanacion.com.ar",
             "https://www.c5n.com/",
             "https://www.eldestapeweb.com",
             "https://www.infobae.com/",
             "https://www.tn.com.ar/",
             "https://www.lavoz.com.ar/",
             "https://www.pagina12.com.ar/"]
