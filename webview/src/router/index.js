import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'Index',
    component: () => import('@/pages/index/Index')
  },
  {
    path: '/sight',
    name: 'Sight',
    component: () => import('@/pages/sight/Sight')
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('@/pages/user/User')
  },
  {
    path: '/usercomment',
    name: 'UserComment',
    component: () => import('@/pages/usercomment/UserComment')
  },
  {
    path: '/analysis',
    name: 'TextAnalysis',
    component: () => import('@/pages/textanalysis/TextAnalysis')
  },
  {
    path: '/comment',
    name: 'Comment',
    component: () => import('@/pages/comment/Comment')
  },
  {
    path: '/crawler',
    name: 'Crawler',
    component: () => import('@/pages/crawler/Crawler')
  },
  {
    path: '/mycrawler',
    name: 'MyCrawler',
    component: () => import('@/pages/mycrawler/MyCrawler')
  },
  {
    path: '/wordcloudchart',
    name: 'WordCloudChart',
    component: () => import('@/pages/wordcloudchart/WordCloudChart')
  },
  {
    path: '/usergroup',
    name: 'UserGroup',
    component: () => import('@/pages/usergroup/UserGroup')
  }]
})
