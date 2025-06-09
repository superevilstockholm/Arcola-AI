import { defineStore } from "pinia";

import axios from "axios";

export const useUserDataStore = defineStore("userData", {
    state: () => ({
        userData: null,
    }),
    actions: {
        async isLoggedInCheck() {
            try {
                const response = await axios.get("/api/isLoggedIn", { withCredentials: true });
                if (response.status == 200) {
                    if (response.data.status) {
                        if (response.data.message == "1") {
                            return true;
                        }
                    }
                }
                return false;                
            } catch {
                return false;
            }
        },
    },
});
