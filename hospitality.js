/**
 * EL TIO HOSPITALITY
 *
 * LA RECORRIDA. El hero: el pasillo de la propia casa, de noche, recorrido puerta por
 * puerta mientras se baja.
 *
 * Existe porque el hero anterior era un titular al lado de una foto, y las tres hermanas
 * rehechas tienen cada una un mecanismo de verdad: real estate baja de la orbita a la
 * terraza, eventos llena la sala hasta el punto de equilibrio y artistas dibuja el disco de
 * territorios. Este rubro tenia el suyo escrito en el eje: el itinerario del huesped,
 * umbral por umbral. Un pasillo con apliques que se encienden a medida que uno avanza es
 * ese eje hecho imagen.
 *
 * Se dibuja en canvas 2D con perspectiva de un punto. Nada de esto es una foto: la
 * categoria entera usa la misma foto de lobby luminoso en hora dorada, y el punto de esta
 * pagina es que el trabajo pasa cuando no hay nadie mirando.
 *
 * Sin JavaScript el hero se lee igual: el titular, la bajada y el boton son HTML, y la
 * lista de umbrales queda escrita en el noscript.
 */
(function () {
  'use strict';

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  function montarPasillo() {
    var escena = document.querySelector('[data-recorrida]');
    if (!escena) return;
    var caja = escena.querySelector('.pasillo-lienzo');
    if (!caja) return;

    var puertas = [].slice.call(escena.querySelectorAll('[data-umbral]')).map(function (el) {
      // Solo el nombre, no el `textContent` del renglon entero: el `li` lleva ademas el
      // numero y la descripcion, asi que la placa decia "05La salidaEl cierre, la factura
      // y lo que queda registrado" de un tiron.
      var b = el.querySelector('b');
      return { n: el.getAttribute('data-numero') || '', t: (b ? b.textContent : '').trim() };
    });
    if (puertas.length < 2) return;

    var salidaNum = escena.querySelector('[data-puerta-num]');
    var salidaNom = escena.querySelector('[data-puerta-nom]');

    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    canvas.setAttribute('role', 'img');
    canvas.setAttribute(
      'aria-label',
      'Pasillo de un hotel de noche dibujado en perspectiva, con ' + puertas.length +
      ' puertas numeradas a los lados y apliques de luz cálida entre ellas. Al bajar por la ' +
      'página se avanza por el pasillo y cada puerta se ilumina al pasar.'
    );
    caja.appendChild(canvas);

    var w = 0, h = 0, dpr = 1;
    function medir() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      var r = caja.getBoundingClientRect();
      w = Math.max(1, Math.round(r.width));
      h = Math.max(1, Math.round(r.height));
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    var PASO = 3.2;          // separacion entre puertas, en unidades de profundidad
    var ANCHO = 2.5;         // media anchura del pasillo
    var ALTO = 3.4;          // altura del pasillo
    var avance = 0;          // posicion de la camara
    var objetivo = 0;
    var corriendo = false;

    /** Proyeccion de un punto del pasillo a la pantalla. */
    function proy(x, y, z) {
      var d = Math.max(0.35, z - avance);
      var f = Math.min(w, h * 1.5) * 0.9;
      return { x: w / 2 + (x * f) / d, y: h * 0.52 - (y * f) / d, e: f / d };
    }

    function progreso() {
      var r = escena.getBoundingClientRect();
      var total = Math.max(1, escena.offsetHeight - window.innerHeight);
      return Math.min(1, Math.max(0, -r.top / total));
    }

    function pintar() {
      ctx.clearRect(0, 0, w, h);
      var fondo = ctx.createLinearGradient(0, 0, 0, h);
      fondo.addColorStop(0, '#0b1a14');
      fondo.addColorStop(1, '#08130f');
      ctx.fillStyle = fondo;
      ctx.fillRect(0, 0, w, h);

      // De atras hacia adelante, para que lo cercano tape a lo lejano.
      for (var i = puertas.length - 1; i >= 0; i--) {
        var z = 2.2 + i * PASO;
        if (z - avance < 0.4) continue;

        var cerca = 1 - Math.min(1, Math.max(0, (z - avance) / (PASO * 5.5)));
        var luz = Math.pow(cerca, 1.7);

        for (var lado = -1; lado <= 1; lado += 2) {
          var x = ANCHO * lado;
          var a = proy(x, -ALTO / 2, z);
          var b = proy(x, ALTO / 2, z);
          var c = proy(x, ALTO / 2, z + PASO * 0.62);
          var d2 = proy(x, -ALTO / 2, z + PASO * 0.62);

          // El pano de pared entre esta puerta y la siguiente.
          ctx.fillStyle = 'rgba(22, 48, 38,' + (0.5 + luz * 0.35).toFixed(3) + ')';
          ctx.beginPath();
          ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
          ctx.lineTo(c.x, c.y); ctx.lineTo(d2.x, d2.y);
          ctx.closePath();
          ctx.fill();

          // La puerta.
          var p1 = proy(x, -ALTO / 2 + 0.30, z + 0.12);
          var p2 = proy(x, ALTO / 2 - 1.05, z + 0.12);
          var p3 = proy(x, ALTO / 2 - 1.05, z + PASO * 0.42);
          var p4 = proy(x, -ALTO / 2 + 0.30, z + PASO * 0.42);
          ctx.fillStyle = 'rgba(9, 22, 17,' + (0.72 + luz * 0.2).toFixed(3) + ')';
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
          ctx.lineTo(p3.x, p3.y); ctx.lineTo(p4.x, p4.y);
          ctx.closePath();
          ctx.fill();
          ctx.strokeStyle = 'rgba(198, 152, 88,' + (0.10 + luz * 0.42).toFixed(3) + ')';
          ctx.lineWidth = Math.max(0.6, p2.e * 0.012);
          ctx.stroke();

          // La chapa de laton con el numero. Es el unico calido de la pagina y por eso es
          // lo unico que se lee de lejos.
          var ch = proy(x, 0.42, z + PASO * 0.30);
          var lado_ch = Math.max(2, ch.e * 0.10);
          ctx.fillStyle = 'rgba(198, 152, 88,' + (0.22 + luz * 0.72).toFixed(3) + ')';
          ctx.fillRect(ch.x - lado_ch / 2, ch.y - lado_ch * 0.62, lado_ch, lado_ch * 1.24);

          // El aplique, y su charco en el piso.
          var ap = proy(x * 0.92, 1.02, z + PASO * 0.80);
          var radio = Math.max(3, ap.e * 0.30);
          var halo = ctx.createRadialGradient(ap.x, ap.y, 0, ap.x, ap.y, radio);
          halo.addColorStop(0, 'rgba(226, 178, 108,' + (0.30 + luz * 0.45).toFixed(3) + ')');
          halo.addColorStop(1, 'rgba(226, 178, 108,0)');
          ctx.fillStyle = halo;
          ctx.beginPath();
          ctx.arc(ap.x, ap.y, radio, 0, Math.PI * 2);
          ctx.fill();

          var piso = proy(x * 0.72, -ALTO / 2, z + PASO * 0.80);
          var rp = Math.max(4, piso.e * 0.42);
          var charco = ctx.createRadialGradient(piso.x, piso.y, 0, piso.x, piso.y, rp);
          charco.addColorStop(0, 'rgba(198, 152, 88,' + (0.10 + luz * 0.26).toFixed(3) + ')');
          charco.addColorStop(1, 'rgba(198, 152, 88,0)');
          ctx.fillStyle = charco;
          ctx.beginPath();
          ctx.ellipse(piso.x, piso.y, rp, rp * 0.34, 0, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // El fondo del pasillo, que nunca se alcanza.
      var f1 = proy(-ANCHO, -ALTO / 2, avance + PASO * (puertas.length + 1.5));
      var f2 = proy(ANCHO, ALTO / 2, avance + PASO * (puertas.length + 1.5));
      ctx.fillStyle = 'rgba(6, 15, 12, 0.9)';
      ctx.fillRect(f1.x, f2.y, f2.x - f1.x, f1.y - f2.y);

      var enPuerta = Math.min(puertas.length - 1, Math.max(0, Math.round(avance / PASO)));
      if (salidaNum) salidaNum.textContent = puertas[enPuerta].n;
      if (salidaNom) salidaNom.textContent = puertas[enPuerta].t;
    }

    function cuadro() {
      // Constante de tiempo y no un factor por cuadro: a 120 hertz un factor fijo corre el
      // doble de rapido que a 60, y el pasillo se recorreria al doble de velocidad segun la
      // pantalla del que mira.
      var ahora = performance.now();
      var dt = Math.min(0.05, (ahora - (cuadro.ultimo || ahora)) / 1000);
      cuadro.ultimo = ahora;
      avance += (objetivo - avance) * (1 - Math.pow(0.03, dt / 0.4));
      if (Math.abs(objetivo - avance) < 0.004) avance = objetivo;
      pintar();
      if (Math.abs(objetivo - avance) > 0.002) requestAnimationFrame(cuadro);
      else corriendo = false;
    }

    function empujar() {
      objetivo = progreso() * PASO * (puertas.length - 1);
      if (quieto.matches) { avance = objetivo; pintar(); return; }
      if (!corriendo) { corriendo = true; cuadro.ultimo = performance.now(); requestAnimationFrame(cuadro); }
    }

    var pedido = 0;
    function pedir() {
      if (pedido) return;
      pedido = requestAnimationFrame(function () { pedido = 0; empujar(); });
    }

    medir();
    empujar();
    pintar();
    escena.classList.add('recorrida-viva');
    window.addEventListener('scroll', pedir, { passive: true });
    window.addEventListener('resize', function () { medir(); pintar(); }, { passive: true });
  }

  /**
   * Las entradas de bloque, por posicion y no con un IntersectionObserver.
   *
   * El observador avisa de lo que ESTA cruzando el borde: si el scroll salta por encima de
   * un bloque, ese bloque pasa de estar abajo a estar arriba sin cruzar nada y se queda
   * invisible para siempre. Ya paso en real estate.
   */
  function montarEntradas() {
    var piezas = [].slice.call(document.querySelectorAll('[data-revela]'));
    if (!piezas.length) return;
    if (quieto.matches) {
      piezas.forEach(function (el) { el.classList.add('visible'); });
      return;
    }
    var faltan = piezas.slice();
    var pedido = 0;
    function revisar() {
      pedido = 0;
      var linea = window.innerHeight * 0.9;
      for (var i = faltan.length - 1; i >= 0; i--) {
        if (faltan[i].getBoundingClientRect().top < linea) {
          faltan[i].classList.add('visible');
          faltan.splice(i, 1);
        }
      }
      if (!faltan.length) {
        window.removeEventListener('scroll', pedir);
        window.removeEventListener('resize', pedir);
      }
    }
    function pedir() {
      if (pedido) return;
      pedido = requestAnimationFrame(revisar);
    }
    revisar();
    window.addEventListener('scroll', pedir, { passive: true });
    window.addEventListener('resize', pedir, { passive: true });
  }

  function arrancar() {
    montarPasillo();
    montarEntradas();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }
})();
