import { createApp } from 'vue';
import App from './App.vue';
import SmartContractDetector from './SmartContractDetector.vue';

const app = createApp(SmartContractDetector);
app.component('smart-contract-detector', SmartContractDetector);
app.mount('#app');
