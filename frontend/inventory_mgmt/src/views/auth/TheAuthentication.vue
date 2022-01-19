<template>
  <login-form :loggedIn="loggedIn"></login-form>
  <logout-form :loggedIn="loggedIn"></logout-form>
</template>

<script>
import LoginForm from "../../components/auth/LoginForm";
import LogoutForm from "../../components/auth/LogoutForm";

export default {
  name: "TheAuthentication",
  components: {LogoutForm, LoginForm},
  computed: {
    loggedIn() {
      return this.$store.state.auth.loggedIn;
    }
  },
}
</script>