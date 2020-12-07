import Vue from 'vue'
import App from './App.vue';
import { Icon } from 'leaflet';
import '@/assets/css/tailwind.css';
import 'leaflet/dist/leaflet.css';

import router from './router';
import store from './store';
import io from "socket.io-client"
// const socket = io('http://localhost:8003')
const socket = io('http://ec2-54-180-10-110.ap-northeast-2.compute.amazonaws.com:8003')

Vue.prototype.$socket = socket;
Vue.config.productionTip = false

// this part resolve an issue where the markers would not appear
delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')



