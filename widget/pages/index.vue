<template>
    <client-only>
        <Widget :chatfaqWs="chatfaqWS" :chatfaqApi="chatfaqAPI" :fsmDef="fsmDef" :title="title"
                :subtitle="subtitle" enable-logout allow-attachments speech-recognition speech-recognition-auto-send
                :hideSources="hideSources"
        />
    </client-only>
</template>
<script setup>
const conf = useRuntimeConfig()

const chatfaqWS = ref(conf.public.chatfaqWS)
const chatfaqAPI = ref(conf.public.chatfaqAPI)
const title = ref("Hello there 👋")
const subtitle = ref("How can we help you?")
const fsmDef = ref("llm_fsm")
const hideSources = ref(false)

</script>
