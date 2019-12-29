<template>
    <v-app>
        <TransactionCreator></TransactionCreator>
    </v-app>
</template>

<script>
    import TransactionCreator from "./TransactionCreator";
    export default {
        name: "CryptoMonitor",
        components: {TransactionCreator}
    }
</script>

<style scoped>

</style>