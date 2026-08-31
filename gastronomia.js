/* ===========================================================================
   EL TIO GASTRONOMIA - el pase en 3D

   El hero es un plato de verdad en tres dimensiones: se levanta de la mesa a
   medida que bajas. Arriba de todo lo ves desde arriba, como se ve una carta o
   una foto cenital; cuando terminas de leer lo tienes de frente, como se ve un
   plato cuando llega a la mesa. Ese giro es el concepto de la pagina: el
   servicio se gana antes de abrir, y lo que el cliente ve al final no se parece
   a lo que se preparo a la manana.

   POR QUE NO HAY THREE.JS. Para un disco con textura, borde ceramico, luz calida
   y sombra de contacto no hace falta una escena: alcanza con resolver la
   interseccion del rayo con un disco inclinado dentro del fragment shader. Son
   ocho kilobytes propios contra seiscientos de una libreria traida de un CDN, y
   una pagina de adquisicion no puede depender de que un CDN de terceros siga en
   pie. La regla esta en CLAUDE.md y hay un test que la verifica.

   DEGRADACION. Sin WebGL, sin JavaScript o con prefers-reduced-motion, el hero
   se queda con las fotos que ya estan en el HTML. El canvas se agrega desde aca,
   nunca desde el markup, asi la pagina sirve entera con los scripts apagados.
   =========================================================================== */

