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
