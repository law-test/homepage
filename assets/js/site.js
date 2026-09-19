/* Shared navigation, deep links and accessible photo viewer. */
(function () {
  'use strict';
  function ready(fn) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn); else fn(); }
  ready(function () {
    function updateEventStatuses() {
      const now = Date.now();
      document.querySelectorAll('[data-event-start][data-event-end]').forEach(label => {
        const start = Date.parse(label.dataset.eventStart), end = Date.parse(label.dataset.eventEnd);
        const state = now < start ? 'upcoming' : now < end ? 'active' : 'closed';
        label.textContent = state === 'upcoming' ? label.dataset.eventUpcoming : state === 'active' ? label.dataset.eventActive : '접수 종료';
        label.dataset.eventState = state;
      });
    }
    updateEventStatuses();
    window.setInterval(updateEventStatuses, 60000);
    const menu = document.querySelector('.menu-toggle'), nav = document.querySelector('nav.primary');
    function closeMenu(focus) { if (!menu || !nav) return; nav.classList.remove('open'); nav.style.maxHeight = ''; document.body.classList.remove('menu-open'); menu.setAttribute('aria-expanded', 'false'); if (focus) menu.focus(); }
    function fitMenu() {
      if (!nav || !nav.classList.contains('open')) return;
      nav.style.maxHeight = Math.max(0, window.innerHeight - nav.getBoundingClientRect().top - 12) + 'px';
    }
    if (menu && nav) {
      menu.addEventListener('click', () => {
        const open = nav.classList.toggle('open');
        menu.setAttribute('aria-expanded', String(open));
        document.body.classList.toggle('menu-open', open);
        if (open) fitMenu(); else nav.style.maxHeight = '';
      });
      nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(false); });
      document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(false); });
      document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) closeMenu(true); });
      window.addEventListener('resize', () => { if (window.matchMedia('(min-width: 861px)').matches) closeMenu(false); else fitMenu(); });
      window.addEventListener('scroll', fitMenu, {passive:true});
    }
    function openHash() {
      if (!location.hash) return;
      let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
      const target = document.getElementById(id); if (!target) return;
      const detail = target.matches('details') ? target : target.querySelector('details');
      if (detail) detail.open = true;
      let parent = target.parentElement;
      while (parent) { if (parent.matches('details')) parent.open = true; parent = parent.parentElement; }
      requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
    }
    window.addEventListener('hashchange', openHash);
    document.addEventListener('click', e => { const a = e.target.closest('a[href^="#"]'); if (a && a.hash === location.hash) openHash(); });
    openHash();
    document.querySelectorAll('.answer-block').forEach(detail => {
      function label() { const text = detail.querySelector('.toggle-text'); if (text) text.textContent = detail.open ? (detail.dataset.closeLabel || '정답 및 해설 닫기') : (detail.dataset.openLabel || '정답 및 해설 보기'); }
      detail.addEventListener('toggle', label); label();
    });
    const announcement = document.getElementById('contest-announcement');
    if (announcement && typeof announcement.showModal === 'function') {
      const day = () => new Date(Date.now() + 9 * 60 * 60 * 1000).toISOString().slice(0, 10);
      const storageKey = 'contest-2026-hwpx';
      const hiddenToday = () => { try { return localStorage.getItem(storageKey) === day(); } catch (_) { return false; } };
      const seen = () => { try { return sessionStorage.getItem(storageKey) === 'seen'; } catch (_) { return false; } };
      const show = () => { if (!announcement.open) announcement.showModal(); };
      announcement.addEventListener('close', () => {
        try {
          sessionStorage.setItem(storageKey, 'seen');
          if (announcement.querySelector('#contest-hide-today').checked) localStorage.setItem(storageKey, day());
        } catch (_) { /* The dialog remains usable if browser storage is disabled. */ }
      });
      announcement.querySelectorAll('[data-close-contest]').forEach(button => button.addEventListener('click', () => announcement.close()));
      announcement.querySelectorAll('a').forEach(link => link.addEventListener('click', () => announcement.close()));
      announcement.addEventListener('click', event => {
        if (event.target !== announcement) return;
        const box = announcement.getBoundingClientRect();
        if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) announcement.close();
      });
      document.querySelectorAll('[data-open-contest]').forEach(button => button.addEventListener('click', show));
      if (!location.hash && Date.now() < Date.parse('2026-09-27T00:00:00+09:00') && !hiddenToday() && !seen()) show();
    }
    const cards = Array.from(document.querySelectorAll('[data-lightbox]')).filter(card => card.querySelector('img'));
    if (!cards.length) return;
    let lb = document.getElementById('lightbox');
    if (!lb) {
      lb = document.createElement('div'); lb.id = 'lightbox'; lb.className = 'lightbox'; lb.hidden = true;
      lb.setAttribute('role','dialog'); lb.setAttribute('aria-modal','true'); lb.setAttribute('aria-labelledby','lb-title');
      lb.innerHTML = '<button type="button" class="lb-close" aria-label="사진 닫기">×</button><button type="button" class="lb-prev" aria-label="이전 사진">‹</button><button type="button" class="lb-next" aria-label="다음 사진">›</button><figure class="lb-figure"><img class="lb-image" alt=""><figcaption class="lb-caption"><div id="lb-title" class="lb-title"></div><div class="lb-position" aria-live="polite"></div><a class="lb-article" hidden>관련 기록 보기</a></figcaption></figure>';
      document.body.appendChild(lb);
    }
    const photo = lb.querySelector('.lb-image'), title = lb.querySelector('.lb-title'), article = lb.querySelector('.lb-article');
    const closeButton = lb.querySelector('.lb-close'), prevButton = lb.querySelector('.lb-prev'), nextButton = lb.querySelector('.lb-next'), position = lb.querySelector('.lb-position');
    let current = 0, lastFocus = null, previousOverflow = '', background = [];
    function caption(card) { return card.getAttribute('data-lb-title') || card.querySelector('img').alt || '대회 사진'; }
    function show(index) {
      current = (index + cards.length) % cards.length;
      const card = cards[current], image = card.querySelector('img');
      photo.src = card.getAttribute('data-full-src') || image.src; photo.alt = image.alt; title.textContent = caption(card);
      if (position) position.textContent = (current + 1) + ' / ' + cards.length;
      prevButton.hidden = nextButton.hidden = cards.length < 2;
      const url = card.getAttribute('data-article'); article.hidden = true; article.removeAttribute('href');
      if (url) {
        const resolved = new URL(url, location.href);
        if (['http:', 'https:'].includes(resolved.protocol)) {
          article.href = resolved.href; article.hidden = false;
          article.textContent = resolved.origin === location.origin ? '관련 기록 보기' : '관련 기사 보기 (새 창)';
          if (resolved.origin !== location.origin) { article.target = '_blank'; article.rel = 'noopener noreferrer'; }
          else { article.removeAttribute('target'); article.removeAttribute('rel'); }
        }
      }
    }
    function open(index) {
      lastFocus = document.activeElement; previousOverflow = document.body.style.overflow; show(index);
      background = Array.from(document.body.children).filter(el => el !== lb && !['SCRIPT','STYLE'].includes(el.tagName)).map(el => { const state = {el, inert:el.inert}; el.inert = true; return state; });
      lb.hidden = false; document.body.style.overflow = 'hidden'; closeButton.focus();
    }
    function close() {
      if (lb.hidden) return; lb.hidden = true; document.body.style.overflow = previousOverflow;
      background.forEach(state => { state.el.inert = state.inert; }); background = [];
      if (lastFocus && lastFocus.isConnected) lastFocus.focus();
    }
    cards.forEach((card,index) => {
      card.tabIndex = 0; card.setAttribute('role','button'); card.setAttribute('aria-haspopup','dialog'); card.setAttribute('aria-label',caption(card)+' 크게 보기');
      card.addEventListener('click',e => { if (!e.target.closest('a,button')) open(index); });
      card.addEventListener('keydown',e => { if (e.target === card && ['Enter',' '].includes(e.key)) { e.preventDefault(); open(index); } });
    });
    closeButton.addEventListener('click',close); prevButton.addEventListener('click',() => show(current-1)); nextButton.addEventListener('click',() => show(current+1)); article.addEventListener('click',close);
    lb.addEventListener('click',e => { if (e.target === lb) close(); });
    document.addEventListener('keydown',e => {
      if (lb.hidden) return;
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); show(current+1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); show(current-1); }
      else if (e.key === 'Tab') {
        const focusable = Array.from(lb.querySelectorAll('button,a[href],[tabindex="0"]')).filter(el => !el.hidden && !el.disabled && el.getClientRects().length);
        const first = focusable[0], last = focusable[focusable.length-1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  });
})();
