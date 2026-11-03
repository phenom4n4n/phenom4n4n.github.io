(() => {
  const images = document.querySelectorAll('main img');
  if (!images.length) return;

  const dialog = document.createElement('dialog');
  dialog.className = 'image-viewer';
  dialog.setAttribute('aria-label', 'Enlarged image');
  dialog.innerHTML = '<button type="button" class="image-viewer-close" aria-label="Close image viewer">×</button><figure><img alt=""><figcaption hidden></figcaption></figure>';
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
      const figure = button.closest('figure');
      const text = figure?.querySelector('figcaption')?.textContent.trim() || '';
      caption.textContent = text;
      caption.hidden = !text;
      scale = 1; offsetX = 0; offsetY = 0; renderZoom();
      dialog.showModal();
      document.body.classList.add('image-viewer-open');
      close.focus();
    });
  }
  close.addEventListener('click', () => dialog.close());
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
