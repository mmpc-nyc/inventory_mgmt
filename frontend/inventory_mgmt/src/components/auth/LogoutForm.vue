<template>
  <form v-if="render" @submit.prevent="logout">
    <button>Logout</button>
  </form>
</template>

<script>
export default {
  name: "LogoutForm",
  props: ["loggedIn"],
  computed: {
    render() {
      console.log(this.loggedIn)
      return this.loggedIn;
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logout')
    }
  }
}
</script>