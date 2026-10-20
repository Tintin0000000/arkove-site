/* Espace d'administration de Pierre-Lou (Decap CMS) */
(function () {
  if (!window.CMS) {
    document.body.innerHTML = '<p style="font:16px system-ui;padding:24px">L\'espace d\'administration n\'a pas pu se charger. Vérifiez la connexion internet puis rechargez la page.</p>';
    return;
  }

  if (!window.PL_DEMO) { CMS.init(); return; }

  // Mode démonstration : le contenu actuel du site est chargé en mémoire.
  var bar = document.createElement('div');
  bar.className = 'demo-bar';
  bar.innerHTML = '<b>Démonstration</b> : vous pouvez tout essayer, rien n\'est enregistré sur le site.';
  document.body.appendChild(bar);

  function text(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.text() : '{}'; }).catch(function () { return '{}'; });
  }
  Promise.all([text('../content/vehicules.json'), text('../content/photos.json')]).then(function (files) {
    window.repoFiles = {
      content: {
        'vehicules.json': { content: files[0] },
        'photos.json': { content: files[1] }
      }
    };
    var site = new URL('../index.html', location.href).href;
    CMS.init({ config: { backend: { name: 'test-repo' }, site_url: site, display_url: site } });
  });
})();
