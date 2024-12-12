let port = null;
let connected = false;

let format = null;
let convert = null;
let downloadpath = null;
let convertpath = null;

function onNativeMessage(message) {
  console.log("Received message: " + JSON.stringify(message));
}

function onDisconnected() {
  console.log("Disconnected from native app.");
  port = null;
  connected = false;
}

async function connect() {
  connected = true;
  const hostName = "com.google.chrome.dersauger.echo";
  console.log("Connecting to native messaging host: " + hostName);
  port = browser.runtime.connectNative(hostName);
  port.onMessage.addListener(onNativeMessage);
  port.onDisconnect.addListener(onDisconnected);
}

async function sendNativeMessage(message) {
  if (port) {
    port.postMessage(message);
    console.log("Sent message: " + JSON.stringify(message));
  } else {
    console.error("Port is not connected!");
  }
}

async function send(message) {
  console.log("Python script running: " + connected);
  if (!connected) {
    await connect();
  }
  await sendNativeMessage(message);
}

async function sendPreferences() {
  let items = await browser.storage.sync.get(["favouriteFormat", "wantsConvert", "CNVtpath", "DLpath"]);
  format = items.favouriteFormat;
  convert = items.wantsConvert;
  downloadpath = items.DLpath;
  convertpath = items.CNVtpath;

  let message = { format, convert, downloadpath, convertpath };
  await send(message);
  await getAndSendUrl();
}

async function sendFixedPreferences(command) {
  let items = await browser.storage.sync.get(["favouriteFormat", "wantsConvert", "CNVtpath", "DLpath"]);
  format = command;
  convert = items.wantsConvert;
  downloadpath = items.DLpath;
  convertpath = items.CNVtpath;

  let message = { format, convert, downloadpath, convertpath };
  await send(message);
  await getAndSendUrl();
}

async function invokeUpdate() {
  await send("invokeUpdate");
}

async function getAndSendUrl() {
  let tabs = await browser.tabs.query({ active: true, currentWindow: true });
  let url = tabs[0].url;
  console.log("Current URL: ", url);
  let message = { "url": url };
  await send(message);
}

browser.commands.onCommand.addListener(async function(command) {
  if (command === "toggle") {
    await sendPreferences();
  } else if (["wav", "mp3", "mp4"].includes(command)) {
    await sendFixedPreferences(command);
  }
});

browser.action.onClicked.addListener(async function (tab) {
  await sendPreferences();
});

browser.runtime.onMessage.addListener(async (request, sender) => {
  if (request.Message === "UPDATE") {
    await invokeUpdate();
  }
});
