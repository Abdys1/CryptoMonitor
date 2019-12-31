<template>
    <v-app>
        <TransactionCreator></TransactionCreator>
    </v-app>
</template>

<script>
    import TransactionCreator from "./TransactionCreator";
    export default {
        name: "CryptoMonitor",
        components: {TransactionCreator},
        beforeCreate() {
            if(this.$session.exists()) {
                this.$http.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem("token")
            }
            else {
                this.$router.push("/")
                this.$http.defaults.headers.common['Authorization'] = "";
                localStorage.removeItem("token")
            }
        }
    }
</script>

<style scoped>

</style>