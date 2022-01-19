<template>
  <div id="qr-scanner"></div>
</template>
<script>
import {Html5QrcodeScanner} from 'html5-qrcode'

export default {
  name: "QrScanner",
  props: {
    qrbox: {
      type: Number,
      default: 250
    },
    fps: {
      type: Number,
      default: 10
    },
  },
  mounted() {
    const config = {
      fps: this.fps,
      qrbox: this.qrbox,
    };
    const qrScanner = new Html5QrcodeScanner('qr-scanner', config);
    qrScanner.render(this.onScanSuccess);
  },
  methods: {
    onScanSuccess(decodedText, decodedResult) {
      this.$emit('onScanSuccess', {decodedText: decodedText, decodedResult: decodedResult});
    }
  }
}
</script>