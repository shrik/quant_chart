def init(context):
    context.s1 = "000001.XSHE"
    context.sum = 0 
    context.s2 = "000002.XSHE"
    logger.info("RunInfo: {}".format(context.run_info))

def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    order_shares(context.s1, 1000)
    order_shares(context.s1, -500)
    order_shares(context.s2, 1000)

def after_trading(context):
    pass
