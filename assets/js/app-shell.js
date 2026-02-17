(function () {
  function ensureUtilityBar() {
    if (document.querySelector('.utility-bar')) return;
    const header = document.querySelector('.site-header');
    if (!header) return;
    const bar = document.createElement('div');
    bar.className = 'utility-bar';
    bar.innerHTML = `
      <div class="container utility-inner">
        <span class="utility-badge">Product Beta</span>
        <span class="utility-text">Data-first science intelligence. Updated hourly from approved sources.</span>
        <a href="/pages/sources.html" class="utility-link">Sources & licensing</a>
      </div>
    `;
    header.parentNode.insertBefore(bar, header);
  }

  function ensureFooter() {
    if (document.querySelector('.site-footer')) return;
    const body = document.body;
    const footer = document.createElement('footer');
    footer.className = 'site-footer';
    footer.innerHTML = `
      <div class="container footer-grid">
        <div>
          <h4>ScholarNotion</h4>
          <p>Evidence-led topics, charts, and AI news with transparent methodology.</p>
        </div>
        <div>
          <h4>Product</h4>
          <a href="/pages/topics.html">Topics</a>
          <a href="/pages/charts.html">Charts</a>
          <a href="/pages/ai-news.html">AI News</a>
        </div>
        <div>
          <h4>Trust</h4>
          <a href="/pages/methodology.html">Methodology</a>
          <a href="/pages/sources.html">Sources & licensing</a>
          <a href="/robots.txt">robots.txt</a>
        </div>
      </div>
      <div class="container footer-meta">© ScholarNotion · Built on Cloudflare</div>
    `;
    body.appendChild(footer);
  }

  function setActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.menu a').forEach((a) => {
      const href = a.getAttribute('href') || '';
      if (href === path || (path === '/' && href === '/')) {
        a.classList.add('is-active');
      }
    });
  }

  function styleMain() {
    const main = document.querySelector('main.container');
    if (main) main.classList.add('main-surface');
  }

  document.addEventListener('DOMContentLoaded', function () {
    ensureUtilityBar();
    styleMain();
    setActiveNav();
    ensureFooter();
  });
})();
