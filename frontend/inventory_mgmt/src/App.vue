<template>
  <TheHeader>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link :to="{name: 'equipments'}">Equipments</router-link>
  </div>
    </TheHeader>
  <router-view/>
  <TheFooter></TheFooter>
</template>
<script>
import TheHeader from './components/TheHeader'
import TheFooter from './components/TheFooter'

export default {
  name: 'home',
  components: {
    'TheHeader': TheHeader,
    'TheFooter': TheFooter
  }
}

</script>