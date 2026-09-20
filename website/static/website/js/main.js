const header = document.querySelector('[data-header]');
const toggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');

function closeNav() {
  if (!nav || !toggle) return;
  nav.classList.remove('is-open');
  toggle.setAttribute('aria-expanded', 'false');
  document.body.classList.remove('nav-open');
}

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('nav-open', open);
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeNav);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) closeNav();
  });
}

if (header) {
  const onScroll = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

const LEAD_EMAIL = 'tejastalole7@gmail.com';

function selectedLabel(select) {
  if (!select || select.selectedIndex < 0) return '';
  return (select.options[select.selectedIndex].textContent || '').trim();
}

function buildLeadPayload(form) {
  const fd = new FormData(form);
  const kind = form.getAttribute('data-notify-email');
  const name = (fd.get('name') || '').toString().trim();
  const email = (fd.get('email') || '').toString().trim();
  const phone = (fd.get('phone') || '-').toString().trim() || '-';

  if (kind === 'contact') {
    const subject = (fd.get('subject') || '').toString().trim();
    const message = (fd.get('message') || '').toString().trim();
    return {
      name,
      email,
      phone,
      subject,
      _subject: `WebMarblow contact: ${subject}`,
      _template: 'table',
      _captcha: 'false',
      message: [
        'New contact enquiry from WebMarblow website',
        '==========================================',
        '',
        `Name: ${name}`,
        `Email: ${email}`,
        `Phone: ${phone}`,
        `Subject: ${subject}`,
        '',
        'Message:',
        message,
      ].join('\n'),
    };
  }

  const company = (fd.get('company') || '-').toString().trim() || '-';
  const service = selectedLabel(form.querySelector('[name="service"]')) || 'Not selected';
  const budget = selectedLabel(form.querySelector('[name="budget"]')) || '-';
  const timeline = selectedLabel(form.querySelector('[name="timeline"]')) || '-';
  const details = (fd.get('project_details') || '').toString().trim();

  return {
    name,
    email,
    phone,
    company,
    service,
    budget,
    timeline,
    _subject: `WebMarblow quote request from ${name}`,
    _template: 'table',
    _captcha: 'false',
    message: [
      'New quote request from WebMarblow website',
      '========================================',
      '',
      `Name: ${name}`,
      `Email: ${email}`,
      `Phone: ${phone}`,
      `Company: ${company}`,
      `Service: ${service}`,
      `Budget: ${budget}`,
      `Timeline: ${timeline}`,
      '',
      'Project details:',
      details,
    ].join('\n'),
  };
}

async function notifyOwnerByEmail(form) {
  const payload = buildLeadPayload(form);
  const response = await fetch(`https://formsubmit.co/ajax/${LEAD_EMAIL}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(payload),
  });
  const result = await response.json().catch(() => ({}));
  return result;
}

document.querySelectorAll('form[data-notify-email]').forEach((form) => {
  form.addEventListener('submit', async (event) => {
    if (form.dataset.leadMailDone === '1') return;

    event.preventDefault();
    const button = form.querySelector('[type="submit"]');
    const original = button ? button.textContent : '';
    if (button) {
      button.disabled = true;
      button.textContent = 'Sending...';
    }

    try {
      await notifyOwnerByEmail(form);
    } catch (error) {
      console.warn('Lead email notify failed', error);
    }

    form.dataset.leadMailDone = '1';
    HTMLFormElement.prototype.submit.call(form);
    if (button) {
      button.disabled = false;
      button.textContent = original;
    }
  });
});
