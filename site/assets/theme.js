(() => {
  document.documentElement.classList.add('js');
  let theme;
  try { theme = localStorage.getItem('minrui-theme'); } catch (_) {}
  if (theme !== 'dark' && theme !== 'light') {
    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  document.documentElement.dataset.theme = theme;
})();
