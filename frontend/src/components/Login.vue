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
          >{{ error }}</v-alert
        >
        <v-form ref="form">
          <v-text-field v-model="username" label="Felhasználónév" required>
          </v-text-field>
          <v-text-field
            v-model="password"
            label="Jelszó"
            type="password"
            required
          ></v-text-field>
        </v-form>
        <v-layout row wrap>
          <v-layout>
            <p>
              Még nem regisztráltál?
              <router-link class="link" to="/registration"
                >Regisztráció</router-link
              >
            </p>
          </v-layout>
          <v-layout justify-end="">
            <v-btn @click="signIn">Bejelentkezés</v-btn>
          </v-layout>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Login",
  data: function() {
    return {
      username: "",
      password: "",
      error: ""
    };
  },
  methods: {
    signIn: function() {
      if (this.username !== "" && this.password !== "") {
        this.$authAPI
          .login(this.username, this.password)
          .then(token => {
            this.$session.start();
            this.$session.set("jwt", token);
            localStorage.setItem("token", token);
            document.cookie = "Authorization=Token " + token;
            this.$router.push("/monitor");
          })
          .catch(err => {
            this.error = err;
            localStorage.removeItem("token");
            document.cookie = "Authorization=";
          });
      } else {
        this.error = "Adjon meg egy érvényes felhasználónevet és/vagy jelszót!";
      }
    }
  }
};
</script>

<style scoped></style>
