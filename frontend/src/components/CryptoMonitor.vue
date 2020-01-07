<template>
    <v-app>
        <TransactionCreator @created="getUsersTransactions"></TransactionCreator>
        <TransactionTable :items="transactions"></TransactionTable>
    </v-app>
</template>

<script>
    import TransactionCreator from "./TransactionCreator";
    import TransactionTable from "./TransactionTable";

    export default {
        name: "CryptoMonitor",
        components: {TransactionTable, TransactionCreator},
        data: function() {
            return {
                transactions: []
            }
        },
        methods: {
            getUsersTransactions: function() {
                this.$http.get("/api/transaction/")
                    .then(response => this.transactions = response.data)
            }
        },
        beforeCreate() {
            if(this.$session.exists()) {
                this.$http.defaults.headers.common["Authorization"] = "Token " + localStorage.getItem("token")
            }
            else {
                this.$http.defaults.headers.common["Authorization"] = ""
                localStorage.removeItem("token")
                this.$router.push("/")
            }
        },
        mounted() {
            this.getUsersTransactions()
        }
    }
</script>

<style scoped>

</style>