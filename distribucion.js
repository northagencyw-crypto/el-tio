/**
 * EL TIO DISTRIBUCION
 *
 * EL PEDIDO QUE SE TRADUCE. Ocho renglones que entran en el idioma del cliente y se
 * resuelven de a uno mientras se baja. Seis salen solos; dos no salen.
 *
 * Es la respuesta a lo unico que el analisis de campo dejo abierto: los trece competidores
 * nombran el margen y ninguno explica donde se pierde. Se pierde en esos dos renglones.
 *
 * La pagina no avanza en ninguna direccion temporal, y este bloque tampoco. No es una
 * secuencia como la cuenta regresiva de eventos o la lista de asistencia de fitness: es
 * una traduccion, y se lee siempre el mismo tramo, de izquierda a derecha. Por eso lo que
 * se mueve no es una camara sino la columna de la derecha, que es la que hoy vive dentro
 * de la cabeza de una persona.
 *
 * Sin JavaScript los ocho renglones se ven resueltos, con los dos marcados como pendientes.
 * El respaldo es la conclusion, no una columna vacia.
 */
(function () {
  'use strict';

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  function montarPedido() {
    var lista = document.querySelector('[data-pedido]');
    if (!lista) return;
    var renglones = [].slice.call(lista.querySelectorAll('.ren'));
    if (!renglones.length) return;

    var salidaOk = document.querySelector('[data-resueltas]');
    var salidaPend = document.querySelector('[data-pendientes]');
    var pendientes = renglones.filter(function (r) { return r.classList.contains('ren--no'); }).length;

    if (quieto.matches) {
      renglones.forEach(function (r) { r.classList.add('leido'); });
      if (salidaOk) salidaOk.textContent = String(renglones.length - pendientes);
      if (salidaPend) salidaPend.textContent = pendientes + ' vuelven al vendedor.';
      return;
    }

    var pedido = 0;
    function revisar() {
      pedido = 0;
      // Por posicion y no con un IntersectionObserver: el observador avisa de lo que ESTA
      // cruzando el borde, asi que un scroll que salta por encima deja el renglon sin
      // resolver para siempre. Ya paso en real estate.
      var linea = window.innerHeight * 0.78;
      var leidos = 0;
      var ok = 0;
      for (var i = 0; i < renglones.length; i++) {
        var r = renglones[i];
        if (r.getBoundingClientRect().top < linea) {
          r.classList.add('leido');
          leidos++;
          if (r.classList.contains('ren--si')) ok++;
        }
      }
      if (salidaOk) salidaOk.textContent = String(ok);
      if (salidaPend) {
        var faltan = leidos - ok;
        salidaPend.textContent = leidos === 0
          ? 'Todavía sin leer.'
          : (faltan === 0
            ? 'Ninguna vuelve al vendedor, por ahora.'
            : faltan + (faltan === 1 ? ' vuelve al vendedor.' : ' vuelven al vendedor.'));
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

  /** Los renglones de conversion que ya existian, que aparecen al llegar. */
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
    montarPedido();
    montarEntradas();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }
})();
