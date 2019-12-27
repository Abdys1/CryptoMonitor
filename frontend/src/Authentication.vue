<template>
    <v-app>
         <v-container class="content" fluid>
            <v-row
                    align="center"
                    justify="center"
                    style="height: 100%">
                <v-col lg="4">
                    <v-card
                            class="auth-box"
                            elevation="13">
                        <v-card-actions class="justify-center">
                            <v-img src="./assets/bitcoin.png" width="160px" height="160px"/>
                            <router-view>

                            </router-view>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-app>
</template>

<script>
    export default {
        name: "Authentication",
        beforeCreate() {
            if(this.$session.exists()) {
                this.$session.destroy()
            }

            if(this.$router.currentRoute.path === "/")
                this.$router.push("/login")
        },
    }
</script>

<style scoped>
    .content {
        background: url("./assets/login_background.jpg");
        background-repeat: no-repeat;
        background-size: cover;
        height: 100%;
    }

    .auth-box {
        background: black;
    }
</style>