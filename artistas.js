/**
 * EL TIO ARTISTAS
 *
 * Dos piezas, y las dos son del concepto, no decoracion:
 *
 *   1. El sello se asienta una sola vez. Los trazos de audiencia crecen escalonados y
 *      despues nada mas se mueve en toda la pagina. Es lo contrario de eventos, donde el
 *      dibujo sigue al scroll: un catalogo no corre.
 *   2. El riel de caja se maneja con el teclado. Un bloque que se recorre en horizontal y
 *      que solo responde al mouse deja afuera a quien navega con teclado, y ademas en un
 *      contenedor con scroll horizontal el foco se mueve sin que la vista lo siga.
 *
 * Sin JavaScript la pagina se lee entera: las reglas de opacidad del sello cuelgan de
 * `html.js`, que se agrega en el head, y los lomos del riel se despliegan con :focus-within
 * y con la consulta de telefono.
 */
(function () {
  'use strict';

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  /**
   * El sello entra cuando se lo mira, y una sola vez.
   *
   * Por posicion y no con un IntersectionObserver: el observador avisa de lo que ESTA
   * cruzando el borde, asi que si el scroll salta por encima (el navegador restaurando la
   * posicion al recargar, un enlace con ancla, la rueda a fondo) el elemento pasa de estar
   * abajo a estar arriba sin cruzar nada y se queda invisible para siempre. Aca eso seria
   * el hero entero. Ya paso en real estate.
   */
  function montarSello() {
    var disco = document.querySelector('.disco');
    if (!disco) return;
    if (quieto.matches) { disco.classList.add('visible'); return; }

    var pedido = 0;
    function revisar() {
      pedido = 0;
      if (disco.getBoundingClientRect().top < window.innerHeight * 0.92) {
        disco.classList.add('visible');
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

  /**
   * El riel: flechas para pasar los lomos, y el lomo enfocado se abre.
   *
   * `scrollIntoView` con `block: 'nearest'` y no el que viene por defecto: el defecto
   * centra tambien en vertical, asi que pasar un lomo movia la pagina entera hacia arriba
   * y el bloque se iba de la pantalla mientras se lo recorria.
   */
  function montarRiel() {
    var riel = document.querySelector('.riel');
    if (!riel) return;
    var lomos = [].slice.call(riel.querySelectorAll('.lomo'));
    if (!lomos.length) return;

    // Cada lomo entra al orden de tabulacion: es contenido, no adorno.
    lomos.forEach(function (l) { l.setAttribute('tabindex', '0'); });

    var actual = 0;
    function ir(i) {
      actual = Math.max(0, Math.min(lomos.length - 1, i));
      var l = lomos[actual];
      l.focus({ preventScroll: true });
      l.scrollIntoView({
        behavior: quieto.matches ? 'auto' : 'smooth',
        inline: 'start',
        block: 'nearest',
      });
    }

    riel.addEventListener('keydown', function (e) {
      var k = e.key;
      if (k !== 'ArrowRight' && k !== 'ArrowLeft' && k !== 'Home' && k !== 'End') return;
      e.preventDefault();
      var foco = lomos.indexOf(document.activeElement.closest ? document.activeElement.closest('.lomo') : null);
      if (foco >= 0) actual = foco;
      if (k === 'ArrowRight') ir(actual + 1);
      else if (k === 'ArrowLeft') ir(actual - 1);
      else if (k === 'Home') ir(0);
      else ir(lomos.length - 1);
    });
  }

  function arrancar() {
    montarSello();
    montarRiel();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }
})();
