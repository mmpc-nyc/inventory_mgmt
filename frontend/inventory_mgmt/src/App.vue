<template>
  <TheHeader>
    <div id="nav">
      <router-link to="/">Home</router-link>
      <router-link :to="{name: 'my_equipment'}">Equipments</router-link>
      <router-link :to="{name: 'my_orders'}">Orders</router-link>
    </div>
  </TheHeader>
  <router-view/>
  <TheLogin></TheLogin>
  <TheFooter></TheFooter>
</template>
<script>
import TheHeader from './components/shared/TheHeader'
import TheFooter from './components/shared/TheFooter'
import TheLogin from './views/auth/TheAuthentication'

export default {
  name: 'home',
  components: {
    'TheLogin': TheLogin,
    'TheHeader': TheHeader,
    'TheFooter': TheFooter
  }
}

</script>