/* ===========================================================================
   EL TIO REAL ESTATE - el recorrido

   La pagina abre caminando la propiedad. Fachada, hall, living, cocina,
   dormitorio, terraza: seis tramos encadenados en un solo bloque pinneado, y la
   camara avanza hacia adelante mientras se pasa de uno al otro.

   Por que ese recorrido y no otro: el producto de este vertical promete que la
   propiedad se carga UNA vez y queda lista. Entonces el recorrido no es un paseo
   decorativo, es la carga misma. En cada ambiente se anota el dato que ese
   ambiente aporta, y al final del bloque estan los seis anotados. Lo que el
   visitante acaba de hacer con el scroll es exactamente lo que el software hace
   con la propiedad.

   NO SE PARECE AL DE GASTRONOMIA A PROPOSITO. Alla hay un objeto calido que gira
   sobre su eje; aca hay un espacio frio por el que se avanza. Comparten que los
   dos son WebGL propio y que los dos degradan a fotografia: nada mas. Si dos
   verticales comparten el mismo efecto vuelven a leerse como la misma pagina, que
   es el problema que todo este trabajo vino a corregir.

   DEGRADACION. Sin WebGL, sin JavaScript o con prefers-reduced-motion, el bloque
   es una tira de fotografia de arquitectura con su pie: los seis ambientes, en
   orden, perfectamente legibles. El canvas se agrega desde aca.
   =========================================================================== */

