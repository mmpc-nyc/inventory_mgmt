import {Component} from "vue";
import {RouteLocationNormalized} from "vue-router";

export interface RouteConfig {
  path: string
  component?: Component
  name?: string
  components?: { [name: string]: Component }
  redirect?: string | Location | Function
  props?: boolean | Object | Function
  alias?: string | Array<string>
  children?: Array<RouteConfig>
  beforeEnter?: (to: RouteLocationNormalized, from: RouteLocationNormalized, next: Function) => void
  meta?: any

  // 2.6.0+
  caseSensitive?: boolean
  pathToRegexpOptions?: Object
}

export default RouteConfig