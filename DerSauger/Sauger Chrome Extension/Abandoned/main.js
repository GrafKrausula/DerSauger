// Copyright 2013 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

var port = null;

var getKeys = function(obj){
   var keys = [];
   for(var key in obj){
      keys.push(key);
   }
   return keys;
}


function appendMessage(text) {
  document.getElementById('response').innerHTML += "<p>" + text + "</p>";
}

function updateUiState() {
  if (port) {
    document.getElementById('connect-button').style.display = 'none';
    document.getElementById('input-text').style.display = 'block';
    document.getElementById('send-message-button').style.display = 'block';
  } else {
    document.getElementById('connect-button').style.display = 'block';
    document.getElementById('input-text').style.display = 'none';
    document.getElementById('send-message-button').style.display = 'none';
  }
}

function sendNativeMessage() {
  chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url;
    // use `url` here inside the callback because it's asynchronous!
  });

  message = {"url": url}; //Hier url von momentanen tab
  port.postMessage(message);
  //appendMessage("Sent message: <b>" + JSON.stringify(message) + "</b>");
}

function onNativeMessage(message) {
  alert("Received message: <b>" + JSON.stringify(message) + "</b>");
}

function onDisconnected() {
  //window.alert("The host has quit")
  alert("Failed to connect: " + chrome.runtime.lastError.message);
  port = null;
  //updateUiState();
}

function connect() {
  var hostName = "com.google.chrome.example.echo";
  alert("Connecting to native messaging host <b>" + hostName + "</b>")
  port = chrome.runtime.connectNative(hostName);
  port.onMessage.addListener(onNativeMessage);
  //updateUiState();
  port.onDisconnect.addListener(onDisconnected);
  //updateUiState();
}

connect();
sendNativeMessage();
