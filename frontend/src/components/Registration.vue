<template>
    <v-form ref="form"
            v-model="valid"
            lazy-validation>
        <v-text-field
            v-model="username"
            label="Felhasználónév"
            :rules="usernameRules"
            required
        ></v-text-field>
        <v-text-field
            v-model="email"
            label="Email cím"
            :rules="emailRules"
            required
        ></v-text-field>
        <v-text-field
            v-model="password"
            type="password"
            label="Jelszó"
            required
        ></v-text-field>
        <v-text-field
            v-model="passwordVerify"
            type="password"
            label="Jelszó megerősítés"
            :rules="verifyRules"
            required
        ></v-text-field>
        <v-btn
            @click="signUp"
        >
            Regisztráció
        </v-btn>
    </v-form>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "Registration",
        data: function() {
            return {
                valid: false,
                username: "",
                usernameRules: [
                    v => !!v || "Kérem adjon meg egy felhasználónevet!",
                    v => (v && v.length > 4) || "Kérem adjon meg legalább 4 karakter hosszú felhasználónevet!"
                ],
                email: "",
                emailRules: [
                  v => (!!v && /.+@.+\..+/.test(v)) || "Kérem adjon meg egy érvényes email címet!",
                ],
                password: "",
                passwordVerify: "",
                verifyRules: [
                    v => v === this.password || "Jelszavak nem egyeznek!"
                ],
                errors: []
            }
        },
        methods: {
            signUp: function () {
                if(this.$refs.form.validate()) {
                    axios.post("/auth/registration", {
                        username: this.username,
                        email: this.email,
                        password: this.password
                    }).then(response => window.console.log(JSON.parse(response.data)["username"][0]))
                }
            }
        }
    }
</script>

<style scoped>

</style>