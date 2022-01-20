<template>
  <form v-if="loggedIn" @submit.prevent="logout">
    <button>Logout</button>
  </form>
</template>

<script>
export default {
  name: "LogoutForm",
  props: ["loggedIn"],
  methods: {
    logout() {
      this.$store.dispatch('auth/logout')
    },
  }
}
</script>