/* EL TIO - hero scrub, matrix rain, reveals */
(function () {
  'use strict';
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* reveal on scroll */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  /* pillars light up while centered (touch devices have no hover) */
  var pio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { e.target.classList.toggle('lit', e.isIntersecting); });
  }, { threshold: 0.55 });
  document.querySelectorAll('.pillar').forEach(function (el) { pio.observe(el); });

  /* marquee pause: WCAG 2.2.2 needs a control usable without hover */
  var marquee = document.querySelector('.marquee');
  var pauseBtn = document.querySelector('.marquee-pause');
  if (marquee && pauseBtn) {
    pauseBtn.addEventListener('click', function () {
      var paused = marquee.classList.toggle('paused');
      pauseBtn.setAttribute('aria-pressed', String(paused));
      pauseBtn.textContent = paused ? 'Reanudar' : 'Pausar';
    });
  }

  /* Las paginas de rubro comparten este archivo por los reveals y nada mas: no
     tienen hero. Sin este corte, todo lo que sigue busca elementos que ahi no
     existen y la pagina se queda con los bloques invisibles. */
  if (!document.querySelector('.hero')) return;

  if (reduced) {
    /* CSS shows the title statically; the CTAs must be reachable */
    document.querySelector('.hero-title').removeAttribute('inert');
    return;
  }

  /* ---------- hero scrub ---------- */
  var hero = document.getElementById('hero');
  var stage = hero.querySelector('.hero-stage');
  /* f1 stays as the base layer; f2..f5 fade IN on top (f5 is tio-1 again,
     the recomposition). Fading in over a visible frame never dims the stage. */
  var frames = [
    hero.querySelector('.f1'),
    hero.querySelector('.f2'),
    hero.querySelector('.f3'),
    hero.querySelector('.f4'),
    hero.querySelector('.f5')
  ];
  var beats = [
    hero.querySelector('.b0'),
    hero.querySelector('.b1'),
    hero.querySelector('.b2'),
    hero.querySelector('.b3')
  ];
  var title = hero.querySelector('.hero-title');
  var cue = hero.querySelector('.scroll-cue');
  var progressBar = document.getElementById('progress');

  /* if the base portrait is missing, fall back to a dark gradient stage */
  frames.forEach(function (f) {
    f.addEventListener('error', function () { f.style.display = 'none'; });
  });
  frames[0].addEventListener('error', function () {
    stage.style.background = 'radial-gradient(ellipse 80% 60% at 50% 35%, #0D1A28 0%, #04070B 70%)';
  });

  function clamp01(v) { return Math.max(0, Math.min(1, v)); }
  /* fade in over [a,b], fade out over [c,d] */
  function windowFade(p, a, b, c, d) {
    if (p < a || p > d) return 0;
    if (p < b) return (p - a) / (b - a);
    if (p > c) return 1 - (p - c) / (d - c);
    return 1;
  }

  /* fade-in windows for f2..f5 (f1 is always the base layer) */
  var fadeIns = [
    { idx: 1, a: 0.10, b: 0.28 },
    { idx: 2, a: 0.30, b: 0.50 },
    { idx: 3, a: 0.52, b: 0.70 },
    { idx: 4, a: 0.74, b: 0.88 }
  ];
  var beatWindows = [
    [0.000, 0.000, 0.055, 0.105],
    [0.115, 0.155, 0.265, 0.305],
    [0.335, 0.375, 0.485, 0.525],
    [0.545, 0.585, 0.685, 0.725]
  ];

  var rainTargetIntensity = 0;

  function heroFrame(p) {
    var op = [1, 0, 0, 0, 0];
    fadeIns.forEach(function (t) {
      op[t.idx] = clamp01((p - t.a) / (t.b - t.a));
    });
    /* release fully covered layers so the compositor skips them, but only
       when the covering frame has real pixels: on slow networks a lazy frame
       can reach opacity 1 before loading, and hiding the base would leave
       a black stage */
    for (var i = 0; i < op.length - 1; i++) {
      for (var j = i + 1; j < op.length; j++) {
        if (op[j] >= 1 && frames[j].complete && frames[j].naturalWidth > 0) {
          op[i] = 0;
          break;
        }
      }
    }
    var scale = 1.12 - 0.12 * p;
    frames.forEach(function (f, idx) {
      f.style.opacity = op[idx].toFixed(3);
      f.style.transform = 'scale(' + scale.toFixed(4) + ')';
    });

    /* beats: b0 is visible on load and only fades out */
    beats.forEach(function (b, idx) {
      var w = beatWindows[idx];
      var o;
      if (idx === 0) {
        o = p >= w[3] ? 0 : (p > w[2] ? 1 - (p - w[2]) / (w[3] - w[2]) : 1);
      } else {
        o = windowFade(p, w[0], w[1], w[2], w[3]);
      }
      b.style.opacity = o.toFixed(3);
      b.style.transform = 'translateY(' + ((1 - o) * 34).toFixed(1) + 'px)';
    });

    /* final title */
    var to = clamp01((p - 0.87) / 0.08);
    title.style.opacity = to.toFixed(3);
    title.style.transform = 'translateY(' + ((1 - to) * 30).toFixed(1) + 'px)';
    title.classList.toggle('live', to > 0.6);
    title.toggleAttribute('inert', to <= 0.6);

    /* cue */
    cue.style.opacity = (1 - clamp01(p / 0.05)).toFixed(3);

    /* rain intensity follows the digitization arc */
    rainTargetIntensity = windowFade(p, 0.08, 0.30, 0.70, 0.90);
  }

  /* the extra frames only matter once the scrub starts; loading them lazily
     keeps the first paint light and skips them entirely in reduced motion */
  var framesLoaded = false;
  function loadFrames() {
    if (framesLoaded) return;
    framesLoaded = true;
    var small = innerWidth <= 768;
    frames.forEach(function (f) {
      if (!f.getAttribute('src') && f.dataset.src) {
        f.src = small && f.dataset.srcSm ? f.dataset.srcSm : f.dataset.src;
      }
    });
  }
  setTimeout(loadFrames, 3500);

  var ticking = false;
  function onScrollFrame() {
    ticking = false;
    var doc = document.documentElement;
    var total = doc.scrollHeight - innerHeight;
    progressBar.style.transform = 'scaleX(' + clamp01(total > 0 ? scrollY / total : 0) + ')';
    if (scrollY > 0) loadFrames();

    var r = hero.getBoundingClientRect();
    if (r.bottom < -200) { rainTargetIntensity = 0; return; }
    var span = r.height - innerHeight;
    heroFrame(clamp01(span > 0 ? -r.top / span : 0));
    if (rainTargetIntensity > 0 && !rainRunning) {
      rainRunning = true;
      requestAnimationFrame(rainFrame);
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(onScrollFrame); } }
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });

  /* ---------- matrix rain with dollar signs ---------- */
  var canvas = document.getElementById('rain');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(devicePixelRatio || 1, 2);
  var FONT = 13;
  var cols = [];
  var intensity = 0;
  var rainRunning = false;

  function sizeCanvas() {
    var w = stage.clientWidth, h = stage.clientHeight;
    var W = Math.round(w * DPR), H = Math.round(h * DPR);
    /* mobile URL bars fire resize without changing the stage; setting
       canvas.width to the same value would still wipe the bitmap */
    if (canvas.width === W && canvas.height === H) return;
    canvas.width = W;
    canvas.height = H;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.font = FONT + 'px "Geist Mono", monospace';
    ctx.textBaseline = 'top';
    var n = Math.ceil(w / (FONT * 1.3));
    cols = [];
    for (var i = 0; i < n; i++) {
      cols.push({
        x: i * FONT * 1.3,
        y: Math.random() * -h,
        speed: 1.8 + Math.random() * 3.2,
        active: Math.random()
      });
    }
  }
  sizeCanvas();
  addEventListener('resize', sizeCanvas, { passive: true });

  function glyph() {
    return Math.random() < 0.5 ? '0' : '1';
  }

  function rainFrame() {
    intensity += (rainTargetIntensity - intensity) * 0.06;
    var visible = intensity > 0.012;
    canvas.style.opacity = visible ? Math.min(intensity * 1.15, 1).toFixed(3) : '0';
    /* park the loop while the rain is idle; onScrollFrame restarts it */
    if (!visible && rainTargetIntensity === 0) {
      rainRunning = false;
      return;
    }
    if (visible) {
      var w = stage.clientWidth, h = stage.clientHeight;
      /* trail: erase toward transparency so the portrait behind stays visible */
      ctx.globalCompositeOperation = 'destination-out';
      ctx.fillStyle = 'rgba(0,0,0,0.18)';
      ctx.fillRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'source-over';
      for (var i = 0; i < cols.length; i++) {
        var c = cols[i];
        if (c.active > intensity) continue;
        var g = glyph();
        if (Math.random() < 0.045) {
          /* occasional brighter leader glyph, soft ice tone */
          ctx.fillStyle = 'rgba(214,236,250,0.85)';
          ctx.shadowColor = 'rgba(127,201,242,0.8)';
          ctx.shadowBlur = 8;
        } else {
          ctx.fillStyle = 'rgba(127,201,242,' + (0.2 + Math.random() * 0.32).toFixed(2) + ')';
          ctx.shadowBlur = 0;
        }
        ctx.fillText(g, c.x, c.y);
        ctx.shadowBlur = 0;
        c.y += c.speed;
        if (c.y > h + 40) {
          c.y = -30 - Math.random() * h * 0.4;
          c.speed = 2.2 + Math.random() * 4.2;
          c.active = Math.random();
        }
      }
    }
    requestAnimationFrame(rainFrame);
  }

  onScrollFrame();
})();
