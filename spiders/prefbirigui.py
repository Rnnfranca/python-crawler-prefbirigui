import scrapy
from my_crawler.items import MyCrawlerItem


class PrefbiriguiSpider(scrapy.Spider):
    name = 'prefbirigui'
    allowed_domains = ['birigui.sp.gov.br']
    start_urls = ['http://www.birigui.sp.gov.br/birigui/noticias/noticias.php']

    def parse(self, response):
        link = 'http://www.birigui.sp.gov.br'
        news_subtitle = response.xpath('//*[@id="conteudo"]/div[3]/div[2]/span/a/text()').get()
        # news_subtitle = response.xpath('//*[@id="conteudo"]/div[3]/div[4]/span/a/text()').get()

        if 'COVID-19: ' in news_subtitle:
            link += response.xpath('//*[@id="conteudo"]/div[3]/div[2]/span/a').attrib['href']
            # link += response.xpath('//*[@id="conteudo"]/div[3]/div[4]/span/a').attrib['href']
            yield response.follow(link, self.parse_news)
        else:
            print(news_subtitle)
            print("Não achou")
        # pass

    def parse_news(self, response):
        # salva a data
        date_selector = response.xpath('//*[@id="conteudo"]/div[2]/table[1]')
        date = date_selector.xpath('//tr/td/text()').get()
        # pega todos os <b> do html
        selector = response.xpath('//span')
        texts = []
        
        # mpega todos os span dentro de uma tag b
        for span in selector.xpath('.//span/text()'):
            # mostra o resultado
            texts.append(span.get())

        for i in range(len(texts)):
            if 'POSITIVOS: ' in texts[i]: 
                positivos = texts[i]
            if 'CURADOS: ' in texts[i]:
                curados = texts[i]
            if 'ÓBITOS CONFIRMADOS:' in texts[i]:
                obitos = texts[i]

        inf = MyCrawlerItem(date=date, positivos=positivos, curados=curados,  obitos=obitos)
        yield inf