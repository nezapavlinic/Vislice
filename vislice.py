import bottle
import model

SECRET = 'skrivnost'

vislice = model.Vislice()
vislice.nalozi_igre_iz_datoteke()

@bottle.get('/')
def index():
    return bottle.template('index.tpl')

@bottle.post('/nova_igra/')
def nova_igra():
    id_igre = vislice.nova_igra()
    vislice.zapisi_igre_v_datoteko()
    bottle.response.set_cookie('id_igre', id_igre, path='/', secret=SECRET)
    return bottle.redirect(f'/igra/')

@bottle.get('/igra/')
def pokazi_igro():
    id_igre = bottle.request.get_cookie('id_igre', secret=SECRET)
    igra, stanje = vislice.igre[id_igre]
    return bottle.template('igra.tpl', igra=igra, id_igre=id_igre, stanje=stanje)

@bottle.post('/igra/')
def ugibaj():
    id_igre = bottle.request.get_cookie('id_igre', secret=SECRET)
    crka = bottle.request.forms.getunicode('crka')
    vislice.ugibaj(id_igre, crka)
    vislice.zapisi_igre_v_datoteko()
    bottle.redirect('/igra/')

@bottle.get('/img/<picture>')
def serve_pictures(picture):
    return bottle.static_file(picture, root='img')

bottle.run(reloader=True, debug=True)
