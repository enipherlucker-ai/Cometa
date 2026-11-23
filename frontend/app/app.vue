<template>
  <NuxtPage />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=Unbounded:wght@500;700&display=swap');

:root {
  --paper: #edf0f5;
  --surface: #ffffff;
  --ink: #1a2142;
  --ink-soft: #5b6382;
  --line: #cdd3e1;
  --accent: #3046c5;
  --accent-hover: #22349e;
  --accent-muted: #a9b3e6;
  --star: #f5b82e;
  --danger: #b4322a;
  --danger-bg: #fcebe9;

  --font-display: 'Unbounded', system-ui, sans-serif;
  --font-body: 'Golos Text', system-ui, sans-serif;

  --radius-s: 8px;
  --radius-m: 14px;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.5;
  background: var(--paper);
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
}

h1,
h2 {
  font-family: var(--font-display);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.01em;
  margin: 0;
}

a {
  color: var(--accent);
  text-underline-offset: 3px;
}

a:hover {
  color: var(--accent-hover);
}

button {
  font: inherit;
  font-weight: 600;
  padding: 11px 20px;
  border: 2px solid var(--accent);
  border-radius: var(--radius-s);
  background: var(--accent);
  color: #fff;
  cursor: pointer;
  transition: background-color 0.15s, border-color 0.15s;
}

button:hover:not(:disabled) {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
}

button:disabled {
  background: var(--accent-muted);
  border-color: var(--accent-muted);
  cursor: wait;
}

input {
  font: inherit;
  padding: 10px 12px;
  border: 1.5px solid var(--line);
  border-radius: var(--radius-s);
  background: var(--surface);
  color: var(--ink);
}

input::placeholder {
  color: #9aa1b8;
}

:focus-visible {
  outline: 3px solid var(--star);
  outline-offset: 2px;
}

input:focus-visible {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(48, 70, 197, 0.2);
}

@media (prefers-reduced-motion: reduce) {
  * {
    transition: none !important;
    animation: none !important;
  }
}
</style>
