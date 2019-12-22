<template>
   <v-container>
       <v-row>
           <v-col>
               <v-form ref="form">
                   <v-text-field
                           v-model="username"
                           label="Felhasználónév"
                           required>
                   </v-text-field>
                   <v-text-field
                           v-model="password"
                           label="Jelszó"
                           type="password"
                           required
                   ></v-text-field>
                   <v-btn
                   >Bejelentkezés</v-btn>
               </v-form>
               <router-link to="/registration">Regisztráció</router-link>
           </v-col>
       </v-row>
   </v-container>
</template>

<script>
    export default {
        name: "Login",
        data: function () {
            return {
                username: "",
                password: ""
            }
        }
    }
</script>

<style scoped>

</style>