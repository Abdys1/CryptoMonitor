<template>
  <v-row>
    <v-dialog v-model="show" max-width="290">
      <v-card style="background-color: black">
        <v-card-title class="headline">{{ title }}</v-card-title>

        <v-card-text>
          {{ message }}
        </v-card-text>

        <v-card-actions>
          <v-btn color="green darken-1" text @click="close">
            Értettem!
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: "InfoModal",
  props: {
    title: String,
    message: String,
    value: Boolean
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      }
    }
  },
  methods: {
    close() {
      this.$emit("verify-message", "Sikerersen bezártad az ablakot!");
    }
  }
};
</script>

<style scoped></style>
