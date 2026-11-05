/* Medicion de eltio.net: pixel de Meta. Sin ID no carga nada. Nunca envia datos personales. */
(function () {
  var PIXEL_ID = "1542521264564309"; // ID del dataset de El Tio (Events Manager). Vacio = apagado.
  if (!/^\d{10,20}$/.test(PIXEL_ID)) return;
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', PIXEL_ID);
  fbq('track', 'PageView');
  var p = location.pathname.replace(/^\/(en|pt|fr|it|de|ja|zh)\//, '/');
  if (/^\/(paquetes|servicios|paginas-web|posicionamiento-en-ia|prospeccion-y-email)(\/|$)/.test(p)) {
    fbq('track', 'ViewContent', { content_name: p.split('/')[1] || 'inicio', content_category: 'servicios' });
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;
    var h = a.href;
    if (/^https:\/\/(wa\.me|api\.whatsapp\.com|ig\.me|m\.me)\//.test(h) || /instagram\.com\/(direct|eltio\.ia)/.test(h)) {
      fbq('track', 'Contact', { content_name: /wa\.me|whatsapp/.test(h) ? 'whatsapp' : 'dm' });
    }
  }, true);
})();
