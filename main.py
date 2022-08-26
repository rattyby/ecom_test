from prodparser import ProductParser


if __name__ == '__main__':
    good = ProductParser()
    # details = good.parse('https://www.wildberries.ru/catalog/18166576/detail.aspx?targetUrl=WR')
    details = good.parse('https://ozon.ru/product/ruchnaya-espresso-kofevarka-staresso-mini-324093592/?sh=IqdCzDwezw')
    # details = good.parse('https://www.ozon.ru/product/kapsulnaya-kofemashina-krups-piccolo-xs-krasnyy-178842724/?sh=yr-vOjksrA')
    # details = good.parse('https://market.yandex.by/product--karta-pamiati-kingmax-sdhc-class-4/1561108?slug=karta-pamiati-kingmax-sdhc-class-4&productId=1561108&cpc=St02_avah7Cnf0g2VCiyh7vnv9AObTN6S_fK6x0192BWc8a0H7v5yL1g8xdZcxV_q-BxUSiCOMkWZb3VLsjou6NZgCDGOTYM4G_dQtQJEcggZx1HZ9hxdYh_CFsYR7ZA87gRtJb1Q3PcNIHVTU6abhRQQdDuFyNs_koqhOZ1hXnnzYdkUzlEgQ%2C%2C&show-uid=16613238073980432050516000&sku=101282624520&lr=157')
