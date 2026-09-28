const navigation = document.querySelector('.navigation');
const toggle = document.querySelector('.menu-toggle');
const links = document.querySelector('#nav-links');

if (navigation && toggle && links) {
  navigation.classList.add('enhanced');
  toggle.hidden = false;
  function setOpen(open) {
    toggle.setAttribute('aria-expanded', String(open));
    links.classList.toggle('is-open', open);
  }
  toggle.addEventListener('click', () => {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });
  links.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      toggle.focus();
    }
  });
  window.matchMedia('(min-width: 621px)').addEventListener('change', () => setOpen(false));
}
