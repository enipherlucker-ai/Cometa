// https://nuxt.com/docs/api/configuration/nuxt-config
const apiTarget = process.env.API_PROXY_TARGET ?? 'http://127.0.0.1:8000'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  app: {
      head: {
          title: 'Cometa',
          htmlAttrs: { lang: 'ru' },
      },
  },
  routeRules: {
    '/api/auth/**': { proxy: `${apiTarget}/auth/**` },
    '/api/receipt/**': { proxy: `${apiTarget}/receipt/**` },
  },
})