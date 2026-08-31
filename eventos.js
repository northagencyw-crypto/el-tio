/**
 * EL TIO EVENTOS
 *
 * Tres piezas, y ninguna es decoracion:
 *
 *   1. La reticula de aforo del hero. Ochocientas marcas que se encienden con el scroll,
 *      con la regla del umbral cortandolas. Es el numero que decide una fecha, mirado en
 *      vez de afirmado.
 *   2. El fader del riesgo. La misma aritmetica que la calculadora publica: costo fijo mas
 *      cachet, dividido por lo que deja cada entrada. No estima nada.
 *   3. Las entradas de bloque, por posicion y no con un IntersectionObserver.
 *
 * Sin JavaScript la pagina se lee entera: el hero deja su cuenta escrita en un noscript y
 * los bloques con `data-revela` quedan visibles porque la regla de opacidad cuelga de
 * `html.js`, que se agrega en el head.
 */
(function () {
  'use strict';

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  // ------------------------------------------------------------------ la reticula
  //
  // Canvas 2D y no WebGL. Ochocientos rectangulos por cuadro no justifican un contexto
  // de GPU, un programa, dos shaders y el manejo de contexto perdido: es complejidad que
  // se paga en bytes y en modos de falla, y aca no compra nada.

  function montarSala() {
    var sala = document.querySelector('[data-sala]');
    if (!sala) return;
    var caja = sala.querySelector('.sala-lienzo');
    var lectura = sala.querySelector('[data-lectura]');
    if (!caja) return;

    var AFORO = 800;
    var EQUILIBRIO = 620;
    var COLS = 40;
    var FILAS = AFORO / COLS;

    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    // El canvas NO es decorativo: es el hero entero. Va con rol y descripcion, y ademas la
    // lectura de al lado queda en texto con los numeros, que es mejor alternativa que una
    // etiqueta porque se actualiza sola mientras se baja.
    canvas.setAttribute('role', 'img');
    canvas.setAttribute(
      'aria-label',
      'Plano de una sala de ' + AFORO + ' localidades dibujado como una retícula de marcas. '
      + 'Las marcas se encienden desde el frente y desde el centro a medida que se baja por '
      + 'la página, y una regla corta la retícula en la localidad ' + EQUILIBRIO + ', que es '
      + 'el punto de equilibrio: las de abajo de esa regla son las que hacen falta para no '
      + 'perder y las de arriba son el margen.'
    );
    caja.appendChild(canvas);

    var salidaVendidas = lectura && lectura.querySelector('[data-vendidas]');
    var salidaEstado = lectura && lectura.querySelector('[data-estado]');

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

    // El orden en que se llena una sala no es de izquierda a derecha: se llena desde
    // adelante y desde el centro, que es donde todos quieren estar. Sin esto, la reticula
    // se lee como una barra de progreso rota en cuadraditos, que es justo lo que no
    // queremos.
    var orden = [];
    for (var i = 0; i < AFORO; i++) orden.push(i);
    orden.sort(function (a, b) {
      var fa = Math.floor(a / COLS), ca = a % COLS;
      var fb = Math.floor(b / COLS), cb = b % COLS;
      var da = fa * 2.6 + Math.abs(ca - (COLS - 1) / 2);
      var db = fb * 2.6 + Math.abs(cb - (COLS - 1) / 2);
      return da - db || a - b;
    });
    var rango = new Array(AFORO);
    for (var k = 0; k < AFORO; k++) rango[orden[k]] = k;

    var objetivo = 0;
    var actual = 0;
    var corriendo = false;

    function progreso() {
      // El recorrido es el alto que le sobra al hero por encima de una pantalla, que es
      // exactamente lo que se scrollea mientras el bloque queda pegado arriba. El primer
      // intento media contra el borde superior y daba 0,93 apenas cargaba la pagina: la
      // sala aparecia llena antes de tocar la rueda, que es justo lo que hace la categoria
      // y lo que esta pagina viene a no hacer.
      var r = sala.getBoundingClientRect();
      var total = Math.max(1, sala.offsetHeight - window.innerHeight);
      return Math.min(1, Math.max(0, -r.top / total));
    }

    function pintar() {
      ctx.clearRect(0, 0, w, h);

      // El plano: escenario arriba, la platea abajo. La reticula se dibuja en una caja
      // proporcional centrada, con un leve ensanche hacia el fondo para que se lea sala y
      // no planilla.
      var margenX = w * 0.06;
      var anchoUtil = w - margenX * 2;
      var altoUtil = h * 0.62;
      var y0 = h * 0.26;
      var paso = Math.min(anchoUtil / COLS, altoUtil / FILAS);
      var lado = Math.max(1.5, paso * 0.44);
      var totalAncho = paso * COLS;
      var x0 = (w - totalAncho) / 2;

      // El escenario.
      ctx.fillStyle = 'rgba(237,242,241,0.07)';
      ctx.fillRect(x0 + totalAncho * 0.22, y0 - paso * 2.6, totalAncho * 0.56, paso * 0.7);

      var vendidas = Math.round(actual);
      for (var idx = 0; idx < AFORO; idx++) {
        var fila = Math.floor(idx / COLS);
        var col = idx % COLS;
        var ensanche = 1 + fila * 0.006;
        var cx = x0 + totalAncho / 2 + (col - (COLS - 1) / 2) * paso * ensanche;
        var cy = y0 + fila * paso;
        var puesto = rango[idx];
        if (puesto < vendidas) {
          // Las que hacen falta para no perder se encienden en gel; las que sobran, en
          // blanco. Asi el umbral no es una linea sobre el dibujo: es un cambio de luz.
          ctx.fillStyle = puesto < EQUILIBRIO ? 'rgba(35,214,192,0.92)' : 'rgba(255,255,255,0.95)';
        } else {
          ctx.fillStyle = 'rgba(237,242,241,0.10)';
        }
        ctx.fillRect(cx - lado / 2, cy - lado / 2, lado, lado);
      }

      // La regla del umbral: cae donde termina la butaca numero 620 en el orden de
      // llenado, no en una columna fija.
      var fEq = Math.floor(EQUILIBRIO / COLS);
      var yEq = y0 + fEq * paso + paso * 0.5;
      ctx.strokeStyle = 'rgba(35,214,192,0.42)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 5]);
      ctx.beginPath();
      ctx.moveTo(x0 - paso, yEq);
      ctx.lineTo(x0 + totalAncho + paso, yEq);
      ctx.stroke();
      ctx.setLineDash([]);

      if (salidaVendidas) salidaVendidas.textContent = String(vendidas);
      if (salidaEstado) {
        var falta = EQUILIBRIO - vendidas;
        salidaEstado.textContent = vendidas === 0
          ? 'Sala vacía'
          : (falta > 0
            ? 'Faltan ' + falta + ' para no perder'
            : (vendidas >= AFORO ? 'Sala llena' : 'Margen de ' + (vendidas - EQUILIBRIO) + ' entradas'));
      }
    }

    function cuadro() {
      // Constante de tiempo y no un factor por cuadro: a 120 hertz un factor fijo corre el
      // doble de rapido que a 60, y la sala se llenaba al doble de velocidad segun la
      // pantalla.
      var ahora = performance.now();
      var dt = Math.min(0.05, (ahora - (cuadro.ultimo || ahora)) / 1000);
      cuadro.ultimo = ahora;
      var k = 1 - Math.pow(0.02, dt / 0.5);
      actual += (objetivo - actual) * k;
      if (Math.abs(objetivo - actual) < 0.4) actual = objetivo;
      pintar();
      if (Math.abs(objetivo - actual) > 0.2) requestAnimationFrame(cuadro);
      else corriendo = false;
    }

    function empujar() {
      objetivo = Math.round(progreso() * AFORO);
      if (quieto.matches) { actual = objetivo; pintar(); return; }
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
    window.addEventListener('scroll', pedir, { passive: true });
    window.addEventListener('resize', function () { medir(); pintar(); }, { passive: true });
  }

  // -------------------------------------------------------------------- el fader
  //
  // La misma aritmetica que la herramienta publica, y a proposito: si la pagina dijera un
  // numero y la calculadora otro, la pagina perderia lo unico que tiene para ofrecer, que
  // es que la cuenta se puede verificar.

  function montarConsola() {
    var consola = document.querySelector('[data-consola]');
    if (!consola) return;
    var faders = [].slice.call(consola.querySelectorAll('[data-fader]'));
    if (!faders.length) return;

    var salida = {
      entradas: consola.querySelector('[data-salida-entradas]'),
      pct: consola.querySelector('[data-salida-pct]'),
      juicio: consola.querySelector('[data-salida-juicio]'),
      barra: consola.querySelector('[data-salida-barra]'),
      ocu: consola.querySelector('[data-salida-ocu]'),
      margen: consola.querySelector('[data-salida-margen]'),
      siete: consola.querySelector('[data-salida-siete]'),
    };

    function leer(id) {
      var el = consola.querySelector('[data-fader="' + id + '"]');
      return el ? Number(el.value) : 0;
    }

    function recalcular() {
      var cachet = leer('cachet');
      var fijos = leer('fijos');
      var neto = Math.max(1, leer('neto'));
      var aforo = Math.max(1, leer('aforo'));

      var costo = cachet + fijos;
      var equilibrio = Math.ceil(costo / neto);
      var pct = Math.round((equilibrio / aforo) * 100);

      faders.forEach(function (f) {
        var v = consola.querySelector('[data-val="' + f.getAttribute('data-fader') + '"]');
        if (!v) return;
        var n = Number(f.value);
        v.textContent = f.getAttribute('data-fader') === 'aforo' || f.getAttribute('data-fader') === 'neto'
          ? String(n)
          : n.toLocaleString('es-AR');
      });

      if (salida.entradas) salida.entradas.textContent = String(equilibrio);
      if (salida.pct) salida.pct.textContent = String(pct);
      if (salida.barra) salida.barra.style.width = Math.min(100, pct) + '%';
      if (salida.ocu) salida.ocu.textContent = String(pct);
      if (salida.margen) salida.margen.textContent = String(Math.max(0, aforo - equilibrio));
      if (salida.siete) {
        var siete = Math.round(aforo * 0.7);
        var dif = siete - equilibrio;
        salida.siete.textContent = siete + ' entradas, ' + Math.abs(dif)
          + (dif >= 0 ? ' por encima del umbral' : ' por debajo del umbral');
      }
      if (salida.juicio) {
        salida.juicio.textContent = pct > 100
          ? 'No entra en la sala: con estos números la fecha pierde llena.'
          : (pct >= 80
            ? 'Es riesgo alto: hay que llenar casi la sala solo para empatar.'
            : (pct >= 60
              ? 'Es riesgo medio: queda poco margen para un mal día.'
              : 'Debajo de eso, la fecha pierde plata.'));
      }
    }

    faders.forEach(function (f) {
      f.addEventListener('input', recalcular);
      f.addEventListener('change', recalcular);
    });
    recalcular();
  }

  // ------------------------------------------------------------------ las entradas
  //
  // Por posicion y no con un IntersectionObserver. El observador avisa de lo que ESTA
  // cruzando el borde: si el scroll salta por encima de un bloque (el navegador
  // restaurando la posicion al recargar, un enlace con ancla, la rueda a fondo), ese
  // bloque pasa de estar abajo a estar arriba sin cruzar nada y se queda en opacidad cero
  // para siempre. Ya paso en real estate, y ahi se comio la seccion con la unica prueba
  // dura del proyecto.

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
    montarSala();
    montarConsola();
    montarEntradas();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }
})();
