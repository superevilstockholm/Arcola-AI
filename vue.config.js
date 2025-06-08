const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        host: "127.0.0.1",
        port: 8080,
        proxy: {
            "/api": {
                target: "http://localhost:8000/api",
                changeOrigin: true,
                pathRewrite: {
                    "^/api": "",
                },
            },
        },
    },
});
