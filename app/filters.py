class ID:
    @staticmethod
    def init_app(app):
        @app.template_filter('id_code')
        def id_code(arg):
            return arg[0:4] + "*" * (len(arg) - 8) + arg[-4:]


class STATUS:
    @staticmethod
    def init_app(app):
        @app.template_filter('exchange_status')
        def exchange_status(arg):
            arg = int(arg)
            if arg == 1:
                return "<span class='badge badge-primary'>等待配对方同意</span>"
            elif arg == 2:
                return "<span class='badge badge-info'>等待发起方加密</span>"
            elif arg == 3:
                return "<span class='badge badge-warning'>等待发起方验证</span>"
            elif arg == 4:
                return "<span class='badge badge-success'>交易成功</span>"
