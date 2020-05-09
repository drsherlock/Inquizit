from controllers import user_controller

def setup_routes(app):
    app.router.add_get('/', user_controller.handle)
    # app.router.add_get('/poll/{question_id}', poll, name='poll')
    # app.router.add_get('/poll/{question_id}/results',
    #                    results, name='results')
    # app.router.add_post('/poll/{question_id}/vote', vote, name='vote')
