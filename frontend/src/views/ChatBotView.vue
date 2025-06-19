<template>
    <div v-if="show" :class="{ 'd-block': show }" style="display: none" class="vh-100 overflow-hidden">
        <div class="container h-100 py-4 my-0 position-relative">
            <div class="flex-grow-1 overflow-auto rounded shadow-sm vh-100 px-5" style="font-size: 0.9rem;">
                <div v-for="(chat, index) in chatLogs" :key="index" class="mb-2">
                    <div :class="{'text-end': chat.role === 'user', 'text-start': chat.role === 'ai'}">
                        <div :class="['d-inline-block p-2 rounded', chat.role === 'user' ? 'bg-primary text-white' : 'bg-secondary text-white']" style="max-width: 70%">
                            {{ chat.message }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="input-group position-absolute bottom-0 start-0 end-0 mb-5 px-5">
                <input type="text" class="form-control" placeholder="Ketik pesan..." v-model="newMessage" @keyup.enter="sendMessage" />
                <button class="btn btn-primary" @click="sendMessage">Kirim</button>
            </div>
        </div>
    </div>
</template>
<script>
import { useUserDataStore } from "@/store/UserDataStore";

export default {
    name: "ChatBotView",
    data() {
        return {
            show: false,
            chatLogs: [
                {
                    role: "user",
                    message: "Hello",
                },
                {
                    role: "ai",
                    message: "Hello, how can i assist you today?",
                },
            ],
        };
    },
    async mounted() {
        if (!(await useUserDataStore().isLoggedInCheck())) {
            this.$router.push("/login");
        }
        this.show = true;
    },
    methods: {},
};
</script>
