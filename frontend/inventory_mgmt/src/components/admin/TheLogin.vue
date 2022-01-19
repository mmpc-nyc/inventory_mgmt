<template>
  <form v-if="!loggedIn" @submit.prevent="login">
    {{loggedIn}}
    <h1>Login Form</h1>
    <input v-model="username" placeholder="username"/>
    <input v-model="password" placeholder="password" type="password">
    <button type="submit">Login</button>
  </form>
  <form v-else @submit.prevent="logout" e>
    <button>Logout</button>
  </form>
</template>

<script>
export default {
  name: "TheLogin.vue",
  data() {
    return {username: '', password: ''}
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.loggedIn;
    }
  },
  methods: {
    login() {
      this.$store.dispatch('auth/login', {username: this.username, password: this.password})
    },
    logout() {
      this.$store.dispatch('auth/logout')
    }
  }
}
</script>