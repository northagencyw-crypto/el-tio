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
    'uniform vec2 relacionA;',   // relacion de aspecto de cada toma, para recortar
    'uniform vec2 relacionB;',   // sin deformar
    'uniform float escalaA;',    // cuanto se acerco la toma de adelante (1 -> K)
    'uniform float escalaB;',    // cuanto se acerco la de atras       (1/K -> 1)
    'uniform float salida;',     // cuanto se desvanecio la de adelante
    'uniform float borron;',     // desenfoque radial, atado a la velocidad de scroll
    'uniform vec2 centroA;',   // hacia donde empuja la camara, en la toma de adelante
    'uniform vec2 anclaB;',    // donde en la pantalla nace la toma de atras
    'uniform vec2 derivaA;',
    'uniform vec2 derivaB;',
    'uniform sampler2D ambienteA;',
    'uniform sampler2D ambienteB;',
    '',
    // Recorte tipo `object-fit: cover`, hecho en el shader. Sin esto la foto se estira
    // al ancho del canvas y en arquitectura una vertical torcida se ve enseguida.
    //
    // `ancla` es el punto de la PANTALLA desde el que se abre la toma, y `centro` el
    // punto de la IMAGEN hacia el que se cierra. Para la toma de adelante el ancla es el
    // centro de la pantalla y el centro corre hacia el punto de fuga; para la de atras es
    // al reves. Sin esto la camara empuja siempre al centro geometrico, y cuando el
    // sujeto de la toma siguiente no cayo exactamente ahi, el empalme se nota.
    'vec2 cubrir(vec2 c, vec2 rel, float escala, vec2 ancla, vec2 centro, vec2 deriva){',
    '  vec2 escalaLienzo = vec2(tamano.x / tamano.y, 1.0);',
    '  vec2 escalaImagen = vec2(rel.x / rel.y, 1.0);',
    '  float f = max(escalaLienzo.x / escalaImagen.x, escalaLienzo.y / escalaImagen.y);',
    '  vec2 tam = escalaImagen * f;',
    '  vec2 p = (c - ancla) * escalaLienzo / tam;',
    '  return p / escala + centro + deriva;',
    '}',
    '',
    // Desenfoque radial: cuatro muestras a lo largo del rayo que sale del centro, con
    // la separacion atada a la velocidad. Es lo unico que distingue un empuje de camara
    // de un zoom de visor: cuando una camara avanza rapido, lo que esta cerca del borde
    // se estira hacia afuera y el centro se queda quieto.
    'vec3 rayo(sampler2D t, vec2 rel, float escala, vec2 ancla, vec2 centro, vec2 deriva){',
    '  vec3 s = vec3(0.0);',
    '  for (int k = 0; k < 6; k++){',
    '    float w = (float(k) / 5.0 - 0.5) * borron;',
    '    vec2 c = (uv - ancla) * (1.0 + w) + ancla;',
    '    s += texture2D(t, cubrir(c, rel, escala, ancla, centro, deriva)).rgb;',
    '  }',
    '  return s * 0.16666667;',
    '}',
    '',
    'void main(){',
    // Con la camara quieta el barrido vale cero, y el bucle de seis muestras termina
    // leyendo doce veces el mismo texel por pixel. La rama depende de un uniform, asi que
    // todos los pixeles toman el mismo camino y no cuesta nada decidirla: es el caso de
    // siempre, porque el hero esta visible mucho mas tiempo del que se lo scrollea.
    '  vec3 a; vec3 b;',
    '  if (borron < 0.002) {',
    '    a = texture2D(ambienteA, cubrir(uv, relacionA, escalaA, vec2(0.5), centroA, derivaA)).rgb;',
    '    b = texture2D(ambienteB, cubrir(uv, relacionB, escalaB, anclaB, vec2(0.5), derivaB)).rgb;',
    '  } else {',
    '    a = rayo(ambienteA, relacionA, escalaA, vec2(0.5), centroA, derivaA);',
    '    b = rayo(ambienteB, relacionB, escalaB, anclaB, vec2(0.5), derivaB);',
    '  }',
    // La de adelante se abre y se va; la de atras venia creciendo desde el centro y
    // queda. Las dos escalas son la misma exponencial corrida un tramo, asi que en el
    // momento del cruce la de atras esta exactamente donde estaba la de adelante al
    // empezar: por eso el cambio de toma no se ve.
    '  vec3 color = mix(a, b, salida);',
    '',
    // Vinieta fria y muy contenida. La pagina es un legajo tecnico: la foto se apoya en
    // el borde, no se dramatiza.
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

  // El vuelo del hero: de la orbita a la villa sin un solo corte.
  //
  // No es un cruce de fotos con un zoom encima, que es lo que habia antes y se leia
  // como ocho postales encadenadas. Es un empuje continuo: cada toma esta compuesta
  // para que el sujeto de la siguiente quede chico y centrado, y las dos escalas del
  // shader son la misma exponencial corrida un tramo. Cuando la toma de adelante llego
  // a K, la de atras llego a 1 y esta encuadrada exactamente donde arranco la anterior.
  // De ahi que el pasaje no se vea: geometricamente, no hay pasaje.
  function montarRecorrido() {
    var escenario = document.querySelector('[data-recorrido]');
    if (!escenario) return;

    var marco = escenario.querySelector('.recorrido-marco');
    if (!marco) return;

    var laminas = [].slice.call(escenario.querySelectorAll('[data-ambiente]'));
    if (laminas.length < 2) return;

    var canvas = document.createElement('canvas');
    canvas.className = 'recorrido-canvas';
    // El canvas NO es decorativo: es el hero entero.
    //
    // Estaba con aria-hidden, y cuando el vuelo arranca la tira de respaldo se oculta con
    // display:none. Medido, el hero quedaba exponiendo cero textos alternativos: un lector
    // de pantalla se llevaba el titulo, la bajada y el boton, y nada del recorrido, que es
    // la pieza central de la pagina. Una descripcion buena vale mas que las ocho de las
    // fotos sueltas, porque lo que hay que contar es el descenso, no cada toma.
    canvas.setAttribute('role', 'img');
    canvas.setAttribute(
      'aria-label',
      'Recorrido continuo desde la órbita hasta una villa en Tulum: la Tierra con la ' +
      'península de Yucatán, la costa, la selva, el techo de la villa con su pileta, el ' +
      'acceso, el living de doble altura y la terraza sobre el Caribe al atardecer.'
    );

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

    // Desde aca el modulo se hace cargo del hero, aunque las fotografias todavia no esten.
    //
    // La tira de respaldo es el plan para cuando no hay JavaScript o no hay WebGL, y se
    // ocultaba recien al montar el canvas, o sea recien cuando las dos primeras texturas
    // habian cargado. Si las imagenes no llegan, ese momento no existe nunca: la tira se
    // quedaba visible con sus ocho figuras de alto cero y la capa del hero encima, y los
    // pies de foto salian pisando la bajada y la ficha. Medido con las imagenes
    // bloqueadas: tres textos encimados en escritorio y dos en telefono.
    //
    // Si el programa compilo, hay WebGL y el modulo va a dibujar. Con las fotografias o
    // sin ellas, el hero queda como texto sobre el fondo verde, que se lee.
    escenario.classList.add('recorrido-vivo');

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'posicion');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    var u = {};
    ['tamano', 'relacionA', 'relacionB', 'escalaA', 'escalaB', 'salida', 'borron',
     'centroA', 'anclaB', 'derivaA', 'derivaB', 'ambienteA', 'ambienteB']
      .forEach(function (n) { u[n] = gl.getUniformLocation(prog, n); });

    var texturas = [];
    var pedidas = [];
    var relaciones = [];
    var corriendo = false;
    var arrancado = false;
    var pintado = false;

    // Cuanto se acerca la camara a lo largo de un tramo. Es la razon de la progresion
    // geometrica del vuelo: el plano de atras arranca en 1/K y termina en 1, el de
    // adelante arranca en 1 y termina en K, y en el empalme los dos valen lo mismo. De
    // ahi que no haya corte visible entre toma y toma.
    var K = 2.4;

    // Una deriva lateral chica y propia de cada toma, para que el empuje no sea un zoom
    // perfectamente centrado, que se lee mecanico. Va multiplicada por (escala - 1), asi
    // que vale cero justo en el empalme y no rompe el encastre.
    function deriva(i) {
      return [Math.sin(i * 12.9898) * 0.030, Math.cos(i * 78.233) * 0.024];
    }

    var focos = laminas.map(function (el) {
      var f = (el.getAttribute('data-foco') || '').split(',');
      var x = parseFloat(f[0]), y = parseFloat(f[1]);
      return [isFinite(x) ? x : 0.5, isFinite(y) ? y : 0.5];
    });

    // La variante que le toca a esta pantalla, elegida con la misma regla que usa el
    // navegador para un `sizes` de 100vw. Asi la etiqueta del respaldo y el shader piden
    // la misma URL y la foto se descarga una sola vez.
    function url(el) {
      var base = el.getAttribute('data-ambiente');
      if (!base) return el.getAttribute('src');
      // Si ya viene entera, se usa tal cual.
      //
      // Esta funcion daba por hecho que el atributo es SIEMPRE una ruta sin extension a la
      // que hay que pegarle la variante. El empaquetado para un archivo suelto incrusta la
      // foto como data URI, y ahi el resultado era
      // `data:image/webp;base64,UklGR...-1200.webp`: ocho ERR_INVALID_URL, ninguna textura,
      // el canvas nunca se agregaba al documento y el hero quedaba en verde plano y quieto.
      // La pagina servida estaba bien, asi que mirarla ahi no lo mostraba nunca.
      if (base.indexOf('data:') === 0 || /\.(webp|avif|jpe?g|png)$/i.test(base)) return base;
      var lista = (el.getAttribute('data-anchos') || '').split(',').filter(Boolean);
      if (!lista.length) return base + '.webp';
      var objetivo = window.innerWidth * (window.devicePixelRatio || 1);
      for (var i = 0; i < lista.length; i++) {
        if (+lista[i] >= objetivo) {
          return base + (i === lista.length - 1 ? '' : '-' + lista[i]) + '.webp';
        }
      }
      return base + '.webp';
    }

    // Las dos primeras de una y el resto en fila india.
    //
    // Antes salian las ocho a la vez: dos mil cuatrocientos kilobytes antes de que la
    // pagina estuviera usable, medido, y en el telefono eso es la diferencia entre entrar
    // y cerrar. En fila, la primera pantalla pide lo que necesita para empezar a volar y
    // el resto va llegando mientras se lee, que es mucho antes de que se lo mire.
    function cargar(i, luego) {
      if (i >= laminas.length) return;
      var img = new Image();
      img.onload = function () {
        texturas[i] = textura(gl, img);
        relaciones[i] = [img.naturalWidth, img.naturalHeight];
        if (!arrancado && texturas[0] && texturas[1]) arrancar();
        if (luego) luego();
      };
      img.onerror = function () { if (luego) luego(); };
      img.src = url(laminas[i]);
    }

    // La fila se adelanta a la lectura. Se pide siempre la primera que falte a partir de
    // donde esta el scroll, no la siguiente en orden: quien baja rapido necesita la seis
    // antes que la tres, y pedirlas en orden fijo lo deja mirando un cuadro quieto.
    var pidiendo = false;
    function enFila() {
      pidiendo = false;
      var tramos = Math.max(1, laminas.length - 1);
      var caja = escenario.getBoundingClientRect();
      var total = Math.max(1, escenario.offsetHeight - window.innerHeight);
      var p = Math.min(1, Math.max(0, -caja.top / total));
      var desde = Math.floor(p * tramos);
      for (var d = 0; d < laminas.length; d++) {
        // Primero hacia adelante desde donde se esta leyendo, despues lo que quedo atras.
        var i = (desde + d) % laminas.length;
        if (!texturas[i] && !pedidas[i]) {
          pedidas[i] = true;
          pidiendo = true;
          cargar(i, enFila);
          return;
        }
      }
    }
    pedidas[0] = true;
    pedidas[1] = true;
    cargar(0, enFila);
    cargar(1, enFila);

    // Escalones de resolucion. Se arranca en 1.5 y no en 2 porque el barrido radial son
    // doce lecturas de textura por pixel (medido: cuesta 2,25 veces lo que cuesta sin
    // barrido) y a 2x en una pantalla grande eso es el doble del trabajo que hace falta
    // para una fotografia en movimiento, donde la nitidez extrema no se ve. Si aun asi
    // el equipo no llega, se baja solo: mas vale un vuelo fluido y algo mas blando que
    // uno nitido a tirones, que es exactamente lo contrario de lo que la pieza promete.
    var ESCALONES = [1.5, 1.15, 0.9];
    var escalon = 0;
    var muestras = [];

    function medir() {
      var caja = canvas.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, ESCALONES[escalon]);
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

    // Las fichas de dato: una por toma, se anotan a medida que se desciende.
    var fichas = escenario.querySelectorAll('[data-ficha]');
    var tramoActual = -1;

    function marcarTramo(i) {
      if (i === tramoActual) return;
      tramoActual = i;
      [].forEach.call(fichas, function (el, j) {
        // Se anotan y se quedan anotadas: al final del recorrido estan las ocho, que es
        // justo lo que la seccion afirma.
        el.classList.toggle('anotada', j <= i);
        el.classList.toggle('activa', j === i);
      });
    }

    // El avance suavizado. La rueda del mouse no entrega un movimiento continuo sino
    // saltos de cien pixeles, y atar la camara directo a esos saltos da un vuelo a
    // tirones. Se persigue el objetivo con un seguimiento exponencial: la camara llega
    // siempre, pero con la demora que tiene una camara de verdad.
    var suave = -1;
    var previo = 0;
    var antes = 0;

    function pintar(ahora) {
      var dt = antes ? Math.min(0.1, (ahora - antes) / 1000) : 0.016;
      antes = ahora;

      var objetivo = progreso();
      if (suave < 0) suave = objetivo;
      // Constante de tiempo de 0.34 s: la camara cubre el 95% de lo que le falta en ese
      // lapso, corra a sesenta cuadros o a diez.
      suave += (objetivo - suave) * (1.0 - Math.pow(0.05, dt / 0.34));

      // La velocidad tambien se normaliza a un cuadro de 60, o el desenfoque dependeria
      // de los cuadros por segundo en vez de la velocidad de lectura.
      var vel = Math.abs(suave - previo) * (0.016 / Math.max(0.004, dt));
      previo = suave;

      // Cada 45 cuadros se mira la mediana. Mediana y no promedio: un solo cuadro largo
      // por una recoleccion de basura no tiene que bajar la resolucion de toda la pieza.
      if (escalon < ESCALONES.length - 1) {
        muestras.push(dt);
        if (muestras.length === 45) {
          muestras.sort(function (x, y) { return x - y; });
          if (muestras[22] > 0.026) { escalon += 1; medir(); }
          muestras = [];
        }
      }

      var tramos = texturas.length - 1;
      if (tramos < 1) { if (corriendo) requestAnimationFrame(pintar); return; }
      var d = suave * tramos;
      var i = Math.min(tramos - 1, Math.floor(d));
      var f = d - i;

      marcarTramo(Math.min(texturas.length - 1, Math.floor(d + 0.5)));

      // Nunca se saltea el cuadro.
      //
      // Antes, si la toma que tocaba todavia no habia llegado, se volvia sin dibujar: el
      // canvas se quedaba con lo ultimo pintado y el vuelo parecia clavado. En una
      // conexion de verdad eso pasa siempre, porque las tomas van llegando mientras se
      // baja; en localhost nunca, y por eso no se veia. Ahora se dibuja con la ultima
      // toma que si esta: el descenso se detiene un momento en un lugar valido en vez de
      // congelarse en un cuadro a medias, y sigue solo en cuanto llega la que falta.
      var tope = -1;
      for (var t = 0; t < texturas.length; t++) if (texturas[t]) tope = t; else break;
      if (tope < 0) {
        if (corriendo) requestAnimationFrame(pintar);
        return;
      }
      var a = Math.min(i, tope);
      var b = Math.min(i + 1, tope);
      if (a !== i) {
        // Se congela la geometria en el empalme de la ultima toma disponible, para que
        // no se vea un zoom sin destino mientras se espera.
        escalaA = 1.0;
        escalaB = 1.0;
        f = 0;
      }

      var escalaA, escalaB;
      escalaA = Math.pow(K, f);
      escalaB = Math.pow(K, f - 1.0);
      // La disolvencia ocupa casi todo el tramo. Con las dos tomas encastradas por
      // escala se pueden cruzar largo sin que se lea como doble exposicion, y cruzarlas
      // largo es lo que borra el limite entre una y la siguiente.
      var s = Math.min(1, Math.max(0, (f - 0.22) / 0.72));
      var da = deriva(a), db = deriva(b);

      // El punto de fuga de la toma de adelante: donde adentro de ella vive el sujeto de
      // la siguiente. Se declara en el HTML porque lo decide la fotografia, no el codigo.
      var foco = focos[a] || [0.5, 0.5];
      // El centro recorre el camino que recorre de verdad una camara que avanza hacia un
      // punto fuera de eje: se corre como la reciproca de la escala, no linealmente.
      var ta = (1.0 - 1.0 / escalaA) / (1.0 - 1.0 / K);
      var tb = (1.0 / escalaB - 1.0) / (K - 1.0);
      gl.uniform2f(u.centroA, 0.5 + (foco[0] - 0.5) * ta, 0.5 + (foco[1] - 0.5) * ta);
      gl.uniform2f(u.anclaB, 0.5 + (foco[0] - 0.5) * tb, 0.5 + (foco[1] - 0.5) * tb);

      gl.uniform1f(u.escalaA, escalaA);
      gl.uniform1f(u.escalaB, escalaB);
      gl.uniform1f(u.salida, s * s * (3.0 - 2.0 * s));
      gl.uniform1f(u.borron, Math.min(0.05, vel * 5.0));
      gl.uniform2f(u.derivaA, da[0] * (escalaA - 1.0), da[1] * (escalaA - 1.0));
      gl.uniform2f(u.derivaB, db[0] * (escalaB - 1.0), db[1] * (escalaB - 1.0));
      gl.uniform2f(u.relacionA, relaciones[a][0], relaciones[a][1]);
      gl.uniform2f(u.relacionB, relaciones[b][0], relaciones[b][1]);

      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, texturas[a]);
      gl.uniform1i(u.ambienteA, 0);
      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, texturas[b]);
      gl.uniform1i(u.ambienteB, 1);

      gl.drawArrays(gl.TRIANGLES, 0, 3);
      // El cartel de espera se retira DESPUES del primer dibujo, no al montar el canvas.
      //
      // Se retiraba al montarlo, y entre montar y pintar hay un hueco: el canvas ya esta
      // adelante y todavia no tiene nada, asi que el hero se ponia en negro. Medido con
      // una conexion de 700 kbps, el hueco duraba cinco segundos y era exactamente lo que
      // el founder vio: "se quedo quieto o en negro".
      if (!pintado) {
        pintado = true;
        escenario.classList.add('recorrido-pintando');
      }
      if (corriendo) requestAnimationFrame(pintar);
    }

    function arrancar() {
      if (arrancado) return;
      arrancado = true;
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
    var piezas = [].slice.call(document.querySelectorAll('[data-revela]'));
    if (!piezas.length) return;
    if (quieto.matches) {
      piezas.forEach(function (el) { el.classList.add('visible'); });
      return;
    }

    // Por posicion y no con un IntersectionObserver.
    //
    // El observador avisa de lo que ESTA cruzando el borde. Si el scroll salta por encima
    // de un elemento (el navegador restaurando la posicion al recargar, un enlace con
    // ancla, la rueda a fondo, o el "ir al final" del teclado), ese elemento pasa de estar
    // abajo a estar arriba sin cruzar nada, y se queda en opacidad cero para siempre.
    //
    // Aca son once bloques, y adentro estan las tres capturas del producto, que son la
    // unica prueba dura que tiene el proyecto. Una comprobacion por posicion no se saltea
    // nada: se pregunta donde esta cada uno, no si acaba de cruzar.
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

  // Los cuatro tiempos: cada edificio se enciende cuando su tiempo entra en lectura.
  //
  // Se usa un observador y no el scroll: lo que decide cual esta vivo es cual renglon de
  // texto esta a la altura de los ojos, y eso un IntersectionObserver lo contesta sin
  // hacer cuentas en cada cuadro.
  function montarPasos() {
    var caja = document.querySelector('[data-pasos]');
    if (!caja) return;
    var celdas = caja.querySelectorAll('[data-paso-txt]');
    if (!celdas.length) return;

    function vivo(n) {
      for (var i = 0; i < celdas.length; i++) celdas[i].classList.toggle('vivo', i <= n);
    }

    if (quieto.matches || !('IntersectionObserver' in window)) {
      vivo(celdas.length - 1);
      return;
    }

    // Tambien por posicion: la banda del observador era el diez por ciento del medio de
    // la ventana, y saltando por encima no la cruza nadie. Vive el ultimo tiempo cuya
    // celda ya paso la mitad de la pantalla.
    var pedido2 = 0;
    function revisarPasos() {
      pedido2 = 0;
      var medio = window.innerHeight * 0.5;
      var n = -1;
      for (var i = 0; i < celdas.length; i++) {
        if (celdas[i].getBoundingClientRect().top < medio) n = i;
      }
      vivo(n);
    }
    function pedirPasos() {
      if (pedido2) return;
      pedido2 = requestAnimationFrame(revisarPasos);
    }
    revisarPasos();
    window.addEventListener('scroll', pedirPasos, { passive: true });
    window.addEventListener('resize', pedirPasos, { passive: true });
    // Si la caja entra entera en pantalla de una, el observador con margen del 45% no
    // dispara nunca y los cuatro quedarian apagados.
    new IntersectionObserver(function (e) {
      if (e[0].intersectionRatio > 0.9) vivo(celdas.length - 1);
    }, { threshold: [0, 0.9, 1] }).observe(caja);
  }

  // ---------------------------------------------------------------- la filigrana
  //
  // El grabado de los margenes se dibuja mientras se baja. Es la capa animada de la
  // pagina y el reemplazo de la ciudad que se encendia.
  //
  // El crecimiento es una mascara que baja, no un stroke-dasharray. El ornamento es un
  // `pattern` repetido, y un patron no tiene un trazo unico que recortar; ademas una
  // mascara cuesta un atributo por cuadro en vez de recalcular longitudes.
  function montarFiligrana() {
    var bandas = [].slice.call(document.querySelectorAll('[data-filigrana]'));
    if (!bandas.length) return;
    var cuerpo = document.querySelector('.cuerpo-plano');
    if (!cuerpo) return;

    var cortinas = bandas.map(function (b) { return b.querySelector('.fg-cortina'); });

    if (quieto.matches) {
      cortinas.forEach(function (c) { if (c) c.style.transform = 'translateY(100%)'; });
      return;
    }

    var pedido = 0;
    function pintar() {
      pedido = 0;
      var caja = cuerpo.getBoundingClientRect();
      // La punta del lapiz va a dos tercios de la ventana, que es donde esta mirando
      // quien baja. En el borde de abajo el grabado siempre estaria terminado antes de
      // que se lo vea.
      var punta = (window.innerHeight * 0.68) - caja.top;
      var p = Math.min(1, Math.max(0, punta / cuerpo.offsetHeight));
      var y = (p * 100).toFixed(2) + '%';
      for (var i = 0; i < cortinas.length; i++) {
        if (cortinas[i]) cortinas[i].style.transform = 'translateY(' + y + ')';
      }
    }
    function pedir() {
      if (pedido) return;
      pedido = requestAnimationFrame(pintar);
    }
    pintar();
    window.addEventListener('scroll', pedir, { passive: true });
    window.addEventListener('resize', pedir, { passive: true });
  }

  function arranque() {
    montarRecorrido();
    montarRevelados();
    montarPasos();
    montarFiligrana();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arranque);
  } else {
    arranque();
  }
})();
