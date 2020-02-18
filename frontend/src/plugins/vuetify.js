import Vue from "vue";
import Vuetify from "vuetify/lib";

import colors from "vuetify/lib/util/colors";
import "@mdi/font/css/materialdesignicons.css"; // Ensure you are using css-loader

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: true,
    themes: {
      dark: {
        primary: colors.yellow.darken1,
        second: "#000000",
        accent: colors.yellow.darken1,
        error: colors.red.accent3,
        anchor: colors.yellow.darken1,
        info: colors.yellow.darken1,
        success: colors.yellow.darken1,
        warning: "#ffbb33"
      },
      options: {
        customProperties: true
      }
    },
    icons: {
      iconfont: "mdi" // default - only for display purposes
    }
  }
});
