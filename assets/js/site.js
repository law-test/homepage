(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  ready(function () {
    var btn = document.querySelector('.menu-toggle');
    var nav = document.querySelector('nav.primary');
    if (btn && nav) {
      btn.addEventListener('click', function () {
        var isOpen = nav.classList.toggle('open');
        btn.setAttribute('aria-expanded', String(isOpen));
      });
      nav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          nav.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
        });
      });
    }
  });
})();


// ============================================================
// Lightbox for ceremony photos
// ============================================================
(function() {
  var lb = document.getElementById('lightbox');
  if (!lb) return;
  var img = lb.querySelector('.lb-image');
  var title = lb.querySelector('.lb-title');
  var article = lb.querySelector('.lb-article');
  var btnClose = lb.querySelector('.lb-close');
  var btnPrev = lb.querySelector('.lb-prev');
  var btnNext = lb.querySelector('.lb-next');

  // Collect all eligible cards
  var cards = Array.prototype.slice.call(
    document.querySelectorAll('[data-lightbox]')
  );
  if (!cards.length) return;
  var current = 0;
  var lastFocus = null;

  function show(idx) {
    var card = cards[idx];
    if (!card) return;
    current = idx;
    var cardImg = card.querySelector('img');
    var titleText = '';

    // Prefer explicit data-lb-title attribute if provided
    var explicitTitle = card.getAttribute('data-lb-title');
    if (explicitTitle) {
      titleText = explicitTitle;
    } else {
      var heading = card.querySelector('h3');
      var roundEl = card.querySelector('.ceremony-round');
      var dateEl = card.querySelector('.ceremony-meta span:last-child');
      var headingText = heading ? heading.textContent.trim() : '';
      var roundText = roundEl ? roundEl.textContent.trim() : '';
      // Avoid duplication if heading already contains round (e.g. "제1회 시상식" already includes "제1회")
      if (roundText && headingText.indexOf(roundText) === -1) {
        titleText += roundText;
      }
      if (headingText) titleText += (titleText ? ' · ' : '') + headingText;
      if (dateEl) titleText += (titleText ? ' · ' : '') + dateEl.textContent.trim();
    }

    img.src = cardImg.src;
    img.alt = cardImg.alt || '';
    title.textContent = titleText;
    var articleUrl = card.getAttribute('data-article');
    if (articleUrl) {
      article.href = articleUrl;
      // External URL opens in new tab; same-site / relative URL opens in same tab.
      var isExternal = /^https?:\/\//i.test(articleUrl) &&
                       articleUrl.indexOf(window.location.origin) !== 0;
      if (isExternal) {
        article.setAttribute('target', '_blank');
        article.setAttribute('rel', 'external noopener');
      } else {
        article.removeAttribute('target');
        article.removeAttribute('rel');
      }
      article.hidden = false;
    } else {
      article.hidden = true;
    }
  }

  function open(idx) {
    lastFocus = document.activeElement;
    show(idx);
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    btnClose.focus();
  }

  function close() {
    lb.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  function next() { show((current + 1) % cards.length); }
  function prev() { show((current - 1 + cards.length) % cards.length); }

  // Wire up triggers
  cards.forEach(function(card, i) {
    card.setAttribute('tabindex', '0');
    card.setAttribute('role', 'button');
    card.setAttribute('aria-label', '시상식 사진 크게 보기');
    card.addEventListener('click', function(e) {
      // Don't trigger if user clicked a link inside the card
      if (e.target.tagName === 'A') return;
      open(i);
    });
    card.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        open(i);
      }
    });
  });

  btnClose.addEventListener('click', close);
  btnPrev.addEventListener('click', prev);
  btnNext.addEventListener('click', next);

  // Close lightbox when the article link is clicked,
  // so the modal doesn't stay open during/after navigation.
  if (article) {
    article.addEventListener('click', function() { close(); });
  }

  // Click on backdrop closes
  lb.addEventListener('click', function(e) {
    if (e.target === lb) close();
  });

  // Keyboard
  document.addEventListener('keydown', function(e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') next();
    else if (e.key === 'ArrowLeft') prev();
  });
})();
