<template>
  <form @submit.prevent="submitForm">
    <h1>Login Form</h1>
    <input v-model="username" placeholder="username" />
    <input v-model="password" placeholder="password" type="password">
    <button type="submit">Login</button>
  </form>
</template>

<script>
export default {
  name: "TheLogin.vue",
  data(){
    return {username: '', password: ''}
  },
  computed:{
    loggedIn() {
      return this.$store.auth.status.loggedIn;
    }
  },
  methods: {
    submitForm(event){
      this.$store.dispatch('auth/login', {username: this.username, password: this.password})
      console.log(event)
    }
  }
}
</script>