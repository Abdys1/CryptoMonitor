<template>
    <h1>Kriptomonitor</h1>
</template>

<script>
    export default {
        name: "CryptoMonitor",
        methods: {
            logout: function () {
                this.$session.destroy()
                this.$router.push("/")
            }
        },
        beforeCreate() {
          if(!this.$session.exists()) {
              this.$router.push("/login")
          }
        }
    }
</script>

<style scoped>

</style>