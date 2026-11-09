(() => {
  const root = document.documentElement;
  const ja = root.lang === 'ja';
  const themeButton = document.querySelector('.theme-toggle');
  const updateThemeButton = () => {
    const dark = root.dataset.theme === 'dark';
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.setAttribute('aria-label', ja ? (dark ? 'ライトモードに切り替え' : 'ダークモードに切り替え') : (dark ? 'Switch to light mode' : 'Switch to dark mode'));
  };
  if (themeButton) {
    themeButton.hidden = false;
    updateThemeButton();
    themeButton.addEventListener('click', () => {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('minrui-theme', root.dataset.theme); } catch (_) {}
      updateThemeButton();
    });
  }
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  if (menu && navigation) {
    menu.hidden = false;
    const setMenu = (open) => {
      navigation.classList.toggle('is-open', open);
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', ja ? (open ? 'メニューを閉じる' : 'メニューを開く') : (open ? 'Close navigation menu' : 'Open navigation menu'));
    };
    menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menu.focus();
      }
    });
  }
  const filters = document.querySelector('.filters');
  if (filters) {
    filters.hidden = false;
    filters.addEventListener('click', event => {
      const selected = event.target.closest('button[data-filter]');
      if (!selected) return;
      const value = selected.dataset.filter;
      filters.querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(button === selected)));
      let count = 0;
      document.querySelectorAll('.publication').forEach(paper => {
        paper.hidden = value !== 'all' && paper.dataset.status !== value;
        if (!paper.hidden) count++;
      });
      document.querySelectorAll('.pub-year').forEach(year => {
        year.hidden = !Array.from(year.querySelectorAll('.publication')).some(paper => !paper.hidden);
      });
      document.querySelector('#filter-status').textContent = ja ? `${count} 件の論文を表示` : `Showing ${count} publication${count === 1 ? '' : 's'}`;
    });
  }
})();