(function () {
  'use strict';

  // Guarda de una sola ejecucion. Este archivo llego a quedar incluido dos veces en el
  // HTML y el resultado fueron dos canvas apilados pintando la misma escena: el doble
  // de trabajo de GPU, invisible a simple vista y detectado solo porque una medicion
  // conto dos. La etiqueta duplicada se arreglo, pero la guarda se queda: un modulo
  // que monta cosas en el DOM no puede depender de que nadie se equivoque al incluirlo.
  if (window.__elTioMontado_recorrido) return;
  window.__elTioMontado_recorrido = true;

  var raiz = document.documentElement;
  raiz.classList.add('js');

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  var VERTEX = [
    'attribute vec2 posicion;',
    'varying vec2 uv;',
    'void main(){ uv = posicion * 0.5 + 0.5; gl_Position = vec4(posicion, 0.0, 1.0); }',
  ].join('\n');

  var FRAGMENT = [
    'precision highp float;',
    'varying vec2 uv;',
    'uniform vec2 tamano;',
    'uniform vec2 relacionA;',   // relacion de aspecto de cada textura, para
    'uniform vec2 relacionB;',   // recortar sin deformar
    'uniform float avance;',     // 0 a 1 dentro del tramo: la camara empuja
    'uniform float mezcla;',     // cruce entre ambiente A y ambiente B
    'uniform sampler2D ambienteA;',
    'uniform sampler2D ambienteB;',
    '',
    // Recorte tipo `object-fit: cover`, hecho en el shader. Sin esto la foto se
    // estira al ancho del canvas y en arquitectura una vertical torcida se ve
    // enseguida: es justo lo que este rubro no perdona.
    'vec2 cubrir(vec2 c, vec2 rel, float empuje){',
    '  vec2 escalaLienzo = vec2(tamano.x / tamano.y, 1.0);',
    '  vec2 escalaImagen = vec2(rel.x / rel.y, 1.0);',
    '  float f = max(escalaLienzo.x / escalaImagen.x, escalaLienzo.y / escalaImagen.y);',
    '  vec2 tam = escalaImagen * f;',
    '  vec2 p = (c - 0.5) * escalaLienzo / tam;',
    // El empuje es un zoom hacia el centro: es lo que convierte un cruce de fotos
    // en la sensacion de estar caminando hacia adentro.
    '  return p / (1.0 + empuje) + 0.5;',
    '}',
    '',
    'void main(){',
    '  float empujeA = mix(0.0, 0.16, avance);',
    // El ambiente que entra arranca un poco mas cerrado y se abre: los dos se
    // mueven en la misma direccion, asi el corte no frena la marcha.
    '  float empujeB = mix(-0.10, 0.06, avance);',
    '',
    '  vec3 a = texture2D(ambienteA, cubrir(uv, relacionA, empujeA)).rgb;',
    '  vec3 b = texture2D(ambienteB, cubrir(uv, relacionB, empujeB)).rgb;',
    '  vec3 color = mix(a, b, mezcla);',
    '',
    // Vinieta fria y muy contenida. La pagina es un legajo tecnico: la foto se
    // apoya en el borde, no se dramatiza.
    '  vec2 d = (uv - 0.5) * vec2(tamano.x / tamano.y, 1.0);',
    '  float vin = smoothstep(0.95, 0.30, length(d));',
    '  color *= 0.80 + 0.20 * vin;',
    '',
    // Enfriado leve: se levanta apenas el azul en las sombras para que el canvas
    // pertenezca a la misma temperatura que el resto de la hoja.
    '  color.b += (1.0 - color.b) * 0.035;',
    '  color.r -= color.r * 0.012;',
    '',
    '  gl_FragColor = vec4(color, 1.0);',
    '}',
  ].join('\n');

  function compilar(gl, tipo, fuente) {
    var s = gl.createShader(tipo);
    gl.shaderSource(s, fuente);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.warn('real-estate: shader', gl.getShaderInfoLog(s));
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

  function montarRecorrido() {
    var escenario = document.querySelector('[data-recorrido]');
    if (!escenario) return;

    var marco = escenario.querySelector('.recorrido-marco');
    if (!marco) return;

    var laminas = [].slice.call(escenario.querySelectorAll('[data-ambiente]'));
    if (laminas.length < 2) return;

    var canvas = document.createElement('canvas');
    canvas.className = 'recorrido-canvas';
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
    ['tamano', 'relacionA', 'relacionB', 'avance', 'mezcla', 'ambienteA', 'ambienteB']
      .forEach(function (n) { u[n] = gl.getUniformLocation(prog, n); });

    var texturas = [];
    var relaciones = [];
    var listas = 0;
    var corriendo = false;

    laminas.forEach(function (el, i) {
      var img = new Image();
      img.onload = function () {
        texturas[i] = textura(gl, img);
        relaciones[i] = [img.naturalWidth, img.naturalHeight];
        listas += 1;
        if (listas === 2) arrancar();
      };
      img.src = el.getAttribute('data-ambiente');
    });

    function medir() {
      var caja = canvas.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.max(1, Math.round(caja.width * dpr));
      canvas.height = Math.max(1, Math.round(caja.height * dpr));
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.uniform2f(u.tamano, canvas.width, canvas.height);
    }

    function progreso() {
      var caja = escenario.getBoundingClientRect();
      var total = Math.max(1, escenario.offsetHeight - window.innerHeight);
      return Math.min(1, Math.max(0, -caja.top / total));
    }

    // Las fichas de dato: una por ambiente, se anotan a medida que se pasa.
    var fichas = escenario.querySelectorAll('[data-ficha]');
    var tramoActual = -1;

    function marcarTramo(i) {
      if (i === tramoActual) return;
      tramoActual = i;
      [].forEach.call(fichas, function (el, j) {
        // Se anotan y se quedan anotadas: al final del recorrido estan las seis,
        // que es justo lo que la seccion afirma.
        el.classList.toggle('anotada', j <= i);
        el.classList.toggle('activa', j === i);
      });
    }

    function pintar() {
      var p = progreso();
      var tramos = texturas.length - 1;
      var escala = p * tramos;
      var i = Math.min(tramos - 1, Math.floor(escala));
      var f = escala - i;

      marcarTramo(Math.min(texturas.length - 1, Math.round(escala)));

      gl.uniform1f(u.avance, f);
      // El cruce se concentra en el ultimo tramo del recorrido de cada ambiente.
      // Con un smoothstep sobre el segmento entero se pasaba la mitad del tiempo en
      // doble exposicion, y eso no se lee como avanzar: se lee como una foto mal
      // cargada encima de otra. Asi cada ambiente se sostiene y despues se cruza.
      var c = Math.min(1, Math.max(0, (f - 0.58) / 0.42));
      gl.uniform1f(u.mezcla, c * c * (3.0 - 2.0 * c));

      var a = i;
      var b = Math.min(texturas.length - 1, i + 1);
      if (!texturas[a] || !texturas[b]) {
        if (corriendo) requestAnimationFrame(pintar);
        return;
      }
      gl.uniform2f(u.relacionA, relaciones[a][0], relaciones[a][1]);
      gl.uniform2f(u.relacionB, relaciones[b][0], relaciones[b][1]);

      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, texturas[a]);
      gl.uniform1i(u.ambienteA, 0);
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, texturas[b]);
      gl.uniform1i(u.ambienteB, 1);

      gl.drawArrays(gl.TRIANGLES, 0, 3);
      if (corriendo) requestAnimationFrame(pintar);
    }

    function arrancar() {
      escenario.classList.add('recorrido-vivo');
      marco.insertBefore(canvas, marco.firstChild);
      medir();
      marcarTramo(0);
      corriendo = true;
      requestAnimationFrame(pintar);
      window.addEventListener('resize', medir, { passive: true });

      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (e) {
          var visible = e[0].isIntersecting;
          if (visible && !corriendo) { corriendo = true; requestAnimationFrame(pintar); }
          if (!visible) corriendo = false;
        }, { threshold: 0 }).observe(escenario);
      }
    }
  }

  function montarRevelados() {
    var piezas = document.querySelectorAll('[data-revela]');
    if (!piezas.length) return;
    if (quieto.matches || !('IntersectionObserver' in window)) {
      [].forEach.call(piezas, function (el) { el.classList.add('visible'); });
      return;
    }
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    [].forEach.call(piezas, function (el) { obs.observe(el); });
  }

  function arranque() {
    montarRecorrido();
    montarRevelados();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arranque);
  } else {
    arranque();
  }
})();
