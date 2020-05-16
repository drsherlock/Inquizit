from controllers import user_controller, room_controller


def setup_routes(app):
    app.add_routes(user_controller.routes)
    app.add_routes(room_controller.routes)
