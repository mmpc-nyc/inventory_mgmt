<template>
  <nav id="navbar" class="navbar">
    <router-link :class="{home:true}" to="/">Home</router-link>
    <router-link :class="{link:true}" :to="{name: 'admin'}">Admin</router-link>
    <TheLogin></TheLogin>
  </nav>
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
<style lang="scss" scoped>
@import "/scss/variables";

.navbar {
  @include shadow-1;
  display: grid;
  grid-template-areas: 'home links userinfo';
  grid-template-columns: 1fr minmax(600px, 1440px) 1fr;
  align-content: center;
  background-color: $color-light-100;
  position: fixed;
  width: 100%;
  top: 0;
  height: 3rem;
  z-index: 100;

  @media only screen and (max-width: 600px) {
    grid-template-areas: 'home userinfo'
    'links links';
    height: 6rem;

  }

  a {
    color: $color-dark-100;
    transition: color ease .25s;
    padding: 1rem;

  &.active {
    color: red;
  }

  &:hover {
    color: $color-danger;
  }
  }
}

.home {
  grid-area: home;
}

.links {
  grid-area: links;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 2em;
}

.user-info {
  grid-area: userinfo;
  display: flex;
  flex-direction: row;
  justify-content: end;
  align-items: center;
}
</style>