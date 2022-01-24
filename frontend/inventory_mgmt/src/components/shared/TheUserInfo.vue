<template>
  <ui-form v-if="!loggedIn">
    <ui-form-field @keyup.enter="login">
      <ui-textfield v-model="username">Username</ui-textfield>
      <ui-textfield v-model="password" input-type="password">Password</ui-textfield>
      <ui-button raised type="submit" @click="login">Login</ui-button>
    </ui-form-field>
  </ui-form>
  <ui-form v-else>
    <ui-button raised @click="logout">Logout</ui-button>
  </ui-form>
</template>

<script>
import EventBus from "../../common/EventBus";

export default {
  name: "TheUserInfo",
  data() {
    return {username: '', password: ''}
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    }
  },
  methods: {
    login() {
      this.$store.dispatch('auth/login', {username: this.username, password: this.password})
    },
    logout() {
      console.log("Logout")
      EventBus.dispatch('logout')
    },
  }
}
</script>
<style scoped lang="scss">
ui-form{background: white;}
</style>