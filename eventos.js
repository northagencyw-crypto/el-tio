/**
 * EL TIO EVENTOS
 *
 * Cuatro piezas, y ninguna es decoracion:
 *
 *   1. El vuelo de sala. Un empuje de camara continuo desde la ciudad de noche hasta la
 *      cabina, sin un solo corte, dibujado en WebGL sobre nueve laminas.
 *   2. La lectura de aforo, encima del vuelo. La sala se llena mientras se vuela hacia
 *      adentro, y cruza el punto de equilibrio a las 620 entradas.
 *   3. El fader del riesgo. La misma aritmetica que la calculadora publica: costo fijo mas
 *      cachet, dividido por lo que deja cada entrada. No estima nada.
 *   4. Las entradas de bloque, por posicion y no con un IntersectionObserver.
 *
 * Sin JavaScript la pagina se lee entera: el hero deja su cuenta escrita en un noscript,
 * la tira de laminas queda como galeria, y los bloques con `data-revela` quedan visibles
 * porque la regla de opacidad cuelga de `html.js`, que se agrega en el head.
 *
 * SOBRE LA COPIA DEL MOTOR. El empuje de camara es el mismo que vuela real-estate, y esta
 * copiado a proposito en vez de extraido a un modulo compartido. Dos razones: real-estate
 * es una pagina aprobada y en produccion, y refactorizarla para que eventos ande es poner
 * en riesgo lo que ya funciona por una ganancia de higiene; y el shader ACA DIVERGE, porque
 * este vuelo necesita el apagon de rig que el otro no tiene. Si algun dia hay un tercer
 * vuelo, ahi si conviene extraerlo, con las tres versiones a la vista.
 */
