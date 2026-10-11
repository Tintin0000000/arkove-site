/* Le garage : section "méthode" en défilement horizontal épinglé */
(function () {
  var PL = window.PL;
  var section = document.querySelector('.method');
  if (!section) return;
  var pin = section.querySelector('.method-pin');
  var track = section.querySelector('.method-track');
  var car = section.querySelector('.car-icon');
  var road = section.querySelector('.method-road');
  var mq = window.matchMedia('(max-width: 900px)');
  var dist = 0;

  function layout() {
    if (mq.matches || PL.reduced) { section.style.height = ''; track.style.transform = ''; return; }
    dist = Math.max(0, track.scrollWidth - window.innerWidth);
    section.style.height = (window.innerHeight + dist) + 'px';
    update();
  }
  function update() {
    if (mq.matches || PL.reduced) return;
    var top = section.getBoundingClientRect().top;
    var p = Math.min(1, Math.max(0, -top / (dist || 1)));
    track.style.transform = 'translate3d(' + (-p * dist) + 'px,0,0)';
    if (car) car.style.setProperty('--x', (p * road.clientWidth) + 'px');
  }
  window.addEventListener('scroll', function () { requestAnimationFrame(update); }, { passive: true });
  window.addEventListener('resize', layout);
  if (document.fonts) document.fonts.ready.then(layout);
  layout();
})();
