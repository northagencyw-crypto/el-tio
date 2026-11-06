/* Portada de eltio.net: selector «¿Cuál es tu rubro?». Sin JavaScript se ven los 7 rubros. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var chips = document.querySelectorAll('.chip');
  var paneles = document.querySelectorAll('.panel');
  var audits = document.querySelectorAll('a[data-cta="cabecera"], a[data-cta="cierre-audit"]');
  function elegir(id, guardar) {
    for (var i = 0; i < chips.length; i++) chips[i].setAttribute('aria-pressed', chips[i].id === 't-' + id ? 'true' : 'false');
    for (var j = 0; j < paneles.length; j++) paneles[j].hidden = paneles[j].dataset.rubro !== id;
    for (var k = 0; k < audits.length; k++) audits[k].href = audits[k].href.replace(/auditoria\/[^?]+/, 'auditoria/' + id);
    if (guardar) { try { localStorage.setItem('eltio-rubro', id); } catch (e) {} }
  }
  var inicial = 'gastronomia';
  try { var g = localStorage.getItem('eltio-rubro'); if (g && document.getElementById('p-' + g)) inicial = g; } catch (e) {}
  elegir(inicial, false);
  for (var i = 0; i < chips.length; i++) chips[i].addEventListener('click', function () {
    elegir(this.id.slice(2), true);
    if (window.fbq) try { fbq('trackCustom', 'ElegirRubro', { rubro: this.id.slice(2) }); } catch (e) {}
  });
})();
