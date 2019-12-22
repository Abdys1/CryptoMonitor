<template>
    <router-view :key="$route.fullPath">

    </router-view>
</template>

<script>
    import Login from "./Login";
    import Registration from "./Registration";

     const routes = [
         {path: "/login", component: Login},
         {path: "/registration", component: Registration}
     ]

    export default {
        name: "Authentication",
        beforeCreate() {
            this.$router.addRoutes(routes)
            this.$router.push("/login")
        }
    }
</script>

<style scoped>

</style>