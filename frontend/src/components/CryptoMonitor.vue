<template>
    <h1>Kriptomonitor</h1>
</template>

<script>
    export default {
        name: "CryptoMonitor",
        beforeCreate() {
          if(!this.$session.exists()) {
              this.$router.push("/login")
          }
        }
    }
</script>

<style scoped>

</style>