var port = null;
var connected = false;

var format = null;
var convert = null;
var downloadpath = null;
var convertpath = null;

var getKeys = function(obj){
   var keys = [];
   for(var key in obj){
      keys.push(key);
   }
   return keys;
}


function onNativeMessage(message) {
  console.log("Received message: <b>" + JSON.stringify(message) + "</b>");
}

function onDisconnected() {
  console.log("Failed to connect: " + chrome.runtime.lastError.message);
  port = null;
  connected = false;
}

async function connect() {
  connected = true;
  var hostName = "com.google.chrome.example.echo";
  console.log("Connecting to native messaging host <b>" + hostName + "</b>")
  port = chrome.runtime.connectNative(hostName);
  port.onMessage.addListener(onNativeMessage);
  port.onDisconnect.addListener(onDisconnected);
}

async function sendNativeMessage(message) {

  await port.postMessage(message);
  console.log("Sent message: <b>" + JSON.stringify(message) + "</b>");
}

async function send(message) {
  console.log("Python script running: " + connected);
  if(!connected){
    await connect();
  }
  await sendNativeMessage(message);
}

async function sendPreferences() {
  // Use default value color = 'red' and likesColor = true.
  chrome.storage.sync.get([
    "favouriteFormat", //das rote ist der speicherkey, das weißte die zu speichernde variable
    "wantsConvert",
    'CNVtpath',
    'DLpath'],
    async function(items) {
    format = items.favouriteFormat;
    convert = items.wantsConvert;
    downloadpath = items.DLpath;
    convertpath = items.CNVtpath;
    message = {format, convert, downloadpath, convertpath};
    await send(message)
    getAndSendUrl()
  });
}

async function invokeUpdate(){
  await send("invokeUpdate")
}

async function getAndSendUrl(){
  chrome.tabs.query({active: true, currentWindow: true}, async tabs => {
    var url = tabs[0].url;
    console.log(url); //Die konsole beweißt, die url wird richtig abgerufen
    message = {"url": url}; //Hier url von momentanen tab
    await send(message)

  });
}

chrome.commands.onCommand.addListener(async function(command) {
  if(command == "toggle"){
    sendPreferences() //sendet url und präferenzen
  }
});

chrome.browserAction.onClicked.addListener(async function (tab) {
  //chrome.tabs.create({url: 'main.html'})
  sendPreferences() //sendet url und präfernezen

})


chrome.runtime.onMessage.addListener( function(request,sender,sendResponse)
{
    if( request.Message === "UPDATE" ){
      invokeUpdate()
    }
})
