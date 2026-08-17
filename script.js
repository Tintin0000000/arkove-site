(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  if (!reduced) {
    var els = document.querySelectorAll('.reveal');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.15 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // animated price counters
  var counters = document.querySelectorAll('.cnt');
  function formatFr(n) { return Math.round(n).toLocaleString('fr-FR'); }
  function animateCounter(el) {
    var to = parseInt(el.getAttribute('data-to'), 10);
    if (reduced) { el.textContent = formatFr(to); return; }
    var duration = 1300, start = null;
    function ease(t) { return 1 - Math.pow(1 - t, 3); }
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      el.textContent = formatFr(to * ease(p));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (counters.length) {
    var priceIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var group = e.target.querySelectorAll('.cnt');
          group.forEach(function (c, i) { setTimeout(function () { animateCounter(c); }, i * 120); });
          priceIo.unobserve(e.target);
        }
      });
    }, { threshold: 0.3 });
    document.querySelectorAll('.pcard').forEach(function (card) { priceIo.observe(card); });
  }

  // subtle 3D tilt on pricing cards (pointer devices only)
  if (!reduced && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.pcard').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        var lift = card.classList.contains('pop') ? -3 : -6;
        card.style.transform = 'perspective(900px) rotateY(' + (x * 7) + 'deg) rotateX(' + (-y * 7) + 'deg) translateY(' + lift + 'px)';
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
  }

  // contact form: friendlier inline confirmation on successful Netlify submit
  var form = document.querySelector('form[name="contact"]');
  if (form) {
    form.addEventListener('submit', function (e) {
      if (window.location.hostname === 'localhost' || window.location.protocol === 'file:') return;
      e.preventDefault();
      var data = new FormData(form);
      fetch('/', { method: 'POST', body: new URLSearchParams(data) })
        .then(function () {
          form.reset();
          var note = form.querySelector('.form-note');
          if (note) note.classList.add('show');
        })
        .catch(function () { form.submit(); });
    });
  }
})();
