<template>
  <the-navbar></the-navbar>
  <the-header></the-header>
  <the-footer></the-footer>
</template>
<script>
import TheHeader from './components/shared/TheHeader'
import TheFooter from './components/shared/TheFooter'
import TheNavbar from "@/components/shared/TheNavbar";

export default {
  name: 'App',
  components: {
    TheNavbar,
    'TheHeader': TheHeader,
    'TheFooter': TheFooter
  }
}

</script>
<style lang="scss">
@import "../scss/style.scss";

#app {
  height: 100vh;
  display: grid;
  grid-template-areas:'. . .'
  '. header .'
          '. main .'
          'footer footer footer';
  grid-template-rows: 3rem max-content 1fr max-content;
  grid-template-columns: 1fr minmax(400px, 1024px) 1fr;
  background: $color-light-200;

  @media only screen and (max-width: 600px){
  grid-template-areas:'.'
          'messages'
          'header'
          'main'
          'footer';
  grid-template-columns: 1fr;
  grid-template-rows: 6rem max-content max-content 1fr 6rem;

  }
}

#navbar {
  @include shadow-2;
  z-index: 90;
  grid-area: messages;
  background-color: $color-light-100;
}

header {
  @include shadow-2;
  grid-area: header;
  background-color: $color-danger;
  z-index: 80;

}


main {
  @include shadow-2;
  z-index: 70;
  grid-area: main;
  background-color: $color-light-100;
  padding: .5rem;
}

footer {
  @include shadow-5;
  z-index: 80;
  grid-area: footer;
  background-color: $color-light-100;
}

</style>