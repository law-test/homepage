/* Runs the real measurement controller against a network-free browser fixture. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/ad-measurement.js'), 'utf8');
const product = 'https://smartstore.naver.com/lawtest/products/11200654869';
const key = 'lawtest.ad-measurement-choice.v1';

function fixture(saved, storageBlocked = false) {
  const nodes = new Map();
  function node(id) {
    const listeners = new Map();
    const element = {
      id, hidden: true, attrs: {}, focused: false, textContent: '',
      addEventListener(name, fn) { listeners.set(name, fn); },
      setAttribute(name, value) { this.attrs[name] = value; },
      focus() { this.focused = true; },
      fire(name, event = {}) { const fn = listeners.get(name); if (fn) fn(event); }
    };
    nodes.set(id, element);
    return element;
  }
  const panel = node('ad-measurement-choice');
  const settings = node('ad-measurement-settings');
  node('ad-measurement-status');
  node('ad-measurement-title');
  const allow = node('allow'), deny = node('deny');
  panel.querySelector = selector => selector.includes('granted') ? allow : deny;
  const requests = [], calls = [], stored = new Map(saved ? [[key, saved]] : []);
  const documentEvents = new Map(), windowEvents = new Map();
  const document = {
    currentScript: { dataset: { pixelId: 'QKaPHrP1F9qNCjJCJYftU3', productUrl: product } },
    getElementById(id) { return nodes.get(id); },
    createElement(tag) { assert.equal(tag, 'script'); return {}; },
    head: { appendChild(script) { requests.push(script); } },
    addEventListener(name, fn) { documentEvents.set(name, fn); }
  };
  const window = {
    location: { href: 'https://lawtest.or.kr/guide.html' },
    localStorage: {
      getItem(name) { if (storageBlocked) throw Error('blocked'); return stored.get(name) || null; },
      setItem(name, value) { if (storageBlocked) throw Error('blocked'); stored.set(name, value); }
    },
    addEventListener(name, fn) { windowEvents.set(name, fn); }
  };
  vm.runInNewContext(source, { window, document, URL });
  function loadSdk() {
    assert.ok(requests.length, 'SDK must have been requested');
    const queued = window.oaiq.q || [];
    window.oaiq = (...args) => calls.push(args);
    queued.forEach(args => window.oaiq(...args));
    requests.at(-1).onload();
  }
  function linkClick(href, overrides = {}) {
    const event = {
      type: 'click', button: 0, defaultPrevented: false,
      target: { closest: () => ({ href, hasAttribute: name => name === 'download' && !!overrides.download }) },
      ...overrides
    };
    documentEvents.get(event.type)(event);
  }
  return {
    panel, settings, allow, deny, requests, calls, nodes, loadSdk, linkClick,
    events: () => calls.filter(call => call[0] === 'measure'),
    storage: (newValue, changedKey = key) => windowEvents.get('storage')({ key: changedKey, newValue })
  };
}

let f = fixture();
assert.equal(f.panel.hidden, false);
assert.equal(f.settings.hidden, false);
assert.equal(f.requests.length, 0, 'No SDK request before choice');
f.linkClick(product);
assert.equal(f.events().length, 0);
f.deny.fire('click');
assert.equal(f.panel.hidden, true);
f.linkClick(product);
assert.equal(f.requests.length, 0, 'Denial must not load the SDK');
assert.equal(f.events().length, 0);

f = fixture();
f.allow.fire('click');
assert.equal(f.requests.length, 1);
assert.equal(f.requests[0].src, 'https://bzrcdn.openai.com/sdk/oaiq.min.js');
assert.equal(f.events().length, 0, 'Wait for a loaded SDK and current consent');
f.loadSdk();
assert.deepEqual(f.events().map(e => e[1]), ['page_viewed']);
f.allow.fire('click');
assert.equal(f.requests.length, 1, 'Only one SDK per page');
assert.equal(f.events().length, 1, 'One page view even after reopening settings');
f.linkClick(product);
f.linkClick(product + '?utm_source=chatgpt');
f.linkClick(product, { type: 'auxclick', button: 1 });
assert.deepEqual(f.events().map(e => e[1]), ['page_viewed', 'custom', 'custom', 'custom']);
assert.ok(f.events().slice(1).every(e => e[3].custom_event_name === 'smartstore_click'));
const beforeUnrelated = f.events().length;
for (const url of [
  '/guide.html', '/privacy.html', 'https://naver.me/51uDf3Nh',
  'https://smartstore.naver.com/lawtest',
  'https://smartstore.naver.com/lawtest/products/another',
  'https://example.com/lawtest/products/11200654869',
  'https://smartstore.naver.com.example.com/lawtest/products/11200654869',
  'http://smartstore.naver.com/lawtest/products/11200654869'
]) f.linkClick(url);
f.linkClick(product, { defaultPrevented: true });
f.linkClick(product, { download: true });
f.linkClick(product, { type: 'auxclick', button: 2 });
f.linkClick(product, { button: 2 });
assert.equal(f.events().length, beforeUnrelated, 'Unrelated or cancelled navigation must not be a conversion');
assert.ok(f.events().every(e => e[3].opt_out === true));
assert.ok(f.events().every(e => !['order_created', 'registration_completed', 'checkout_started', 'lead_created'].includes(e[1])));
assert.ok(f.calls.filter(c => c[0] === 'init').every(c => Object.keys(c[1]).join() === 'pixelId'), 'No direct customer identifiers');
f.settings.fire('click');
assert.equal(f.panel.hidden, false);
assert.equal(f.nodes.get('ad-measurement-title').focused, true);
f.deny.fire('click');
assert.equal(f.settings.focused, true);
assert.deepEqual(f.calls.at(-1), ['consent', false], 'Withdrawal disables the official SDK');
f.linkClick(product);
assert.equal(f.events().length, beforeUnrelated);
f.allow.fire('click');
assert.equal(f.events().filter(e => e[1] === 'page_viewed').length, 1);
f.linkClick(product);
assert.equal(f.events().length, beforeUnrelated + 1);

f = fixture();
f.allow.fire('click');
f.linkClick(product); // SDK is still loading.
f.deny.fire('click');
f.loadSdk();
assert.equal(f.events().length, 0, 'Withdrawal during loading discards pending events');
assert.deepEqual(f.calls.at(-1), ['consent', false]);

f = fixture();
f.allow.fire('click');
f.linkClick(product);
f.loadSdk();
assert.deepEqual(f.events().map(e => e[1]), ['page_viewed', 'custom']);

f = fixture('denied');
assert.equal(f.panel.hidden, true);
assert.equal(f.requests.length, 0);
f = fixture('granted');
assert.equal(f.panel.hidden, true);
assert.equal(f.requests.length, 1);
f.loadSdk();
assert.deepEqual(f.events().map(e => e[1]), ['page_viewed']);
f.storage('denied');
f.linkClick(product);
assert.equal(f.events().length, 1, 'Withdrawal in another tab is respected');
f.storage(null, null);
assert.equal(f.panel.hidden, false);
f = fixture('unexpected');
assert.equal(f.panel.hidden, false);
assert.equal(f.requests.length, 0);
f = fixture('granted', true);
assert.equal(f.requests.length, 0, 'Unavailable storage cannot imply consent');
f.allow.fire('click');
f.loadSdk();
assert.equal(f.events().length, 1);

console.log('PASS: consent gating, withdrawal/loading race, stored/cross-tab choices, one page view, exact product clicks, unrelated links and no purchase/registration/PII events. No network requests were sent.');
