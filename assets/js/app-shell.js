(function () {
  function setActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.menu a').forEach((a) => {
      const href = a.getAttribute('href') || '';
      if (href === path || (path === '/' && href === '/')) {
        a.classList.add('is-active');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    setActiveNav();
  });
})();
