(() => {
  const nav = document.querySelector('.projects-nav');
  if (!nav) return;
  const details = nav.querySelector('details');
  const summary = details.querySelector('summary');
  const update = () => summary.setAttribute('aria-expanded', String(details.open || nav.matches(':hover') || nav.contains(document.activeElement)));
  nav.addEventListener('mouseenter', update);
  nav.addEventListener('mouseleave', update);
  nav.addEventListener('focusin', update);
  nav.addEventListener('focusout', () => setTimeout(update, 0));
  details.addEventListener('toggle', update);
  update();
})();
