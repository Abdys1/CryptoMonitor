<template>
  <v-app>
      <Registration></Registration>
  </v-app>
</template>

<script>
import Registration from "./components/Registration";

export default {
  name: 'App',

  components: {
    Registration,
  },

  data: () => ({
    //
  })
};
</script>