(function () {
  'use strict';

  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');

  // ------------------------------------------------------------------------ el vuelo
  //
  // No es un cruce de fotos con un zoom encima, que se lee como nueve postales
  // encadenadas. Es un empuje continuo: cada toma esta compuesta para que el sujeto de la
  // siguiente quede chico y centrado, y las dos escalas del shader son la misma
  // exponencial corrida un tramo. Cuando la toma de adelante llego a K, la de atras llego
  // a 1 y esta encuadrada exactamente donde arranco la anterior. De ahi que el pasaje no
  // se vea: geometricamente, no hay pasaje.

  var VERTEX = [
    'attribute vec2 posicion;',
    'varying vec2 uv;',
    'void main(){ uv = posicion * 0.5 + 0.5; gl_Position = vec4(posicion, 0.0, 1.0); }',
  ].join('\n');

  var FRAGMENT = [
    'precision highp float;',
    'varying vec2 uv;',
    'uniform vec2 tamano;',
    'uniform vec2 relacionA;',
    'uniform vec2 relacionB;',
    'uniform float escalaA;',
    'uniform float escalaB;',
    'uniform float salida;',
    'uniform float borron;',
    'uniform float apagon;',   // el corte de rig, 1 = luz, 0 = negro
    'uniform vec2 centroA;',
    'uniform vec2 anclaB;',
    'uniform vec2 derivaA;',
    'uniform vec2 derivaB;',
    'uniform sampler2D ambienteA;',
    'uniform sampler2D ambienteB;',
    '',
    // Recorte tipo `object-fit: cover`, hecho en el shader. `ancla` es el punto de la
    // PANTALLA desde el que se abre la toma, y `centro` el punto de la IMAGEN hacia el que
    // se cierra. Sin esto la camara empuja siempre al centro geometrico, y cuando el
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
    // Desenfoque radial atado a la velocidad. Es lo unico que distingue un empuje de
    // camara de un zoom de visor: cuando una camara avanza rapido, lo que esta cerca del
    // borde se estira hacia afuera y el centro se queda quieto.
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
    // Con la camara quieta el barrido vale cero y el bucle termina leyendo doce veces el
    // mismo texel por pixel. La rama depende de un uniform, asi que todos los pixeles
    // toman el mismo camino: es el caso de siempre, porque el hero esta visible mucho mas
    // tiempo del que se lo scrollea.
    '  vec3 a; vec3 b;',
    '  if (borron < 0.002) {',
    '    a = texture2D(ambienteA, cubrir(uv, relacionA, escalaA, vec2(0.5), centroA, derivaA)).rgb;',
    '    b = texture2D(ambienteB, cubrir(uv, relacionB, escalaB, anclaB, vec2(0.5), derivaB)).rgb;',
    '  } else {',
    '    a = rayo(ambienteA, relacionA, escalaA, vec2(0.5), centroA, derivaA);',
    '    b = rayo(ambienteB, relacionB, escalaB, anclaB, vec2(0.5), derivaB);',
    '  }',
    '  vec3 color = mix(a, b, salida);',
    '',
    // Vinieta profunda. Una sala no esta iluminada en los bordes: lo unico que se ve en el
    // perimetro es lo que devuelve el rig. Es mucho mas cerrada que la de real-estate, que
    // es un legajo tecnico y se apoya en el borde en vez de dramatizarlo.
    '  vec2 d = (uv - 0.5) * vec2(tamano.x / tamano.y, 1.0);',
    // Los dos numeros de abajo estaban en 0.62/0.38 y la curva en 0.18, y con eso la
    // fotografia se apagaba DOS VECES: la lamina ya venia oscura del generador y encima el
    // shader la cerraba. Medido mirando la primera tanda: la composicion era exacta y la
    // imagen era casi negra. La correccion va en los dos lados, el brief y el shader, y
    // aca queda contenida a un realce de borde en vez de un tuneleo.
    '  float vin = smoothstep(1.05, 0.25, length(d));',
    '  color *= 0.78 + 0.22 * vin;',
    '',
    // Curva en S contenida, para que los negros caigan hacia el carbon de la hoja en vez
    // de quedar en un gris de fotografia. Es lo que hace que la foto pertenezca a la
    // pagina y no parezca pegada encima.
    '  color = mix(color, color * color * (3.0 - 2.0 * color), 0.10);',
    '  color.b += (1.0 - color.b) * 0.05;',
    '  color.r -= color.r * 0.03;',
    '',
    // El apagon de rig. Multiplica, no mezcla: un corte de luz apaga la fuente, no le pone
    // una capa negra encima, y la diferencia se ve en los brillos especulares.
    '  color *= apagon;',
    '',
    '  gl_FragColor = vec4(color, 1.0);',
    '}',
  ].join('\n');

  function compilar(gl, tipo, fuente) {
    var s = gl.createShader(tipo);
    gl.shaderSource(s, fuente);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.warn('eventos: shader', gl.getShaderInfoLog(s));
      return null;
    }
    return s;
  }

  function textura(gl, imagen) {
    var t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    // WebGL tiene el origen de la textura abajo a la izquierda y una imagen lo tiene
    // arriba a la izquierda: sin esto la foto se sube al canvas dada vuelta.
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, imagen);
    return t;
  }

  function montarVuelo() {
    var escenario = document.querySelector('[data-vuelo]');
    if (!escenario) return null;

    var marco = escenario.querySelector('.vuelo-marco');
    if (!marco) return null;

    var laminas = [].slice.call(escenario.querySelectorAll('[data-ambiente]'));
    if (laminas.length < 2) return null;

    var canvas = document.createElement('canvas');
    canvas.className = 'vuelo-canvas';
    // El canvas NO es decorativo: es el hero entero. Cuando el vuelo arranca, la tira de
    // respaldo se oculta, asi que sin esto un lector de pantalla se lleva el titulo y el
    // boton y nada del recorrido, que es la pieza central de la pagina.
    canvas.setAttribute('role', 'img');
    canvas.setAttribute(
      'aria-label',
      'Vuelo continuo desde el aire sobre la ciudad de noche hasta la cabina: el techo ' +
      'del galpón iluminado, el patio de carga, la puerta con la cola, el pasillo de ' +
      'servicio, la sala desde el fondo, las manos levantadas bajo el rig, el foso frente ' +
      'a la cabina y, al final, la sala entera vista desde detrás del disc jockey.'
    );

    var gl = canvas.getContext('webgl', { antialias: true, alpha: false })
      || canvas.getContext('experimental-webgl', { antialias: true, alpha: false });
    if (!gl) return null;

    var vs = compilar(gl, gl.VERTEX_SHADER, VERTEX);
    var fs = compilar(gl, gl.FRAGMENT_SHADER, FRAGMENT);
    if (!vs || !fs) return null;

    var prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return null;
    gl.useProgram(prog);

    // Desde aca el modulo se hace cargo del hero, aunque las fotografias todavia no esten.
    // Si el programa compilo hay WebGL y el modulo va a dibujar; con las fotos o sin
    // ellas, el hero queda como texto sobre el carbon, que se lee.
    escenario.classList.add('vuelo-vivo');

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'posicion');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    var u = {};
    ['tamano', 'relacionA', 'relacionB', 'escalaA', 'escalaB', 'salida', 'borron', 'apagon',
     'centroA', 'anclaB', 'derivaA', 'derivaB', 'ambienteA', 'ambienteB']
      .forEach(function (n) { u[n] = gl.getUniformLocation(prog, n); });

    var texturas = [];
    var pedidas = [];
    var relaciones = [];
    var corriendo = false;
    var arrancado = false;
    var pintado = false;

    // Cuanto se acerca la camara a lo largo de un tramo. Real-estate usa 2.4 porque va de
    // la orbita a una casa, que son cuatrocientos cincuenta y ocho aumentos en siete
    // tramos. Una sala va de la ciudad a una cabina, que es un rango mucho menor: con 2.4
    // el empuje se siente irreal, como si la camara atravesara paredes.
    var K = 1.8;

    // La deriva lateral, mas alta que en real-estate (0.030/0.024) porque aquello es un
    // dron de relevamiento y esto es una camara en mano entrando a una sala. Va
    // multiplicada por (escala - 1), asi que vale cero justo en el empalme y no rompe el
    // encastre.
    function deriva(i) {
      return [Math.sin(i * 12.9898) * 0.050, Math.cos(i * 78.233) * 0.038];
    }

    // El apagon de rig, y por que existe.
    //
    // Las costuras 01 a 08 son invisibles por geometria: cada toma tiene al sujeto de la
    // siguiente chico y centrado, y el shader las encastra. La ULTIMA no, porque es una
    // orbita: la camara pasa de mirar la cabina de frente a mirar la sala desde detras del
    // hombro del disc jockey, y eso no es un acercamiento sino un giro. Un generador de
    // imagenes encadena por escala y no preserva identidad, asi que entre esas dos tomas
    // la silueta, la consola y el truss derivan, y la deriva se lee como una falla.
    //
    // Se resuelve como se resuelve en una sala de verdad: con un corte de rig. El disc
    // jockey va siempre en contraluz, que es una silueta sin identidad que pueda derivar,
    // y el pasaje se tapa con un apagon breve. No es un truco de transicion importado de
    // otro medio: un apagon de rig pasa todas las noches, y es lo unico que puede pasar
    // ahi sin que el rubro lo note.
    var ULTIMO = laminas.length - 2;   // indice del tramo que hace la orbita
    function apagonDe(i, f) {
      if (i !== ULTIMO) return 1.0;
      var d = (f - 0.5) / 0.09;
      // Piso en 0.05 y no en cero: el scroll lo maneja el usuario, y un negro absoluto
      // sostenido mientras alguien lee despacio es una pantalla muerta, no un apagon.
      return 0.05 + 0.95 * (1.0 - Math.exp(-d * d));
    }

    var focos = laminas.map(function (el) {
      var f = (el.getAttribute('data-foco') || '').split(',');
      var x = parseFloat(f[0]), y = parseFloat(f[1]);
      return [isFinite(x) ? x : 0.5, isFinite(y) ? y : 0.5];
    });

    // La variante que le toca a esta pantalla, con la misma regla que usa el navegador
    // para un `sizes` de 100vw, para que la etiqueta del respaldo y el shader pidan la
    // misma URL y la foto se descargue una sola vez.
    function url(el) {
      var base = el.getAttribute('data-ambiente');
      if (!base) return el.getAttribute('src');
      // Si ya viene entera se usa tal cual. El empaquetado para un archivo suelto incrusta
      // la foto como data URI, y pegarle el sufijo de variante ahi da
      // `data:image/webp;base64,UklGR...-1200.webp`, que no es una URL: ninguna textura,
      // el canvas nunca se agrega y el hero queda plano y quieto. La pagina servida esta
      // bien, asi que mirarla ahi no lo muestra nunca.
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

    // Las dos primeras de una y el resto en fila india. Las nueve juntas son mas de un
    // megabyte antes de que la pagina este usable, y en el telefono eso es la diferencia
    // entre entrar y cerrar.
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

    // La fila se adelanta a la lectura: se pide siempre la primera que falte a partir de
    // donde esta el scroll, no la siguiente en orden. Quien baja rapido necesita la siete
    // antes que la tres, y pedirlas en orden fijo lo deja mirando un cuadro quieto.
    function enFila() {
      var tramos = Math.max(1, laminas.length - 1);
      var caja = escenario.getBoundingClientRect();
      var total = Math.max(1, escenario.offsetHeight - window.innerHeight);
      var p = Math.min(1, Math.max(0, -caja.top / total));
      var desde = Math.floor(p * tramos);
      for (var d = 0; d < laminas.length; d++) {
        var i = (desde + d) % laminas.length;
        if (!texturas[i] && !pedidas[i]) {
          pedidas[i] = true;
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
    // doce lecturas de textura por pixel, y a 2x en una pantalla grande eso es el doble
    // del trabajo que hace falta para una fotografia en movimiento. Si aun asi el equipo
    // no llega, se baja solo: mas vale un vuelo fluido y algo mas blando que uno nitido a
    // tirones, que es lo contrario de lo que la pieza promete.
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

    // Las fichas de tramo: una por toma, se anotan a medida que se entra.
    var fichas = escenario.querySelectorAll('[data-ficha]');
    var tramoActual = -1;

    function marcarTramo(i) {
      if (i === tramoActual) return;
      tramoActual = i;
      [].forEach.call(fichas, function (el, j) {
        el.classList.toggle('anotada', j <= i);
        el.classList.toggle('activa', j === i);
      });
    }

    // A quien avisarle del avance. La lectura de aforo viaja encima del vuelo y tiene que
    // moverse con la MISMA cuenta, no con su propio scroll: si cada uno mide por su lado,
    // en un salto de scroll grande la sala se llena antes o despues de que la camara
    // llegue, y el sentido de la pieza es justamente que las dos cosas son la misma noche.
    var oyentes = [];

    // El avance suavizado. La rueda del mouse no entrega movimiento continuo sino saltos
    // de cien pixeles, y atar la camara directo a esos saltos da un vuelo a tirones. Se
    // persigue el objetivo con un seguimiento exponencial: la camara llega siempre, pero
    // con la demora que tiene una camara de verdad.
    var suave = -1;
    var previo = 0;
    var antes = 0;

    function pintar(ahora) {
      // El dt se acota por arriba: al volver de una pestania en segundo plano el salto es
      // enorme y, sin el tope, la camara se come el vuelo entero en un cuadro.
      var dt = antes ? Math.min(0.05, (ahora - antes) / 1000) : 0.016;
      antes = ahora;

      var objetivo = progreso();
      if (suave < 0) suave = objetivo;
      // Constante de tiempo de 0.34 s: la camara cubre el 95 por ciento de lo que le falta
      // en ese lapso, corra a sesenta cuadros o a ciento veinte. Un factor fijo por cuadro
      // parece lo mismo y no lo es: a 120 Hz llega al 95 por ciento en la mitad de tiempo,
      // o sea que el vuelo va al doble de velocidad segun la pantalla.
      suave += (objetivo - suave) * (1.0 - Math.pow(0.05, dt / 0.34));

      // La velocidad se normaliza a un cuadro de 60, o el desenfoque dependeria de los
      // cuadros por segundo en vez de la velocidad de lectura.
      var vel = Math.abs(suave - previo) * (0.016 / Math.max(0.004, dt));
      previo = suave;

      // Cada 45 cuadros se mira la mediana. Mediana y no promedio: un solo cuadro largo
      // por una recoleccion de basura no tiene que bajarle la resolucion a toda la pieza.
      if (escalon < ESCALONES.length - 1) {
        muestras.push(dt);
        if (muestras.length === 45) {
          muestras.sort(function (x, y) { return x - y; });
          if (muestras[22] > 0.026) { escalon += 1; medir(); }
          muestras = [];
        }
      }

      for (var o = 0; o < oyentes.length; o++) oyentes[o](suave);

      var tramos = texturas.length - 1;
      if (tramos < 1) { if (corriendo) requestAnimationFrame(pintar); return; }
      var d = suave * tramos;
      var i = Math.min(tramos - 1, Math.floor(d));
      var f = d - i;

      marcarTramo(Math.min(texturas.length - 1, Math.floor(d + 0.5)));

      // Nunca se saltea el cuadro. Si la toma que toca todavia no llego, se dibuja con la
      // ultima que si esta: el vuelo se detiene un momento en un lugar valido en vez de
      // congelarse en un cuadro a medias. En una conexion de verdad eso pasa siempre,
      // porque las tomas llegan mientras se baja; en localhost nunca, y por eso no se ve.
      var tope = -1;
      for (var t = 0; t < texturas.length; t++) if (texturas[t]) tope = t; else break;
      if (tope < 0) {
        if (corriendo) requestAnimationFrame(pintar);
        return;
      }
      var a = Math.min(i, tope);
      var b = Math.min(i + 1, tope);
      // Se congela la geometria en el empalme de la ultima toma disponible, para que no se
      // vea un empuje sin destino mientras se espera.
      //
      // El original de real-estate escribe esto ANTES de declarar las dos variables y de
      // calcularlas, asi que las dos asignaciones se pisan dos lineas mas abajo. Ahi queda
      // inerte porque en f=0 la disolvencia vale cero y la lamina de atras no se mezcla,
      // pero es codigo que dice una cosa y hace otra. Aca se calcula una sola vez.
      if (a !== i) f = 0;

      var escalaA = Math.pow(K, f);
      var escalaB = Math.pow(K, f - 1.0);
      // La disolvencia ocupa casi todo el tramo. Con las dos tomas encastradas por escala
      // se pueden cruzar largo sin que se lea como doble exposicion, y cruzarlas largo es
      // lo que borra el limite entre una y la siguiente.
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
      gl.uniform1f(u.apagon, apagonDe(a, f));
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
      // El cartel de espera se retira DESPUES del primer dibujo y no al montar el canvas:
      // entre montar y pintar hay un hueco en el que el canvas ya esta adelante y todavia
      // no tiene nada, y el hero se pone en negro. En una conexion lenta ese hueco dura
      // varios segundos.
      if (!pintado) {
        pintado = true;
        escenario.classList.add('vuelo-pintando');
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

    return {
      alAvanzar: function (fn) { oyentes.push(fn); },
      progreso: progreso,
    };
  }

  // ------------------------------------------------------------------- la lectura
  //
  // La sala se llena mientras la camara entra. Es la union de las dos cosas que la pagina
  // tiene para decir: el espectaculo, que es lo que el rubro vende, y la cuenta, que es lo
  // unico que decide si la fecha gana o pierde. Separadas, la cuenta se lee como una
  // planilla pegada abajo de una foto linda. Encima del vuelo, es la misma noche.
  //
  // Cuelga del avance del vuelo y no de su propio scroll, a proposito: dos mediciones
  // independientes se desincronizan en cualquier salto grande, y ahi la sala termina de
  // llenarse antes de que la camara llegue a la cabina.

  var AFORO = 800;
  var EQUILIBRIO = 620;

  function montarAforo(vuelo) {
    var lectura = document.querySelector('[data-lectura]');
    if (!lectura) return;
    var cifra = lectura.querySelector('[data-vendidas]');
    var estado = lectura.querySelector('[data-estado]');
    var barra = lectura.querySelector('[data-aforo-barra]');
    var ultimo = -1;

    function pintar(p) {
      var vendidas = Math.round(p * AFORO);
      if (vendidas === ultimo) return;
      ultimo = vendidas;
      if (cifra) cifra.textContent = String(vendidas);
      if (barra) barra.style.transform = 'scaleX(' + (vendidas / AFORO).toFixed(4) + ')';
      lectura.classList.toggle('cubierto', vendidas >= EQUILIBRIO);
      if (estado) {
        estado.textContent = vendidas === 0
          ? 'Sala vacía'
          : (vendidas < EQUILIBRIO
            ? 'Faltan ' + (EQUILIBRIO - vendidas) + ' para no perder plata'
            : (vendidas < AFORO
              ? 'Cubierto el costo, ' + (vendidas - EQUILIBRIO) + ' entradas de ganancia'
              : 'Sala llena'));
      }
    }

    // Sin vuelo, sin WebGL o con el movimiento reducido, la lectura queda en el unico
    // estado que se sostiene solo: la sala llena, con la cuenta completa escrita.
    if (!vuelo || quieto.matches) { pintar(1); return; }
    vuelo.alAvanzar(pintar);
  }

  // --------------------------------------------------------------- el texto por partes
  //
  // El titular, la bajada, los botones y la linea de cue no aparecen todos juntos: van
  // entrando a medida que la camara avanza, que es lo que pidio el founder ("que mientras
  // van cambiando las imagenes vaya apareciendo el texto de a partes").
  //
  // La PRIMERA linea del titular no tiene etapa y esta siempre puesta, a proposito: es el
  // elemento LCP de la pagina y esconderla hasta que carguen las texturas seria cambiar una
  // pagina que abre rapido por una que abre en blanco. El boton principal tampoco queda
  // fuera de alcance mientras tanto, porque la pastilla de arriba lo lleva desde el cuadro
  // cero.
  //
  // Se ponen y se QUEDAN puestas. Un texto que se desarma al subir obliga a leer contra el
  // scroll, y nadie hace eso: lee una vez, en un sentido.

  function montarTextoPorPartes(vuelo) {
    var partes = [].slice.call(document.querySelectorAll('[data-etapa]'));
    var cue = document.querySelector('[data-cue]');
    var lineas = cue ? [].slice.call(cue.querySelectorAll('[data-cue-i]')) : [];

    function todoPuesto() {
      partes.forEach(function (el) { el.classList.add('puesto'); });
      // Sin vuelo la cue no puede ir cambiando, asi que se queda la primera, que es la que
      // abre el argumento. Las otras ocho se ocultan.
      lineas.forEach(function (el, i) { el.hidden = i !== 0; });
    }

    if (!vuelo || quieto.matches || (!partes.length && !lineas.length)) { todoPuesto(); return; }

    var umbrales = partes.map(function (el) {
      var n = parseFloat(el.getAttribute('data-etapa'));
      return isFinite(n) ? n : 0;
    });
    var actual = -1;

    vuelo.alAvanzar(function (p) {
      for (var i = 0; i < partes.length; i++) {
        if (p >= umbrales[i]) partes[i].classList.add('puesto');
      }
      if (!lineas.length) return;
      // La cue que corresponde a la toma que se esta mirando. Se redondea igual que el
      // rotulo del riel, para que la linea cambie en el mismo momento en que se enciende
      // la marca de esa toma y no medio tramo despues.
      var i2 = Math.round(p * (lineas.length - 1));
      if (i2 === actual) return;
      actual = i2;
      for (var j = 0; j < lineas.length; j++) lineas[j].hidden = j !== i2;
    });
  }

  // ------------------------------------------------------------------- el fader
  //
  // La misma aritmetica que la herramienta publica, y a proposito: si la pagina dijera un
  // numero y la calculadora otro, la pagina perderia lo unico que tiene para ofrecer, que
  // es que la cuenta se puede verificar.

  function montarConsola() {
    var consola = document.querySelector('[data-consola]');
    if (!consola) return;
    var faders = [].slice.call(consola.querySelectorAll('[data-fader]'));
    if (!faders.length) return;

    var salida = {
      entradas: consola.querySelector('[data-salida-entradas]'),
      pct: consola.querySelector('[data-salida-pct]'),
      juicio: consola.querySelector('[data-salida-juicio]'),
      barra: consola.querySelector('[data-salida-barra]'),
      ocu: consola.querySelector('[data-salida-ocu]'),
      margen: consola.querySelector('[data-salida-margen]'),
      siete: consola.querySelector('[data-salida-siete]'),
    };

    function leer(id) {
      var el = consola.querySelector('[data-fader="' + id + '"]');
      return el ? Number(el.value) : 0;
    }

    function recalcular() {
      var cachet = leer('cachet');
      var fijos = leer('fijos');
      var neto = Math.max(1, leer('neto'));
      var aforo = Math.max(1, leer('aforo'));

      var costo = cachet + fijos;
      var equilibrio = Math.ceil(costo / neto);
      var pct = Math.round((equilibrio / aforo) * 100);

      faders.forEach(function (f) {
        var v = consola.querySelector('[data-val="' + f.getAttribute('data-fader') + '"]');
        if (!v) return;
        var n = Number(f.value);
        v.textContent = f.getAttribute('data-fader') === 'aforo' || f.getAttribute('data-fader') === 'neto'
          ? String(n)
          : n.toLocaleString('es-AR');
      });

      if (salida.entradas) salida.entradas.textContent = String(equilibrio);
      if (salida.pct) salida.pct.textContent = String(pct);
      if (salida.barra) salida.barra.style.width = Math.min(100, pct) + '%';
      if (salida.ocu) salida.ocu.textContent = String(pct);
      if (salida.margen) salida.margen.textContent = String(Math.max(0, aforo - equilibrio));
      if (salida.siete) {
        var siete = Math.round(aforo * 0.7);
        var dif = siete - equilibrio;
        salida.siete.textContent = siete + ' entradas, ' + Math.abs(dif)
          + (dif >= 0 ? ' por encima del umbral' : ' por debajo del umbral');
      }
      if (salida.juicio) {
        salida.juicio.textContent = pct > 100
          ? 'No entra en la sala: con estos números la fecha pierde llena.'
          : (pct >= 80
            ? 'Es riesgo alto: hay que llenar casi la sala solo para empatar.'
            : (pct >= 60
              ? 'Es riesgo medio: queda poco margen para un mal día.'
              : 'Debajo de eso, la fecha pierde plata.'));
      }
    }

    faders.forEach(function (f) {
      f.addEventListener('input', recalcular);
      f.addEventListener('change', recalcular);
    });
    recalcular();
  }

  // ------------------------------------------------------------------ las entradas
  //
  // Por posicion y no con un IntersectionObserver. El observador avisa de lo que ESTA
  // cruzando el borde: si el scroll salta por encima de un bloque (el navegador
  // restaurando la posicion al recargar, un enlace con ancla, la rueda a fondo), ese
  // bloque pasa de estar abajo a estar arriba sin cruzar nada y se queda en opacidad cero
  // para siempre. Ya paso en real estate, y ahi se comio la seccion con la unica prueba
  // dura del proyecto.

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
      var linea = window.innerHeight * 0.9;
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

  function arrancar() {
    var vuelo = quieto.matches ? null : montarVuelo();
    montarAforo(vuelo);
    montarTextoPorPartes(vuelo);
    montarConsola();
    montarEntradas();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }
})();
