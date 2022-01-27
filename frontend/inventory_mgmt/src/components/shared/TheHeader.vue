<template>
  <header id="header">
    <h1 :class="$tt('headline3')">{{ $route.meta.title }}</h1>
  </header>
</template>
<script>
export default {
  name: 'TheHeader',
}
</script>