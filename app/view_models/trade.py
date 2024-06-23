from app.view_models.book import BookViewModel


class TradeInfo:
    """对礼物或者心愿进行原始数据封装，满足前端展示需求"""

    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(i) for i in goods]

    def __map_to_trade(self, single):
        """single是一个模型
        user是表关联的模型
        create_time时间戳
        id当前的礼物护或心愿的id号"""
        if single.create_datetime:
            time = single.create_datetime.strftime("%Y-%m-%d")
        else:
            time = "未知"
        return dict(user_name=single.user.nickname, time=time, id=single.id)


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trade = []
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list
        # 不建议在一个类的方法中修改实例变量的值，推荐将需要修改的值返回在外部修改
        self.trade = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)

        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade_count["isbn"] == trade.isbn:
                count = trade_count["count"]

        return {"id": trade.id, "book": BookViewModel(trade.book), "wishes_count": count}
