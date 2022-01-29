<template>
  <the-top-nav-bar>
  </the-top-nav-bar>
  <the-header></the-header>
  <router-view/>
</template>
<script>

import TheTopNavBar from "@/components/shared/TheTopNavBar";
import TheHeader from "@/components/shared/TheHeader";

export default {
  name: 'App',
  components: {TheHeader, TheTopNavBar},
  methods: {
    logout() {
      this.$store.dispatch('auth/logout')
    }
  },

}

</script>
<style lang="scss">
@import "@/scss/style.scss";


#app {
  display: grid;
  grid-template-areas: "top-nav-bar top-nav-bar top-nav-bar"
  ". header ."
  "side-nav-bar main .";
  justify-content: center;
  grid-template-rows: auto 1fr;
  grid-template-columns: 30ch minmax(700px, 1440px) auto;
  gap: 1rem;
}

main {
  grid-area: main;
  height: 100vh;
}

.top-nav-bar {
  grid-area: top-nav-bar;
}

.side-nav-bar {
  grid-area: side-nav-bar;
  max-width: 30ch;
}

#header {
  grid-area: header;
}

</style>