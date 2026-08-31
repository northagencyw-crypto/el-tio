/**
 * EL TIO · PORTADA
 *
 * Una sola cosa: las entradas de bloque.
 *
 * Existe porque el HTML salio con `data-revela` y sin modulo que lo atendiera, asi que
 * las siete muestras del muestrario quedaron en opacidad cero para siempre. O sea: la
 * pagina cuyo contenido ENTERO son las siete muestras no mostraba ninguna. Lo agarro la
 * medicion, no el ojo, porque en la captura el fondo era el mismo carton de siempre.
 *
 * Por posicion y no con un IntersectionObserver. El observador avisa de lo que ESTA
 * cruzando el borde: si el scroll salta por encima de un bloque (el navegador restaurando
 * la posicion al recargar, un enlace con ancla, la rueda a fondo), ese bloque pasa de estar
 * abajo a estar arriba sin cruzar nada y se queda invisible. En esta pagina eso seria el
 * muestrario entero.
 *
 * Sin JavaScript todo se ve: la regla de opacidad cuelga de `html.js`, que se agrega en el
 * head.
 */
(function () {
  'use strict';

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

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
      var linea = window.innerHeight * 0.92;
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', montarEntradas);
  } else {
    montarEntradas();
  }
})();