(function () {
  'use strict';

  // Guarda de una sola ejecucion. Este archivo llego a quedar incluido dos veces en el
  // HTML y el resultado fueron dos canvas apilados pintando la misma escena: el doble
  // de trabajo de GPU, invisible a simple vista y detectado solo porque una medicion
  // conto dos. La etiqueta duplicada se arreglo, pero la guarda se queda: un modulo
  // que monta cosas en el DOM no puede depender de que nadie se equivoque al incluirlo.
  if (window.__elTioMontado_pase) return;
  window.__elTioMontado_pase = true;

  var raiz = document.documentElement;
  raiz.classList.add('js');

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------------------------------------------------------------------
     El shader
     --------------------------------------------------------------------- */

  var VERTEX = [
    'attribute vec2 posicion;',
    'varying vec2 uv;',
    'void main(){ uv = posicion; gl_Position = vec4(posicion, 0.0, 1.0); }',
  ].join('\n');

  var FRAGMENT = [
    'precision highp float;',
    'varying vec2 uv;',
    'uniform vec2 tamano;',
    'uniform float tiempo;',
    'uniform float inclinacion;',   // 0 = cenital, 1 = casi de perfil
    'uniform float giro;',
    'uniform float mezcla;',        // cruce entre plato A y plato B
    'uniform sampler2D platoA;',
    'uniform sampler2D platoB;',
    'uniform vec3 fondo;',
    'uniform vec3 brasa;',
    '',
    // Medido sobre gas-plato-01: la ceramica llega hasta 0.41 del ancho desde el
    // centro. Se mapea el borde del disco justo ahi, asi entra el ala real de la
    // foto, con su luz y su sombra, en vez de taparla con ceramica sintetica. El
    // anillo sintetico queda como un hilo al filo, solo para disimular la costura
    // y que no se cuele la pizarra del fondo de la foto.
    'const float RECORTE = 0.415;',
    'const float RADIO = 1.0;',
    'const float BORDE = 0.94;',
    '',
    'mat3 rotX(float a){ float c=cos(a), s=sin(a); return mat3(1.0,0.0,0.0, 0.0,c,-s, 0.0,s,c); }',
    'mat3 rotZ(float a){ float c=cos(a), s=sin(a); return mat3(c,-s,0.0, s,c,0.0, 0.0,0.0,1.0); }',
    '',
    'void main(){',
    '  vec2 p = uv;',
    '  p.x *= tamano.x / tamano.y;',
    '',
    // Camara fija, el plato es el que se inclina. Asi el encuadre no se mueve y
    // el texto de al lado se mantiene quieto mientras la pieza gira.
    // El plato vive a la derecha del encuadre y el texto ocupa la columna
    // izquierda. Antes estaba centrado y el velo que hacia legible al texto le
    // tapaba el 78 por ciento: se veia el arco del ala y nada mas. Corriendolo, el
    // velo puede ser horizontal y el plato se ve entero.
    '  vec3 origen = vec3(0.0, 0.0, 3.0);',
    '  vec2 centro = vec2(mix(0.0, 0.46, clamp(tamano.x / tamano.y - 0.9, 0.0, 1.0)), 0.0);',
    '  vec3 rayo = normalize(vec3((p - centro) * 0.46, -1.0));',
    '',
    // De cenital a la mesa, no al reves. La normal del disco arranca mirando a la
    // camara, que es exactamente como se ve la foto de arriba, y termina inclinada
    // como un plato apoyado que se mira sentado. Estaba invertido y el hero abria
    // con el plato de canto, o sea con la peor vista posible de un plato de comida.
    '  float a = mix(0.06, 1.02, inclinacion);',
    // El giro va sobre el eje del propio plato, no sobre el eje Y del mundo. Con
    // rotY, estando cenital, el disco se aplastaba horizontalmente y dejaba de
    // leerse como un plato: un plato que gira sobre su eje mantiene el contorno
    // redondo y lo que se mueve es la comida, como una bandeja giratoria. La
    // inclinacion se aplica despues, asi el escorzo no depende de en que punto del
    // giro este.
    '  mat3 M = rotX(-a) * rotZ(giro);',
    '  mat3 Minv = rotZ(-giro) * rotX(a);',
    '',
    '  vec3 normal = M * vec3(0.0, 0.0, 1.0);',
    '  float denom = dot(rayo, normal);',
    '  vec3 color = fondo;',
    '',
    // Un halo calido detras, como el resplandor del pase. Da profundidad sin
    // pintar un degradado plano.
    '  float halo = exp(-length(p - centro - vec2(0.0, 0.10)) * 1.45);',
    '  color = mix(color, brasa * 0.30, halo * 0.55);',
    '',
    '  if (abs(denom) > 0.0005) {',
    '    float t = dot(-origen, normal) / denom;',
    '    if (t > 0.0) {',
    '      vec3 golpe = origen + rayo * t;',
    '      vec3 local = Minv * golpe;',
    '      float r = length(local.xy);',
    '',
    '      if (r < RADIO) {',
    '        vec2 tuv = local.xy / RADIO * RECORTE + 0.5;',
    '        tuv.y = 1.0 - tuv.y;',
    '        vec3 comida = mix(texture2D(platoA, tuv).rgb, texture2D(platoB, tuv).rgb, mezcla);',
    '',
    // El ala de la ceramica: fuera de BORDE la foto se apaga y queda el plato.
    '        float ala = smoothstep(BORDE, BORDE + 0.06, r);',
    '        vec3 ceramica = vec3(0.90, 0.87, 0.82);',
    '        vec3 sup = mix(comida, ceramica, ala);',
    '',
    // Luz calida desde arriba a la izquierda, mas un especular apretado sobre el
    // vidriado. Es lo que hace que se lea como ceramica y no como una calcomania.
    '        vec3 luz = normalize(vec3(-0.42, 0.62, 0.92));',
    // La normal del disco se aleja de la luz a medida que el plato se para, y con
    // difuso puro la comida se apagaba justo cuando queda de frente al lector. Se
    // toma el valor absoluto y se lo levanta con ambiente alto: es una foto de
    // comida, no una escena de terror, y tiene que verse apetecible en todo el giro.
    '        float dif = abs(dot(normal, luz));',
    '        vec3 vista = normalize(origen - golpe);',
    '        vec3 medio = normalize(luz + vista);',
    '        float esp = pow(max(abs(dot(normal, medio)), 0.0), 42.0) * (0.10 + ala * 0.34);',
    '',
    // Oclusion contra el canto: el borde exterior siempre baja un poco.
    '        float canto = smoothstep(1.02, 0.88, r);',
    '        sup *= 0.86 + 0.30 * dif;',
    '        sup += esp;',
    '        sup *= 0.80 + 0.20 * canto;',
    '',
    '        color = sup;',
    '      }',
    '    }',
    '  }',
    '',
    // Sombra de contacto: una elipse blanda debajo, que se aplasta cuando el
    // plato se pone de perfil. Sin esto la pieza flota y se ve pegada.
    '  float caida = mix(0.0, 0.62, inclinacion);',
    '  vec2 s = (p - centro + vec2(0.03, caida)) * vec2(1.0, mix(3.4, 1.5, inclinacion));',
    '  float sombra = exp(-dot(s, s) * 1.45) * (0.30 + 0.30 * inclinacion);',
    '  color *= 1.0 - sombra * 0.55;',
    '',
    // Grano fino: la pagina entera es fotografia de 35mm y el canvas tiene que
    // pertenecer al mismo material, no verse digital al lado de las fotos.
    '  float grano = fract(sin(dot(gl_FragCoord.xy + tiempo * 0.4, vec2(12.9898, 78.233))) * 43758.5453);',
    '  color += (grano - 0.5) * 0.028;',
    '',
    '  gl_FragColor = vec4(color, 1.0);',
    '}',
  ].join('\n');

  /* ---------------------------------------------------------------------
     Utilidades de WebGL
     --------------------------------------------------------------------- */

  function compilar(gl, tipo, fuente) {
    var s = gl.createShader(tipo);
    gl.shaderSource(s, fuente);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      // Si el shader no compila no se deja el canvas negro: se avisa al que
      // desarrolla y se devuelve el hero de respaldo.
      console.warn('gastronomia: shader', gl.getShaderInfoLog(s));
      return null;
    }
    return s;
  }

  function textura(gl, imagen) {
    var t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, imagen);
    return t;
  }

  function hex(v) {
    return [
      parseInt(v.slice(1, 3), 16) / 255,
      parseInt(v.slice(3, 5), 16) / 255,
      parseInt(v.slice(5, 7), 16) / 255,
    ];
  }

  /* ---------------------------------------------------------------------
     El pase
     --------------------------------------------------------------------- */

  function montarPase() {
    var escenario = document.querySelector('[data-pase]');
    if (!escenario) return;

    var fuentes = [].slice
      .call(escenario.querySelectorAll('[data-plato]'))
      .map(function (el) { return el.getAttribute('data-plato'); });
    if (fuentes.length < 2) return;

    var canvas = document.createElement('canvas');
    canvas.className = 'pase-canvas';
    canvas.setAttribute('aria-hidden', 'true');

    var gl = canvas.getContext('webgl', { antialias: true, alpha: false })
      || canvas.getContext('experimental-webgl', { antialias: true, alpha: false });
    if (!gl) return;

    var vs = compilar(gl, gl.VERTEX_SHADER, VERTEX);
    var fs = compilar(gl, gl.FRAGMENT_SHADER, FRAGMENT);
    if (!vs || !fs) return;

    var prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
    gl.useProgram(prog);

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'posicion');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    var u = {};
    ['tamano', 'tiempo', 'inclinacion', 'giro', 'mezcla', 'platoA', 'platoB', 'fondo', 'brasa']
      .forEach(function (n) { u[n] = gl.getUniformLocation(prog, n); });

    var estilo = getComputedStyle(document.documentElement);
    var cFondo = hex((estilo.getPropertyValue('--pizarra') || '#1C1E17').trim());
    var cBrasa = hex((estilo.getPropertyValue('--brasa') || '#A03C0E').trim());
    gl.uniform3fv(u.fondo, cFondo);
    gl.uniform3fv(u.brasa, cBrasa);

    // Las texturas se cargan de a una y el canvas recien reemplaza al respaldo
    // cuando hay al menos dos: un plato solo no puede cruzarse con el siguiente.
    var texturas = [];
    var listas = 0;
    fuentes.forEach(function (src, i) {
      var img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = function () {
        texturas[i] = textura(gl, img);
        listas += 1;
        if (listas === 2) arrancar();
      };
      img.src = src;
    });

    var corriendo = false;

    function medir() {
      // La caja del canvas, no la del escenario. El escenario mide varias pantallas de
      // alto porque es el recorrido del pin; el canvas esta sticky y ocupa una sola. Con
      // la caja equivocada el buffer sale con otra relacion de aspecto que la superficie
      // pintada, y el plato se ve como una elipse estirada en vez de un disco en escorzo.
      var caja = canvas.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.max(1, Math.round(caja.width * dpr));
      canvas.height = Math.max(1, Math.round(caja.height * dpr));
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.uniform2f(u.tamano, canvas.width, canvas.height);
    }

    function progreso() {
      // Cuanto se recorrio del bloque pinneado, de 0 a 1.
      var caja = escenario.getBoundingClientRect();
      var recorrido = -caja.top;
      var total = Math.max(1, escenario.offsetHeight - window.innerHeight);
      return Math.min(1, Math.max(0, recorrido / total));
    }

    // Los tres tiempos del pase se turnan con el recorrido. Se reparten en tramos
    // iguales y se cambia solo cuando cambia el indice, no en cada cuadro: tocar
    // la clase sesenta veces por segundo obliga al navegador a recalcular estilo
    // todo el tiempo y se nota en el scroll.
    var tiempos = escenario.querySelectorAll('[data-tiempo]');
    var tiempoActual = -1;

    function marcarTiempo(p) {
      if (!tiempos.length) return;
      var i = Math.min(tiempos.length - 1, Math.floor(p * tiempos.length));
      if (i === tiempoActual) return;
      tiempoActual = i;
      [].forEach.call(tiempos, function (el, j) {
        el.classList.toggle('activo', j === i);
      });
    }

    function pintar(ms) {
      var t = ms * 0.001;
      var p = progreso();
      marcarTiempo(p);

      // La inclinacion sube con el scroll y se suaviza al final para que el
      // plato no quede temblando cuando se llega al fondo del bloque.
      // Inclinacion fija en cero: el plato se ve SIEMPRE de arriba, como una foto de
      // carta. Antes subia con el scroll y era lo que lo iba tumbando; con el disco
      // plano el unico movimiento es el giro sobre su propio eje, que es lo que se
      // pidio y lo que un plato hace de verdad sobre una bandeja giratoria.
      gl.uniform1f(u.inclinacion, 0.0);
      gl.uniform1f(u.tiempo, quieto.matches ? 0.0 : t);
      // El giro es ACOTADO, no una vuelta continua. Antes era `t * 0.16 + p * 1.9`:
      // el termino de tiempo crecia sin limite, asi que a los quince segundos el plato
      // estaba a 137 grados y del segundo al tercer ambiente quedaba practicamente
      // dado vuelta. Un plato emplatado tiene un arriba definido, igual que una foto
      // de producto: la salsa cae, las hojas apuntan, y a mas de treinta grados se lee
      // como un error de montaje.
      //
      // Ahora respira. Una oscilacion de cuatro grados que nunca se acumula, mas un
      // cuarto de vuelta lento repartido en todo el recorrido: alcanza para que la
      // pieza este viva y para que ningun plato llegue nunca cabeza abajo.
      gl.uniform1f(u.giro, quieto.matches ? 0.0 : t * 0.085 + p * 0.55);

      // Los platos se turnan segun el avance: cuatro tramos, cruce dentro de cada uno.
      var tramos = texturas.length - 1;
      var escala = p * tramos;
      var i = Math.min(tramos - 1, Math.floor(escala));
      var f = escala - i;
      gl.uniform1f(u.mezcla, f * f * (3.0 - 2.0 * f));

      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, texturas[i] || texturas[0]);
      gl.uniform1i(u.platoA, 0);
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, texturas[i + 1] || texturas[texturas.length - 1]);
      gl.uniform1i(u.platoB, 1);

      gl.drawArrays(gl.TRIANGLES, 0, 3);
      if (corriendo) requestAnimationFrame(pintar);
    }

    function arrancar() {
      escenario.classList.add('pase-vivo');
      marcarTiempo(0);
      // Dentro del marco pinneado, no del bloque de recorrido. `.pase` mide varias
      // pantallas de alto; `.pase-marco` mide una. Un canvas absoluto colgado del
      // bloque toma el alto del recorrido entero y el plato sale gigante, porque el
      // shader usa la relacion de aspecto del buffer para armar el rayo.
      var marco = escenario.querySelector('.pase-marco') || escenario;
      marco.insertBefore(canvas, marco.firstChild);
      medir();
      corriendo = true;
      requestAnimationFrame(pintar);
      window.addEventListener('resize', medir, { passive: true });

      // Cuando el hero no esta a la vista no se pinta: un canvas a pantalla
      // completa girando fuera de pantalla es bateria regalada.
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entradas) {
          var visible = entradas[0].isIntersecting;
          if (visible && !corriendo) { corriendo = true; requestAnimationFrame(pintar); }
          if (!visible) corriendo = false;
        }, { threshold: 0 }).observe(escenario);
      }
    }
  }

  /* ---------------------------------------------------------------------
     Revelados: la pagina se arma a medida que se lee
     --------------------------------------------------------------------- */

  /**
   * Por posicion y no con un IntersectionObserver.
   *
   * El observador avisa de lo que ESTA cruzando el borde. Si el scroll salta por encima de
   * un elemento (el navegador restaurando la posicion al recargar, un enlace con ancla, la
   * rueda a fondo, o el "ir al final" del teclado), ese elemento pasa de estar abajo a
   * estar arriba sin cruzar nada, y se queda en opacidad cero para siempre.
   *
   * No es teorico: el barrido de las ocho paginas encontro OCHO bloques invisibles en
   * escritorio, cuatro en telefono y dos con el zoom al cuatrocientos por ciento, en esta
   * misma pagina. Ya habia pasado igual en real estate, donde se comio la seccion con la
   * unica prueba dura del proyecto.
   *
   * Una comprobacion por posicion no se saltea nada: se pregunta donde esta cada uno, no
   * si acaba de cruzar.
   */
  function montarRevelados() {
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
      var linea = window.innerHeight * 0.88;
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

  /* ---------------------------------------------------------------------
     El reloj del servicio: la franja activa se marca sola
     --------------------------------------------------------------------- */

  function montarReloj() {
    var reloj = document.querySelector('[data-reloj]');
    if (!reloj) return;
    var franjas = reloj.querySelectorAll('[data-franja]');
    if (!franjas.length || !('IntersectionObserver' in window)) return;

    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        var id = e.target.getAttribute('data-franja-ancla');
        [].forEach.call(franjas, function (f) {
          f.classList.toggle('activa', f.getAttribute('data-franja') === id);
        });
      });
    }, { rootMargin: '-45% 0px -45% 0px' });

    [].forEach.call(document.querySelectorAll('[data-franja-ancla]'), function (el) {
      obs.observe(el);
    });
  }

  /* ---------------------------------------------------------------------
     La enredadera: cada planta crece cuando le toca
     --------------------------------------------------------------------- */

  function montarEnredadera() {
    var planta = document.querySelector('.enredadera');
    if (!planta) return;

    var plantas = [].slice.call(planta.querySelectorAll('.planta'));
    if (!plantas.length) return;

    if (quieto.matches || !('IntersectionObserver' in window)) {
      plantas.forEach(function (el) { el.classList.add('visible'); });
      return;
    }

    // Se usa un observador y no el scroll: cada planta crece cuando entra en pantalla y
    // se queda crecida. Antes esto recalculaba el avance del bloque entero en cada
    // cuadro para dibujar un tallo que ya no existe; ahora el navegador avisa y el
    // codigo no corre mientras no pasa nada.
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -14% 0px' });

    plantas.forEach(function (el) { obs.observe(el); });
  }

  /* ---------------------------------------------------------------------
     El Tio: cuatro respuestas, una a la vez
     --------------------------------------------------------------------- */

  function montarTio() {
    var tio = document.querySelector('[data-tio]');
    if (!tio) return;

    // El widget viene oculto del servidor y lo revela el script. Sin JavaScript no
    // aparece un boton que no hace nada, y no falta nada: las cuatro preguntas siguen
    // enteras en la prep list, que es de donde salen.
    tio.hidden = false;

    var abrir = tio.querySelector('[data-tio-abrir]');
    var panel = tio.querySelector('.tio-panel');
    var cerrar = tio.querySelector('[data-tio-cerrar]');
    if (!abrir || !panel) return;

    function mostrar(si) {
      panel.hidden = !si;
      abrir.setAttribute('aria-expanded', si ? 'true' : 'false');
      if (si) {
        var primera = panel.querySelector('.tio-lista button');
        if (primera) primera.focus();
      }
    }

    abrir.addEventListener('click', function () { mostrar(panel.hidden); });
    if (cerrar) {
      cerrar.addEventListener('click', function () {
        mostrar(false);
        abrir.focus();
      });
    }

    // Escape cierra y devuelve el foco al boton: si el panel se abre con teclado,
    // tiene que poder cerrarse con teclado sin salir a buscar la cruz.
    tio.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || panel.hidden) return;
      mostrar(false);
      abrir.focus();
    });

    [].forEach.call(panel.querySelectorAll('[data-pregunta]'), function (boton) {
      var id = boton.getAttribute('data-pregunta');
      var respuesta = panel.querySelector('#tio-r' + id);
      if (!respuesta) return;
      boton.setAttribute('aria-expanded', 'false');
      boton.setAttribute('aria-controls', 'tio-r' + id);
      boton.addEventListener('click', function () {
        var abierta = !respuesta.hidden;
        // Una sola respuesta a la vez: el panel es chico y dos abiertas obligan a
        // scrollear adentro de una caja que ya esta flotando sobre la pagina.
        [].forEach.call(panel.querySelectorAll('.tio-respuesta'), function (r) { r.hidden = true; });
        [].forEach.call(panel.querySelectorAll('[data-pregunta]'), function (b) {
          b.setAttribute('aria-expanded', 'false');
        });
        respuesta.hidden = abierta;
        boton.setAttribute('aria-expanded', abierta ? 'false' : 'true');
      });
    });
  }

  function arranque() {
    montarPase();
    montarEnredadera();
    montarTio();
    montarRevelados();
    montarReloj();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arranque);
  } else {
    arranque();
  }
})();
