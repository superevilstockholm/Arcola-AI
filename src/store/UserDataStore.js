import { defineStore } from "pinia";

import axios from "axios";

export const useUserDataStore = defineStore("userData", {
    state: () => ({
        isLoggedIn: false,
        userData: null,
    }),
    actions: {
        async isLoggedInCheck() {
            await axios
                .get("/api/user", { withCredentials: true })
                .then((response) => {
                    if (response.status == 200) {
                        if (response.data.status) {
                            if (response.data.message == "1") {
                                this.isLoggedIn = true;
                            }
                        }
                    }
                    this.isLoggedIn = false;
                })
                .catch(() => {
                    this.isLoggedIn = false;
                });
        },
    },
});
