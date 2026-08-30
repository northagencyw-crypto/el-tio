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
    // WebGL tiene el origen de la textura abajo a la izquierda y una imagen lo tiene
    // arriba a la izquierda: sin esto la foto se sube al canvas dada vuelta. Se veia en
    // el hero, con los seis ambientes cabeza abajo. Gastronomia lo resolvia invirtiendo
    // la coordenada dentro del shader; aca se hace al subir la textura, que es una linea
    // en vez de una operacion por pixel.
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
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

  // ------------------------------------------------------------------ la mensura
  //
  // La capa de detalle propia de este vertical. En gastronomía lo que crece por el
  // margen es una enredadera porque el rubro es la comida; acá lo que aparece es la
  // acotación de un plano porque el rubro es medir. Esa es la única forma de que dos
  // páginas tengan capa de detalle sin terminar teniendo la misma idea con otro dibujo.
  //
  // Se arma en JavaScript y no en el generador porque cada cota tiene que caer en el
  // borde real de su sección, y esa altura no existe hasta que el navegador maquetó:
  // depende del ancho de la ventana, de si la tipografía llegó a cargar y de cuánto
  // texto entró en cada renglón. Calcularla en Python sería adivinarla.

  function azar(s) {
    // Hash de parte fraccionaria. Un sin() crudo muestreado a paso regular devuelve
    // valores casi iguales cuando el paso por la constante cae cerca de un múltiplo de
    // 2*PI, y el temblor sale alineado en vez de aleatorio. Ya pasó dos veces.
    var x = Math.sin(s * 78.233 + 19.19) * 43758.5453;
    return x - Math.floor(x);
  }

  function pulso(x0, y0, x1, y1, semilla, temblor) {
    // Una recta a mano: seis puntos que se apartan de la ideal, más en el medio que en
    // las puntas, que es como tiembla una mano apoyada en dos extremos. Un <line> de SVG
    // es exacto y por eso se lee impreso y no dibujado.
    var N = 6, d = '', i, t, sep;
    var largo = Math.hypot(x1 - x0, y1 - y0) || 1;
    var nx = -(y1 - y0) / largo, ny = (x1 - x0) / largo;
    for (i = 0; i <= N; i++) {
      t = i / N;
      sep = Math.sin(Math.PI * t) * temblor * (azar(semilla * 7 + i * 3) - 0.5) * 2;
      d += (i ? ' L' : 'M') +
        (x0 + (x1 - x0) * t + nx * sep).toFixed(1) + ' ' +
        (y0 + (y1 - y0) * t + ny * sep).toFixed(1);
    }
    return d;
  }

  function svgEl(nombre, atributos) {
    var el = document.createElementNS('http://www.w3.org/2000/svg', nombre), k;
    for (k in atributos) if (atributos.hasOwnProperty(k)) el.setAttribute(k, atributos[k]);
    return el;
  }

  // Las notas a lápiz son los datos de la propiedad de demostración que aparece en la
  // captura del producto: Torre Vela, piso 12, 2 dormitorios, 2 baños, 84 metros.
  // Inventar otras habría sido gratis y habría dejado dos juegos de números distintos
  // para la misma propiedad en la misma página.
  var NOTAS_LAPIZ = ['84 m2', '2 dorm', 'piso 12'];

  function montarMensura() {
    var cuerpo = document.querySelector('.cuerpo-plano');
    if (!cuerpo) return;

    var capa = document.createElement('div');
    capa.className = 'mensura';
    capa.setAttribute('aria-hidden', 'true');
    cuerpo.appendChild(capa);

    var svg = null, eje = null, ejeClaro = null, niveles = [], largoEje = 0;

    function dibujar() {
      // Debajo de 1100px no hay margen donde dibujar: la cota se montaría encima del
      // texto y dejaría de ser una anotación al costado para ser ruido arriba.
      // El canal se mide contra el contenido de verdad y no contra un contenedor por
      // nombre de clase: buscar '.inner' devolvia null porque esta hoja nunca uso esa
      // clase, y la capa entera se apagaba sin decir nada. Los titulos siempre estan y
      // siempre arrancan en el borde de la caja de texto, asi que el borde izquierdo mas
      // chico de todos ellos es exactamente donde termina el margen disponible.
      var canal = Infinity;
      var titulos = cuerpo.querySelectorAll('h2, h3, .rotulo');
      for (var q = 0; q < titulos.length; q++) {
        var izq = titulos[q].getBoundingClientRect().left;
        if (izq > 0) canal = Math.min(canal, izq);
      }
      canal = isFinite(canal) ? Math.round(canal) : 0;
      while (capa.firstChild) capa.removeChild(capa.firstChild);
      svg = null; niveles = [];
      if (window.innerWidth < 1100 || canal < 56) return;

      var W = canal, H = cuerpo.offsetHeight;
      var x = Math.round(W * 0.52);   // el eje, ni pegado al borde ni contra el texto
      svg = svgEl('svg', { width: W, height: H, viewBox: '0 0 ' + W + ' ' + H, 'class': 'mensura-svg' });

      var secciones = [].slice.call(cuerpo.children).filter(function (s) {
        return s.tagName === 'SECTION' && s.offsetHeight > 120;
      });

      // El eje: una sola línea de punta a punta, que es lo que ordena una lámina. Se
      // dibuja sola al bajar, con stroke-dashoffset, y ese es el equivalente exacto de
      // la enredadera que crece: la página se va midiendo mientras se recorre.
      var trazo = pulso(x, 24, x, H - 24, 3, 2.6);
      eje = svgEl('path', { d: trazo, 'class': 'eje' });
      svg.appendChild(eje);

      // El mismo eje otra vez, en claro, recortado a los tramos de fondo oscuro. Es la
      // forma de que la linea cambie al contraste mas fuerte donde el papel se vuelve
      // grafito sin recurrir a mix-blend-mode, que se apaga en silencio en cuanto
      // cualquier ancestro crea contexto de apilado. Ya se rompio tres veces por eso en
      // la pagina de gastronomia; aca el recorte es explicito y no depende del entorno.
      var oscuros = cuerpo.querySelectorAll('.sangre-noche, .cierre-oscuro');
      if (oscuros.length) {
        var clip = svgEl('clipPath', { id: 'mensura-oscuro' });
        for (var k = 0; k < oscuros.length; k++) {
          clip.appendChild(svgEl('rect', {
            x: 0, y: oscuros[k].offsetTop - cuerpo.offsetTop,
            width: W, height: oscuros[k].offsetHeight }));
        }
        svg.appendChild(clip);
        ejeClaro = svgEl('path', { d: trazo, 'class': 'eje eje--claro',
          'clip-path': 'url(#mensura-oscuro)' });
        svg.appendChild(ejeClaro);
      } else {
        ejeClaro = null;
      }

      var i, s, y, g, nivel, medida, alto;
      for (i = 0; i < secciones.length; i++) {
        s = secciones[i];
        y = s.offsetTop - cuerpo.offsetTop;
        nivel = s.getAttribute('data-lamina') || '';
        medida = s.getAttribute('data-cota') || '';
        g = svgEl('g', { 'class': 'nivel' });
        // La marca de nivel: el tick que sale del eje hacia el contenido, como el que
        // señala una altura en un corte de arquitectura.
        g.appendChild(svgEl('path', { d: pulso(x - 9, y, W - 4, y, i * 5 + 11, 1.1), 'class': 'marca' }));
        g.appendChild(svgEl('circle', { cx: x, cy: y, r: 2.6, 'class': 'nodo' }));
        if (nivel) {
          var t = svgEl('text', { x: x - 8, y: y - 7, 'class': 'num' });
          t.textContent = nivel;
          g.appendChild(t);
        }
        // La cota entre esta marca y la siguiente, con sus topes a 45 grados y el
        // nombre de la lámina escrito de costado sobre la línea.
        if (i < secciones.length - 1) {
          alto = (secciones[i + 1].offsetTop - cuerpo.offsetTop) - y;
          if (alto > 220 && medida) {
            var xc = x - 22;
            g.appendChild(svgEl('path', { d: pulso(xc, y + 16, xc, y + alto - 16, i * 9 + 4, 1.6), 'class': 'cota' }));
            g.appendChild(svgEl('path', { d: 'M' + (xc - 4) + ' ' + (y + 22) + ' L' + (xc + 4) + ' ' + (y + 10), 'class': 'tope' }));
            g.appendChild(svgEl('path', { d: 'M' + (xc - 4) + ' ' + (y + alto - 10) + ' L' + (xc + 4) + ' ' + (y + alto - 22), 'class': 'tope' }));
            var m = svgEl('text', { x: xc - 7, y: y + alto / 2, 'class': 'medida',
              transform: 'rotate(-90 ' + (xc - 7) + ' ' + (y + alto / 2) + ')' });
            m.textContent = medida;
            g.appendChild(m);
          }
          // Cada tanto, una nota a lápiz de la propiedad de demostración.
          if (i % 3 === 1 && alto > 300) {
            var n = svgEl('text', { x: W - 10, y: y + 46, 'class': 'lapiz',
              transform: 'rotate(-4 ' + (W - 10) + ' ' + (y + 46) + ')' });
            n.textContent = NOTAS_LAPIZ[Math.floor((i - 1) / 3) % NOTAS_LAPIZ.length];
            g.appendChild(n);
          }
        }
        g.dataset.y = y;
        if (s.className.indexOf('oscuro') >= 0 || s.className.indexOf('sangre') >= 0) {
          g.setAttribute('class', 'nivel nivel--oscuro');
        }
        svg.appendChild(g);
        niveles.push(g);
      }

      capa.appendChild(svg);
      largoEje = eje.getTotalLength();
      if (quieto.matches) {
        eje.style.strokeDasharray = 'none';
        if (ejeClaro) ejeClaro.style.strokeDasharray = 'none';
        for (i = 0; i < niveles.length; i++) niveles[i].classList.add('visto');
      } else {
        eje.style.strokeDasharray = largoEje;
        eje.style.strokeDashoffset = largoEje;
        if (ejeClaro) {
          ejeClaro.style.strokeDasharray = largoEje;
          ejeClaro.style.strokeDashoffset = largoEje;
        }
        avanzar();
      }
    }

    function avanzar() {
      if (!svg || quieto.matches) return;
      // El trazo llega hasta donde llegó la lectura: se toma el medio de la ventana como
      // punta del lápiz, que es donde está mirando quien baja.
      var caja = cuerpo.getBoundingClientRect();
      var punta = (window.innerHeight * 0.62) - caja.top;
      var p = Math.min(1, Math.max(0, punta / cuerpo.offsetHeight));
      var resto = (largoEje * (1 - p)).toFixed(1);
      eje.style.strokeDashoffset = resto;
      if (ejeClaro) ejeClaro.style.strokeDashoffset = resto;
      for (var i = 0; i < niveles.length; i++) {
        if (punta > +niveles[i].dataset.y) niveles[i].classList.add('visto');
      }
    }

    dibujar();
    var pedido = 0;
    window.addEventListener('scroll', function () {
      if (pedido) return;
      pedido = requestAnimationFrame(function () { pedido = 0; avanzar(); });
    }, { passive: true });
    var redibujo;
    window.addEventListener('resize', function () {
      clearTimeout(redibujo);
      redibujo = setTimeout(dibujar, 180);
    }, { passive: true });
  }

  function arranque() {
    montarRecorrido();
    montarRevelados();
    montarMensura();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arranque);
  } else {
    arranque();
  }
})();
