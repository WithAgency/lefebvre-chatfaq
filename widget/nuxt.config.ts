// https://nuxt.com/docs/api/configuration/nuxt-config
import dns from "dns";
dns.setDefaultResultOrder('ipv4first')

export default defineNuxtConfig({
    ssr: false,
    css: [
        'primevue/resources/themes/saga-blue/theme.css',
        'primevue/resources/primevue.css',
        'primeicons/primeicons.css',
        'primeflex/primeflex.css',
        '~/assets/styles/global.scss'
    ],
    build: {
        transpile: ['primevue']
    },
    runtimeConfig: {
        // The private keys which are only available server-side
        // privateKey: process.env.PRIVATE_KEY,
        // Keys within public are also exposed client-side
        public: {
            chatfaqAPI: process.env.CHATFAQ_BACKEND_API,
            chatfaqWS: process.env.CHATFAQ_BACKEND_WS,
        }
    },
    app: {
        head: {
            style: [
                {children: 'body { margin: 0 }'}
            ],
        }
    }
})
