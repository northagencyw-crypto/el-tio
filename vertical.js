/* EL TIO - landings verticales.

   Tres cosas y ninguna mas: los reveals, los parametros de campana y el
   registro de clics en los CTA. Sin librerias y sin scripts de terceros: una
   landing que carga un rastreador externo tarda mas y se lo come el rebote. */
(function () {
  'use strict';

  /* ---------- reveals ---------- */
  var reducido = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var elementos = document.querySelectorAll('.reveal');

  if (reducido || !('IntersectionObserver' in window)) {
    /* Sin observador el contenido tiene que verse igual. Un bloque invisible
       por falta de JavaScript es contenido que no existe. */
    elementos.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -5% 0px' });
    elementos.forEach(function (el) { io.observe(el); });
  }

  /* ---------- parametros de campana ----------
     Se guardan la primera vez que la persona entra y sobreviven a la
     navegacion interna: si vuelve al hero desde el pie, el origen sigue siendo
     el anuncio que la trajo, no la pagina. */
  var CLAVES = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  var GUARDADO = 'eltio_utm';

  function leerCampana() {
    var params = new URLSearchParams(location.search);
    var actual = {};
    CLAVES.forEach(function (k) {
      var v = params.get(k);
      if (v) actual[k] = v.slice(0, 120);
    });

    if (Object.keys(actual).length) {
      try { sessionStorage.setItem(GUARDADO, JSON.stringify(actual)); } catch (e) { /* modo privado */ }
      return actual;
    }
    try {
      return JSON.parse(sessionStorage.getItem(GUARDADO) || '{}');
    } catch (e) {
      return {};
    }
  }

  var campana = leerCampana();

  /* El origen viaja con la persona hasta donde pueda: en la agenda como
     parametros, y en WhatsApp o correo dentro del texto, que es lo unico que
     un enlace de esos admite. */
  function propagar() {
    var etiqueta = CLAVES
      .filter(function (k) { return campana[k]; })
      .map(function (k) { return k.replace('utm_', '') + '=' + campana[k]; })
      .join(' ');
    if (!etiqueta) return;

    document.querySelectorAll('a[data-cta]').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (!href) return;

      if (/^https?:/.test(href) && href.indexOf('wa.me') === -1) {
        var u = new URL(href);
        CLAVES.forEach(function (k) { if (campana[k]) u.searchParams.set(k, campana[k]); });
        a.setAttribute('href', u.toString());
        return;
      }
      if (href.indexOf('wa.me') !== -1 || href.indexOf('mailto:') === 0) {
        a.setAttribute('href', href + encodeURIComponent('\n\n[' + etiqueta + ']'));
      }
    });
  }
  propagar();

  /* ---------- clics en los CTA ----------
     Se apilan en una cola. El dia que exista una herramienta de medicion, la
     lee de aca. Hoy no sale nada del navegador, que es lo correcto mientras no
     haya politica de privacidad publicada. */
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-cta]');
    if (!a) return;
    window.dataLayer.push({
      evento: 'cta',
      cta: a.getAttribute('data-cta'),
      pagina: location.pathname,
      campana: campana
    });
  });
})();
