/**
 * EL TIO FITNESS
 *
 * LA TIRA QUE SE VACIA. El mes de molinete, recorrido casilla por casilla mientras se baja.
 *
 * Es la tesis de la pagina hecha imagen: las marcas aparecen mientras la persona viene, se
 * cortan el dia que deja de venir, y el sistema recien se entera dieciseis casillas
 * despues, cuando rebota el debito. Esa distancia es el producto.
 *
 * Existe porque la tira ya estaba dibujada pero quieta, que es exactamente la critica que
 * el analisis de campo le hace a la competencia: la senal de la baja YA esta en sus heros,
 * pero como adorno. Una senal que no se mueve no es una senal, es una decoracion.
 *
 * Sin JavaScript la tira queda en su estado final, con las quince marcas y los dos hitos.
 * El respaldo es la conclusion, no una caja vacia.
 */
(function () {
  'use strict';

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  function montarMolinete() {
    var banda = document.querySelector('[data-molinete]');
    if (!banda) return;
    var casillas = [].slice.call(banda.querySelectorAll('.tira i'));
    if (casillas.length < 4) return;

    var ULTIMA = Number(banda.getAttribute('data-ultima')) || 15;
    var PAGO = Number(banda.getAttribute('data-pago')) || 27;
    var TOTAL = casillas.length;

    var salidaDias = banda.querySelector('[data-dias]');
    var salidaEstado = banda.querySelector('[data-estado]');
    var hitoBaja = banda.querySelector('.hito--baja');
    var hitoPago = banda.querySelector('.hito--pago');

    var hoy = 0;
    var objetivo = 0;
    var corriendo = false;

    function progreso() {
      var r = banda.getBoundingClientRect();
      var total = Math.max(1, banda.offsetHeight - window.innerHeight);
      return Math.min(1, Math.max(0, -r.top / total));
    }

    function pintar() {
      var d = Math.round(hoy);
      for (var i = 0; i < TOTAL; i++) {
        var c = casillas[i];
        // Antes de hoy y antes de la baja: vino. Antes de hoy y despues de la baja: hueco.
        var pasado = i < d;
        var vino = pasado && i < ULTIMA;
        c.classList.toggle('hay', vino);
        c.classList.toggle('hueco', pasado && !vino);
        c.classList.toggle('porvenir', !pasado);
      }
      if (hitoBaja) hitoBaja.classList.toggle('activo', d > ULTIMA);
      if (hitoPago) hitoPago.classList.toggle('activo', d >= PAGO);

      var sin = Math.max(0, d - ULTIMA);
      if (salidaDias) salidaDias.textContent = String(sin);
      if (salidaEstado) {
        salidaEstado.textContent = d < ULTIMA
          ? 'Viene. Todo en orden.'
          : (d < PAGO
            ? 'El sistema todavía no sabe nada.'
            : 'Recién ahora rebotó el débito, y ya es tarde.');
      }
      banda.classList.toggle('avisado', d >= PAGO);
    }

    function cuadro() {
      // Constante de tiempo y no un factor por cuadro: a 120 hertz un factor fijo corre el
      // doble de rapido que a 60, y el mes pasaria al doble de velocidad segun la pantalla.
      var ahora = performance.now();
      var dt = Math.min(0.05, (ahora - (cuadro.ultimo || ahora)) / 1000);
      cuadro.ultimo = ahora;
      hoy += (objetivo - hoy) * (1 - Math.pow(0.03, dt / 0.32));
      if (Math.abs(objetivo - hoy) < 0.02) hoy = objetivo;
      pintar();
      if (Math.abs(objetivo - hoy) > 0.01) requestAnimationFrame(cuadro);
      else corriendo = false;
    }

    function empujar() {
      objetivo = progreso() * TOTAL;
      if (quieto.matches) { hoy = objetivo; pintar(); return; }
      if (!corriendo) { corriendo = true; cuadro.ultimo = performance.now(); requestAnimationFrame(cuadro); }
    }

    var pedido = 0;
    function pedir() {
      if (pedido) return;
      pedido = requestAnimationFrame(function () { pedido = 0; empujar(); });
    }

    banda.classList.add('molinete-vivo');
    empujar();
    pintar();
    window.addEventListener('scroll', pedir, { passive: true });
    window.addEventListener('resize', pedir, { passive: true });
  }

  /**
   * Las entradas de bloque, por posicion y no con un IntersectionObserver.
   *
   * El observador avisa de lo que ESTA cruzando el borde: si el scroll salta por encima de
   * un bloque, ese bloque pasa de estar abajo a estar arriba sin cruzar nada y se queda
   * invisible para siempre. Ya paso en real estate y ahi se comio la unica prueba dura del
   * proyecto.
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
    montarMolinete();
    montarEntradas();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }
})();
