<template>
  <form v-if="!loggedIn" @submit.prevent="login">
    <h1>Login Form</h1>
    <input v-model="username" placeholder="username"/>
    <input v-model="password" placeholder="password" type="password">
    <button type="submit">Login</button>
  </form>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {username: '', password: ''}
  },
  props: ["loggedIn"],
  methods: {
    login() {
      this.$store.dispatch('auth/login', {username: this.username, password: this.password})
    },
  }
}
</script>