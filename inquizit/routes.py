from controllers import user_controller


def setup_routes(app):
    app.add_routes(user_controller.routes)
