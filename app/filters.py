class ID:
    @staticmethod
    def init_app(app):
        @app.template_filter('id_code')
        def id_code(arg):
            return arg[0:4] + "*" * (len(arg) - 8) + arg[-4:]
