const eventBus = {
  on(event, callback) {
    console.log(`Event added ${event}`);
    document.addEventListener(event, (e) => callback(e.detail));
  },
  dispatch(event, data) {
    console.log(`Event called ${event}`);
    document.dispatchEvent(new CustomEvent(event, { detail: data }));
  },
  remove(event, callback) {
    document.removeEventListener(event, callback);
  },
};

export default eventBus;
