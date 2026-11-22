(() => {
  const images = document.querySelectorAll('main img');
  if (!images.length) return;

  const dialog = document.createElement('dialog');
  dialog.className = 'image-viewer';
  dialog.setAttribute('aria-label', 'Enlarged image');
  dialog.innerHTML = '<button type="button" class="image-viewer-close" aria-label="Close image viewer">×</button><div class="image-viewer-controls" role="group" aria-label="Image zoom"><button type="button" data-zoom="out" aria-label="Zoom out">−</button><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" data-zoom="reset">Reset</button></div><figure><img alt=""><figcaption hidden></figcaption></figure>';
  document.body.append(dialog);
  const large = dialog.querySelector('img');
  const caption = dialog.querySelector('figcaption');
  const close = dialog.querySelector('button');
  let opener;
  let scale = 1, offsetX = 0, offsetY = 0;
  const renderZoom = () => { large.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`; };

  for (const img of images) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'image-expand';
    button.setAttribute('aria-label', `Enlarge image: ${img.alt || 'project image'}`);
    img.replaceWith(button);
    button.append(img);
    button.addEventListener('click', () => {
      opener = button;
      large.src = img.currentSrc || img.src;
      large.alt = img.alt;
      const figure = button.closest('.section-image-item') || button.closest('figure');
      const text = (figure?.querySelectorAll('img').length === 1 ? figure.querySelector('figcaption')?.textContent.trim() : '') || '';
      caption.textContent = text;
      caption.hidden = !text;
      scale = 1; offsetX = 0; offsetY = 0; renderZoom();
      dialog.showModal();
      document.body.classList.add('image-viewer-open');
      close.focus();
    });
  }
  close.addEventListener('click', () => dialog.close());
  dialog.querySelector('.image-viewer-controls').addEventListener('click', event => {
    const action = event.target.dataset.zoom;
    if (!action) return;
    scale = action === 'reset' ? 1 : Math.min(5, Math.max(1, scale * (action === 'in' ? 1.25 : 0.8)));
    offsetX = 0; offsetY = 0; renderZoom();
  });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('wheel', event => {
    event.preventDefault();
    const next = Math.min(5, Math.max(1, scale * Math.exp(-event.deltaY * 0.0015)));
    if (next === scale) return;
    const rect = large.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const ratio = next / scale;
    offsetX += (event.clientX - centerX) * (1 - ratio);
    offsetY += (event.clientY - centerY) * (1 - ratio);
    scale = next;
    if (scale === 1) { offsetX = 0; offsetY = 0; }
    renderZoom();
  }, { passive: false });
  dialog.addEventListener('close', () => { document.body.classList.remove('image-viewer-open'); large.removeAttribute('src'); opener?.focus(); });
})();
