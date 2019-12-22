<template>
    <v-container>
        <v-row>
            <v-col>
                <v-alert
                    border="top"
                    colored-border
                    type="info"
                    elevation="2"
                    v-show="error !== ''"
                    transition="scale-transition"
                >
                    {{ error }}
                </v-alert>
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
                        :rules="passwordRules"
                        required
                    ></v-text-field>
                    <v-text-field
                        v-model="passwordVerify"
                        type="password"
                        label="Jelszó megerősítés"
                        :rules="verifyRules"
                        required
                    ></v-text-field>
                </v-form>
                  <v-btn
                    @click="signUp"
                >
                    Regisztráció
                </v-btn>
                <InfoModal
                        title="Sikeres regisztráció"
                        message="Mielőtt bejelentkeznél, kérlek aktiváld a profilodat!"
                        v-model="dialog"
                        @verify-message="redirectLoginPage"
                ></InfoModal>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import axios from 'axios'
    import InfoModal from "./InfoModal";

    export default {
        name: "Registration",
        components: {InfoModal},
        data: function() {
            return {
                valid: false,
                error: "",
                username: "",
                usernameRules: [
                    v => !!v || "Kérem adjon meg egy felhasználónevet!",
                    v => (v && v.length > 4) || "Kérem adjon meg legalább 4 karakter hosszú felhasználónevet!",
                    v => (v && v.length < 16) || "Túl hosszú felhasználónév!"
                ],
                email: "",
                emailRules: [
                    v => (!!v && /.+@.+\..+/.test(v)) || "Kérem adjon meg egy érvényes email címet!",
                ],
                password: "",
                passwordRules: [
                    v => (!!v && v.length > 6) || "Kérem adjon meg legalább 6 karakter hosszú jelszót!",
                    v => (!!v && v.length < 25) || "Túl hosszú jelszó!"
                ],
                passwordVerify: "",
                verifyRules: [
                    v => v === this.password || "Jelszavak nem egyeznek!"
                ],
                dialog: false
            }
        },
        methods: {
            signUp: function () {
                if(this.$refs.form.validate()) {
                    axios.post("/auth/registration", {
                        username: this.username,
                        email: this.email,
                        password: this.password
                    }).then(response => {
                        if(response.status === 200) {
                            const errors = JSON.parse(response.data)
                            this.getFirstError(errors)
                        }
                        else if(response.status === 201) {
                            this.$refs.form.reset()
                            this.dialog = true
                        }
                    });
                }
            },
            getFirstError: function (errors) {
                if(errors.hasOwnProperty("username"))
                    this.error = errors.username[0]
                else if(errors.hasOwnProperty("email"))
                    this.error = errors.email[0]
            },
            redirectLoginPage: function (event, value) {
                window.console.log(value)
                this.$router.push("/login")
            }
        }
    }
</script>

<style scoped>

</style>