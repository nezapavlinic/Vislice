% import model

<!DOCTYPE html>
<html>

<body>

  <h1>Vislice</h1>

  <h2>{{igra.pravilni_del_gesla()}}</h2>

  <p>Nepravilni ugibi: <b>{{igra.nepravilni_ugib()}}</b></p>

  <img src="/img/{{igra.stevilo_napak()}}.jpg" alt="obesanje">

% if stanje == model.ZMAGA:

  <h1>ZMAGA</h1>
  <form action="/igra/" method="post">
    <button type="submit">Nova igra</button>
  </form>

% elif stanje == model.PORAZ:

  <h1>PORAZ</h1>
  <p>Pravilno geslo: <b>{{igra.geslo}}</b></p>
  <form action="/igra/" method="post">
    <button type="submit">Nova igra</button>
  </form>

% else:

  <form action="/igra/{{id_igre}}/" method="post">
   Črka: <input type="text" name="crka" />
   <button type="submit">Ugibaj</button>
  </form>

% end

</body>

</html>