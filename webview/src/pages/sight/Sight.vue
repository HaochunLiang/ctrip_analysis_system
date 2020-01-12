<template>
  <div>
    <common-header></common-header>
    <sight-header></sight-header>
    <scroll-top></scroll-top>
    <bg-color></bg-color>
    <common-footer></common-footer>
  </div>
</template>

<script>
import CommonHeader from 'common/Header'
import ScrollTop from 'common/ScrollToTop'
import CommonFooter from 'common/Footer'
import BgColor from 'common/BgSet'
import SightHeader from './components/SightHeader'

export default {
  name: 'SightInfo',
  components: {
    CommonHeader,
    SightHeader,
    ScrollTop,
    CommonFooter,
    BgColor
  }
}

</script>

<style lang="scss" scoped>

</style>
