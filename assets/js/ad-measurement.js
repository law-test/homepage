/* Optional ChatGPT ad measurement. No SDK request is made before consent. */
(function () {
  'use strict';
  const config = document.currentScript;
  const panel = document.getElementById('ad-measurement-choice');
  const settings = document.getElementById('ad-measurement-settings');
  const status = document.getElementById('ad-measurement-status');
  if (!config || !panel || !settings) return;

  const storageKey = 'lawtest.ad-measurement-choice.v1';
  const pixelId = config.dataset.pixelId;
  let productUrl;
  try { productUrl = new URL(config.dataset.productUrl); } catch (_) { return; }
  let choice = null;
  try {
    const stored = window.localStorage.getItem(storageKey);
    if (stored === 'granted' || stored === 'denied') choice = stored;
  } catch (_) { /* A blocked storage API must not imply consent. */ }

  let sdkReady = false;
  let sdkLoading = false;
  let pageMeasured = false;
  let pendingClicks = 0;
  let returnFocus = false;

  function measurePage() {
    if (choice !== 'granted' || !sdkReady || pageMeasured) return;
    pageMeasured = true;
    window.oaiq('measure', 'page_viewed', { type: 'contents' }, { opt_out: true });
  }

  function measureClick() {
    window.oaiq('measure', 'custom', { type: 'custom' }, {
      custom_event_name: 'smartstore_click', opt_out: true
    });
  }

  function enableMeasurement() {
    if (choice !== 'granted') return;
    if (sdkReady) {
      window.oaiq('consent', true);
      measurePage();
      return;
    }
    if (sdkLoading) return;
    sdkLoading = true;
    if (!window.oaiq) {
      const queue = function () { queue.q.push(arguments); };
      queue.q = [];
      window.oaiq = queue;
    }
    // Keep the SDK disabled while it loads, including if consent is withdrawn.
    window.oaiq('consent', false);
    window.oaiq('init', { pixelId: pixelId });
    const sdk = document.createElement('script');
    sdk.async = true;
    sdk.src = 'https://bzrcdn.openai.com/sdk/oaiq.min.js';
    sdk.onload = function () {
      sdkLoading = false;
      sdkReady = true;
      window.oaiq('consent', choice === 'granted');
      if (choice !== 'granted') { pendingClicks = 0; return; }
      measurePage();
      while (pendingClicks > 0) { pendingClicks -= 1; measureClick(); }
    };
    sdk.onerror = function () { sdkLoading = false; pendingClicks = 0; };
    document.head.appendChild(sdk);
  }

  function choose(value) {
    choice = value;
    try { window.localStorage.setItem(storageKey, value); } catch (_) {}
    panel.hidden = true;
    settings.setAttribute('aria-expanded', 'false');
    if (choice === 'granted') {
      enableMeasurement();
      status.textContent = '광고 측정을 허용했습니다. 광고 측정 설정에서 언제든 변경할 수 있습니다.';
    } else {
      pendingClicks = 0;
      if (window.oaiq) window.oaiq('consent', false);
      status.textContent = '광고 측정을 거부했습니다. 홈페이지와 참가 신청은 그대로 이용할 수 있습니다.';
    }
    if (returnFocus) settings.focus();
    returnFocus = false;
  }

  settings.hidden = false;
  settings.addEventListener('click', function () {
    panel.hidden = false;
    settings.setAttribute('aria-expanded', 'true');
    returnFocus = true;
    document.getElementById('ad-measurement-title').focus();
  });
  panel.querySelector('[data-ad-consent="granted"]').addEventListener('click', function () { choose('granted'); });
  panel.querySelector('[data-ad-consent="denied"]').addEventListener('click', function () { choose('denied'); });

  function onProductClick(event) {
    if (choice !== 'granted' || event.defaultPrevented) return;
    if (event.type === 'click' && event.button !== 0) return;
    if (event.type === 'auxclick' && event.button !== 1) return;
    const target = event.target;
    const link = target && target.closest ? target.closest('a[href]') : null;
    if (!link || link.hasAttribute('download')) return;
    let destination;
    try { destination = new URL(link.href, window.location.href); } catch (_) { return; }
    if (destination.origin !== productUrl.origin || destination.pathname !== productUrl.pathname) return;
    if (sdkReady) measureClick(); else pendingClicks += 1;
    // Never delay, redirect, or otherwise interfere with the actual navigation.
  }
  document.addEventListener('click', onProductClick);
  document.addEventListener('auxclick', onProductClick);
  window.addEventListener('storage', function (event) {
    if (event.key !== storageKey && event.key !== null) return;
    choice = event.newValue === 'granted' ? 'granted' : event.newValue === 'denied' ? 'denied' : null;
    pendingClicks = 0;
    if (choice === 'granted') enableMeasurement();
    else if (window.oaiq) window.oaiq('consent', false);
    panel.hidden = choice !== null;
    settings.setAttribute('aria-expanded', String(!panel.hidden));
  });

  panel.hidden = choice !== null;
  settings.setAttribute('aria-expanded', String(!panel.hidden));
  if (choice === 'granted') enableMeasurement();
})();
