import './assets/main.css'

import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faPause,
  faPlay,
  faExpand,
  faCompress,
  faArrowsToDot
} from '@fortawesome/free-solid-svg-icons'
import { isMobile } from '@/state'

library.add(faPause, faPlay, faExpand, faCompress, faArrowsToDot)

const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon)

isMobile.value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
  navigator.userAgent
)

app.use(router)

app.mount('#app')
