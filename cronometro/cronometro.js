/* EL TIO - el Cronometro en la pagina.

   Lee el formulario, llama a CronometroCalculo.calcular y pinta el resultado,
   la cuenta y la tarjeta. No hay fetch, ni cookies, ni almacenamiento, ni
   scripts de terceros: lo que escribe el dueno no sale de su navegador. */
(function () {
  'use strict';

  var C = window.CronometroCalculo;
  var $ = function (id) { return document.getElementById(id); };

  var RUBROS = {
    'gastronomia': { nombre: 'local',
      noche: 'Deja una respuesta para después del cierre que pida nombre, día y número de personas. A la mañana confirmas tú y la mesa no se va a otro lado.' },
    'hospitality': { nombre: 'propiedad',
      noche: 'Deja una respuesta nocturna con lo que más te preguntan: fechas disponibles, estacionamiento y cómo reservar directo contigo.' },
    'real-estate': { nombre: 'inmobiliaria',
      noche: 'Deja una respuesta nocturna que pida zona, presupuesto y si busca compra o renta. A primera hora llamas con eso en la mano.' },
    'fitness': { nombre: 'gimnasio',
      noche: 'Deja una respuesta nocturna con los horarios de la clase de prueba y cómo apartar un lugar. Quien escribe de noche suele querer empezar mañana.' },
    'eventos': { nombre: 'productora',
      noche: 'Deja una respuesta nocturna con la fecha, dónde se compran las entradas y a qué hora abren puertas. Es lo que preguntan a esa hora.' },
    'artistas': { nombre: 'proyecto',
      noche: 'Deja una respuesta nocturna que separe a quien quiere contratarte del resto y le pida fecha, ciudad y tipo de evento.' },
    'distribucion': { nombre: 'distribuidora',
      noche: 'Deja una respuesta fuera de horario que pida el pedido completo en un solo mensaje y diga a qué hora llega la cotización.' }
  };
  var CONSEJO_HORARIO = 'En horario, un mensaje espera porque no tiene dueño. Decide quién contesta en cada franja del día y escríbelo donde lo vea todo el equipo. Tu equipo no es el problema. El proceso, sí.';
  var CONSEJO_NINGUNO = 'Contestas dentro de la hora. Eso tiene mérito. Lo que sigue es mirar qué pasa con los que preguntaron y no volvieron, y eso lo mira el Audit.';

  var AUDIT = 'https://app.eltio.net/auditoria/';
  var UTM = '?utm_source=cronometro&utm_medium=herramienta';

  var pesos = new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN', maximumFractionDigits: 0 });
  var entero = new Intl.NumberFormat('es-MX', { maximumFractionDigits: 0 });
  var dec = new Intl.NumberFormat('es-MX', { maximumFractionDigits: 2 });

  function radio(nombre) {
    var r = document.querySelector('input[name="' + nombre + '"]:checked');
    return r ? r.value : '';
  }

  function leer() {
    return {
      rubro: $('rubro').value,
      mensajes: $('mensajes').value,
      fueraDeHorario: radio('fuera'),
      respuestaHorario: radio('horario'),
      respuestaNoche: radio('noche'),
      compranDeCada10: $('compran').value,
      ticket: $('ticket').value,
      diasAlMes: $('dias').value,
      seVanDeCada10: $('sevan').value
    };
  }

  function de10(n) { return entero.format(n) + ' de 10'; }

  function formulas(r) {
    var e = r.entradas;
    var pct = function (x) { return dec.format(x * 100) + ' %'; };
    var lineas = [
      ['Mensajes que esperan en horario, por día',
        '<em>' + entero.format(e.mensajes) + '</em> mensajes × <em>' + pct(1 - e.fueraDeHorario) + '</em> en horario × <em>' + e.esperaEnHorario + '</em> (' + (e.esperaEnHorario ? 'tardas más de una hora' : 'contestas dentro de la hora') + ') = <em>' + dec.format(r.esperanEnHorarioPorDia) + '</em>'],
      ['Mensajes que esperan de noche, por día',
        '<em>' + entero.format(e.mensajes) + '</em> mensajes × <em>' + pct(e.fueraDeHorario) + '</em> fuera de horario × <em>' + e.esperaDeNoche + '</em> (' + (e.esperaDeNoche ? 'esperan más de una hora' : 'contestas dentro de la hora') + ') = <em>' + dec.format(r.esperanDeNochePorDia) + '</em>'],
      ['Mensajes que esperan más de una hora, al mes',
        '<em>' + dec.format(r.esperanPorDia) + '</em> por día × <em>' + entero.format(e.diasAlMes) + '</em> días = <em>' + entero.format(r.esperanAlMes) + '</em>'],
      ['Ventas que pasan por esos mensajes',
        '<em>' + entero.format(r.esperanAlMes) + '</em> × <em>' + de10(e.compranDeCada10) + '</em> que compran = <em>' + entero.format(r.ventasEnJuego) + '</em> al mes'],
      ['Dinero en juego',
        e.ticket === null ? 'Falta tu ticket promedio.' :
          '<em>' + entero.format(r.ventasEnJuego) + '</em> ventas × <em>' + pesos.format(e.ticket) + '</em> = <em>' + pesos.format(r.dineroEnJuego) + '</em> al mes'],
      ['Lo que se iría si se van ' + de10(e.seVanDeCada10) + ' (supuesto)',
        e.ticket === null ? 'Falta tu ticket promedio.' :
          '<em>' + pesos.format(r.dineroEnJuego) + '</em> × <em>' + de10(e.seVanDeCada10) + '</em> = <em>' + pesos.format(r.perdidaEstimada) + '</em> al mes']
    ];
    return lineas.map(function (l) { return '<li><div><b>' + l[0] + '</b><code>' + l[1] + '</code></div></li>'; }).join('');
  }

  var ultimo = null;

  function actualizar() {
    var e = leer();
    var r = C.calcular(e);
    var rubro = RUBROS[e.rubro] || RUBROS.gastronomia;
    ultimo = { r: r, rubro: e.rubro };

    $('compran-v').textContent = de10(r.entradas.compranDeCada10);
    $('sevan-v').textContent = de10(r.entradas.seVanDeCada10);
    $('r-sevan-t').textContent = de10(r.entradas.seVanDeCada10).replace(' de 10', ' de cada 10');

    $('r-esperan').textContent = entero.format(r.esperanAlMes);
    $('r-ventas').textContent = entero.format(r.ventasEnJuego) + ' al mes';
    var sinTicket = 'Pon tu ticket para verlo';
    $('r-dinero').textContent = r.dineroEnJuego === null ? sinTicket : pesos.format(r.dineroEnJuego) + ' al mes';
    $('r-perdida').textContent = r.perdidaEstimada === null ? sinTicket : pesos.format(r.perdidaEstimada) + ' al mes';

    $('r-consejo').textContent = r.foco === 'noche' ? rubro.noche : (r.foco === 'horario' ? CONSEJO_HORARIO : CONSEJO_NINGUNO);
    $('r-formulas').innerHTML = formulas(r);

    var url = AUDIT + encodeURIComponent(e.rubro) + UTM;
    $('cta-audit').href = url;
    $('cta-audit-2').href = url;
    $('cta-rubro').textContent = rubro.nombre;

    $('con-dinero').disabled = r.dineroEnJuego === null;
    pedirTarjeta();
  }

  /* ---------- la tarjeta ----------
     1080 × 1920, el formato de historias. Se dibuja en un canvas con las mismas
     fuentes y colores del sitio, y se descarga como PNG. */
  var foto = new Image();
  foto.src = '../assets/gas-tio-avatar.webp';
  var listo = Promise.all([
    new Promise(function (ok) { if (foto.complete && foto.naturalWidth) ok(); else { foto.onload = ok; foto.onerror = ok; } }),
    document.fonts ? Promise.all([
      document.fonts.load('800 100px Archivo'),
      document.fonts.load('400 30px Geist'),
      document.fonts.load('400 24px "Geist Mono"')
    ]).catch(function () {}) : Promise.resolve()
  ]);

  var pendiente = 0;
  function pedirTarjeta() {
    if (pendiente) return;
    pendiente = requestAnimationFrame(function () { pendiente = 0; listo.then(dibujar); });
  }

  function partir(ctx, texto, ancho) {
    var palabras = texto.split(' '), lineas = [], linea = '';
    palabras.forEach(function (p) {
      var prueba = linea ? linea + ' ' + p : p;
      if (ctx.measureText(prueba).width > ancho && linea) { lineas.push(linea); linea = p; }
      else linea = prueba;
    });
    if (linea) lineas.push(linea);
    return lineas;
  }

  function archivo(ctx, peso, px) {
    ctx.font = peso + ' ' + px + 'px Archivo, sans-serif';
    if ('fontStretch' in ctx) ctx.fontStretch = 'expanded';
  }
  function normal(ctx, fuente) {
    if ('fontStretch' in ctx) ctx.fontStretch = 'normal';
    ctx.font = fuente;
  }

  function dibujar() {
    if (!ultimo) return;
    var r = ultimo.r;
    var cv = $('tarjeta');
    var ctx = cv.getContext('2d');
    var W = 1080, H = 1920, M = 84;
    var CELESTE = '#7FC9F2', BLANCO = '#EDF1F4', GRIS = '#8794A1', VACIO = '#04070B';

    ctx.fillStyle = VACIO;
    ctx.fillRect(0, 0, W, H);

    // El Tio arriba, fundido al vacio.
    if (foto.naturalWidth) {
      ctx.globalAlpha = 0.92;
      ctx.drawImage(foto, 0, -90, W, W);
      ctx.globalAlpha = 1;
    }
    var g = ctx.createLinearGradient(0, 380, 0, 1000);
    g.addColorStop(0, 'rgba(4,7,11,0)');
    g.addColorStop(0.75, 'rgba(4,7,11,.92)');
    g.addColorStop(1, VACIO);
    ctx.fillStyle = g;
    ctx.fillRect(0, 380, W, 640);
    var gt = ctx.createLinearGradient(0, 0, 0, 220);
    gt.addColorStop(0, 'rgba(4,7,11,.85)');
    gt.addColorStop(1, 'rgba(4,7,11,0)');
    ctx.fillStyle = gt;
    ctx.fillRect(0, 0, W, 220);

    // Cabecera: wordmark y estado.
    ctx.textBaseline = 'alphabetic';
    archivo(ctx, 900, 40);
    ctx.fillStyle = BLANCO;
    ctx.textAlign = 'left';
    ctx.fillText('EL TÍO', M, 120);
    var anchoMarca = ctx.measureText('EL TÍO').width;
    ctx.fillStyle = CELESTE;
    ctx.fillText('.', M + anchoMarca + 2, 120);

    normal(ctx, '400 22px "Geist Mono", monospace');
    ctx.textAlign = 'right';
    ctx.fillStyle = GRIS;
    ctx.fillText('HECHO CON IA', W - M, 116);

    // Cuerpo.
    var y = 840;
    ctx.textAlign = 'left';
    normal(ctx, '400 24px "Geist Mono", monospace');
    ctx.fillStyle = CELESTE;
    ctx.fillText('EL CRONÓMETRO DEL TÍO', M, y);

    var negocio = ($('negocio').value || '').trim().slice(0, 40);
    var sujeto = negocio ? negocio.toUpperCase() : 'MI NEGOCIO';
    y += 90;

    if (r.esperanAlMes > 0) {
      var tam = 64, lineas;
      archivo(ctx, 800, tam);
      lineas = partir(ctx, sujeto + ' DEJA ESPERANDO', W - 2 * M);
      while (lineas.length > 2 && tam > 44) { tam -= 4; archivo(ctx, 800, tam); lineas = partir(ctx, sujeto + ' DEJA ESPERANDO', W - 2 * M); }
      ctx.fillStyle = BLANCO;
      lineas.forEach(function (l) { ctx.fillText(l, M, y); y += tam + 6; });

      var cifra = entero.format(r.esperanAlMes);
      var px = 260;
      archivo(ctx, 800, px);
      while (ctx.measureText(cifra).width > W - 2 * M && px > 120) { px -= 10; archivo(ctx, 800, px); }
      y += px * 0.74;
      ctx.fillStyle = CELESTE;
      ctx.fillText(cifra, M - 6, y);
      y += 108;

      archivo(ctx, 800, 62);
      ctx.fillStyle = BLANCO;
      ctx.fillText(r.esperanAlMes === 1 ? 'MENSAJE AL MES.' : 'MENSAJES AL MES.', M, y);
      y += 68;
      ctx.fillStyle = CELESTE;
      ctx.fillText('¿Y EL TUYO?', M, y);
    } else {
      archivo(ctx, 800, 84);
      ctx.fillStyle = BLANCO;
      partir(ctx, sujeto + ' CONTESTA DENTRO DE LA HORA.', W - 2 * M).slice(0, 5).forEach(function (l) { ctx.fillText(l, M, y); y += 88; });
      y += 10;
      ctx.fillStyle = CELESTE;
      ctx.fillText('¿Y EL TUYO?', M, y);
    }

    // Linea fina y pie de la cifra.
    y += 62;
    normal(ctx, '400 28px Geist, sans-serif');
    ctx.fillStyle = '#C9D2DA';
    var pie = r.esperanAlMes > 0 ? 'Mensajes de clientes que esperan más de una hora.' : 'Ningún mensaje de cliente espera más de una hora.';
    partir(ctx, pie, W - 2 * M).forEach(function (l) { ctx.fillText(l, M, y); y += 40; });

    if ($('con-dinero').checked && r.dineroEnJuego !== null && r.dineroEnJuego > 0) {
      y += 18;
      normal(ctx, '500 34px Geist, sans-serif');
      ctx.fillStyle = BLANCO;
      partir(ctx, pesos.format(r.dineroEnJuego) + ' al mes en ventas pasan por esos mensajes.', W - 2 * M).forEach(function (l) { ctx.fillText(l, M, y); y += 46; });
      normal(ctx, '400 24px Geist, sans-serif');
      ctx.fillStyle = GRIS;
      ctx.fillText('Estimación con mis números.', M, y);
    }

    // Pie de la tarjeta.
    ctx.strokeStyle = 'rgba(237,241,244,.14)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(M, H - 160); ctx.lineTo(W - M, H - 160); ctx.stroke();
    archivo(ctx, 800, 44);
    ctx.fillStyle = BLANCO;
    ctx.fillText('ELTIO.NET/CRONOMETRO', M, H - 92);
    normal(ctx, '400 22px "Geist Mono", monospace');
    ctx.fillStyle = GRIS;
    ctx.fillText('TIENES UN PROBLEMA. EL TÍO LO SOLUCIONA.', M, H - 50);
  }

  function blobTarjeta() {
    return listo.then(function () {
      dibujar();
      return new Promise(function (ok) { $('tarjeta').toBlob(ok, 'image/png'); });
    });
  }

  $('descargar').addEventListener('click', function () {
    blobTarjeta().then(function (blob) {
      if (!blob) return;
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'cronometro-el-tio.png';
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    });
  });

  // Compartir directo, solo donde el sistema acepta archivos (sobre todo telefonos).
  var compartir = $('compartir');
  try {
    if (navigator.canShare && navigator.canShare({ files: [new File([''], 'x.png', { type: 'image/png' })] })) compartir.hidden = false;
  } catch (err) { /* sin soporte */ }
  compartir.addEventListener('click', function () {
    blobTarjeta().then(function (blob) {
      if (!blob) return;
      var archivoPng = new File([blob], 'cronometro-el-tio.png', { type: 'image/png' });
      navigator.share({ files: [archivoPng], text: '¿Y el tuyo? eltio.net/cronometro' }).catch(function () {});
    });
  });

  document.addEventListener('input', actualizar);
  document.addEventListener('change', actualizar);
  $('cr-form').addEventListener('submit', function (ev) { ev.preventDefault(); });
  actualizar();

})();
