<template>
    <MenuItem v-if="store.deleting">
        <Trash class="trash-icon"/>
        <span>{{ $t("confirm") }}</span>
        <div class="confirm-controls">
            <Close class="close-icon" @click="() => {store.deleting = false}"/>
            <Check class="check-icon" @click="deleteConversations"/>
        </div>
    </MenuItem>
    <MenuItem v-else @click="store.deleting = true; store.downloading = false;">
        <Trash class="trash-icon"/>
        <span v-if="store.selectedConversations.length">{{ $t("deleteselected") }}</span>
        <span v-else>{{ $t("clearhistory") }}</span>
    </MenuItem>
</template>

<script setup>
import Check from "~/components/icons/Check.vue";
import Close from "~/components/icons/Close.vue";
import { useGlobalStore } from "~/store";

const store = useGlobalStore();

import MenuItem from "~/components/left-menu/items/abs/MenuItem.vue";
import Trash from "~/components/icons/Trash.vue";

async function deleteConversation(id) {
    if (store.previewMode)
        return

    const headers = { "Content-Type": "application/json" }
    if (store.authToken)
        headers.Authorization = `Token ${store.authToken}`;

    await chatfaqFetch(
        store.chatfaqAPI + `/back/api/broker/conversations/${id}/`,
        {
            method: "DELETE",
            headers,
        }
    );
}

async function deleteConversations() {
    if(store.previewMode)
        return

    const ids = store.selectedConversations.length ? store.selectedConversations : store.conversationsIds
    await Promise.all(ids.map(id => deleteConversation(id)))
    await store.gatherConversations()

    store.selectedConversations = []
    store.deleting = false
}

</script>


<style lang="scss" scoped>

.trash-icon {
    color: $chatfaq-trash-icon-color;
}
.confirm-controls {
    margin-left: auto;
    display: flex;
    flex-direction: row-reverse;
    .check-icon {
        color: $chatfaq-menu-check-icon-color;
    }
    .close-icon {
        color: $chatfaq-close-icon-color;
    }
}
</style>

