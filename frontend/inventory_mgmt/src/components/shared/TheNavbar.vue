<template>
  <ui-top-app-bar id="navbar" class="navbar" content-selector="main">
    <template #toolbar="{ toolbarItemClass }">
      <router-link :class="toolbarItemClass" to="/">Home</router-link>
      <router-link :class="toolbarItemClass" :to="{name: 'admin'}">Admin</router-link>
      <TheLogin :class="toolbarItemClass"></TheLogin>
    </template>
  </ui-top-app-bar>
  <router-view/>

</template>

<script>
import TheLogin from '@/views/auth/TheAuthentication'

export default {
  name: "TheNavbar",
  components: {
    'TheLogin': TheLogin
  }
}
</script>