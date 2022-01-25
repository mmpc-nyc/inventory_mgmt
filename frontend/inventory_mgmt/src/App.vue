<template>
  <the-top-nav-bar>
  </the-top-nav-bar>
  <router-view/>
</template>
<script>

import TheTopNavBar from "@/components/shared/TheTopNavBar";
import EventBus from "@/common/EventBus";
import AuthService from "@/services/AuthService";

export default {
  name: 'App',
  components: {TheTopNavBar},
  methods: {
    logout() {
      this.$store.dispatch('auth/logout')
      AuthService.logout()
    }
  },
  mounted() {
    EventBus.on("logout", () => {
      console.log("logout called")
      this.logout()
    })
  },
  beforeUnmount() {
    EventBus.remove("logout")
  }
}

</script>
<style lang="scss">
@import "@/scss/style.scss";


#app {
  display: grid;
  grid-template-areas: "top-nav-bar top-nav-bar top-nav-bar"
  "side-nav-bar main .";
  justify-content: center;
  grid-template-rows: auto 1fr;
  grid-template-columns: 30ch minmax(700px, 1440px) auto;
}

main {
  grid-area: main;
  height: 100vh;
}

.top-nav-bar {
  grid-area: top-nav-bar
}

.side-nav-bar {
  grid-area: side-nav-bar;
  max-width: 30ch;
}

</style>