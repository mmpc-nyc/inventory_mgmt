function main(){
    let v = document.getElementById('scanner');
    let qrScanner = new f(v, result => console.log('decoded qr code:', result));
    qrScanner.start()
};