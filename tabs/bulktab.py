class BulkTab(object):

    def process_items(self):
        print('Processing {} items'.format(len(self._raw_tab)))
        itemlist = []
        for i, item_txt in enumerate(self._raw_tab):
            if i % 10 == 0:
                self.traderator.save_cache()
            item = BaseItem.get_item_cls(item_txt)
            #quick skip for not implemented
            if item is None:
                continue
            print('Found item - {}'.format(item))
            price_stuff = self.traderator.get_price_stats(item.item_hash, item.item_query)
            itemtuple = (str(item), item.position, price_stuff)
            itemlist.append(itemtuple)
        self.priced_items = itemlist
        print('Pricing finished, writing cache')
        self.traderator.save_cache()

    def display_results(self):
        val_items = [(iname, ipos, ival, ival[1])
                        for iname, ipos, ival in self.priced_items]
        print('Displaying maybe valuable bases')
        for iname, ipos, ival, compval in val_items:
            if compval > 3:
                print('{} - {}\n{}\n------'.format(iname, ipos, ival))
        print('Finished')