<template>
  <ui-top-app-bar short nav-id="top-app-bar" content-selector="main">
    <template v-slot:toolbar>
      <router-link to="/" custom v-slot="{navigate, isActive}">
        <ui-button raised :class="{active: isActive}" @click="navigate">Home</ui-button>
      </router-link>
      <router-link :to="{name:'admin'}" custom v-slot="{navigate, isActive}">
        <ui-button raised :class="{active: isActive}" @click="navigate">Admin</ui-button>
      </router-link>
      <the-user-info></the-user-info>
    </template>
  </ui-top-app-bar>
  <router-view/>
</template>
<script>

import TheUserInfo from "@/components/shared/TheUserInfo";
export default {
  name: 'App',
  components: {TheUserInfo}
}

</script>
<style lang="scss">
@import "../scss/style.scss";

#app {
  height: 100vh;
  display: grid;
  grid-template-areas:
  '. header .'
          '. main .'
          'footer footer footer';
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 1fr minmax(400px, 1024px) 1fr;
}

header {
  grid-area: header;
  z-index: 80;

}

main {
  z-index: 70;
  grid-area: main;
}

footer {
  z-index: 80;
}

</style>