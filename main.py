from prodparser import ProductParser


if __name__ == '__main__':
    good = ProductParser()
    # details = good.parse('https://www.wildberries.ru/catalog/18256273/detail.aspx?targetUrl=MI')
    # details = good.parse('https://ozon.ru/product/ruchnaya-espresso-kofevarka-staresso-mini-324093592/?sh=IqdCzDwezw')
    # details = good.parse('https://www.ozon.ru/product/kapsulnaya-kofemashina-krups-piccolo-xs-krasnyy-178842724/?sh=yr-vOjksrA')
    details = good.parse('https://market.yandex.ru/product--kvadrokopter-dji-mavic-air-2-fly-more-combo/673833009')
