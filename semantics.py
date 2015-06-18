import web
render = web.template.render('templates/',base='layout')
class semantics_index:
    def GET(self):
        return render.semantics_index()

class semantics_show:
    def GET(self):
        return 'Semantics show'
