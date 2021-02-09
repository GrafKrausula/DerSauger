// Saves options to chrome.storage
//chrome.downloads.showDefaultFolder()

chrome.runtime.onInstalled.addListener(function(details){
    if(details.reason == "install"){
      restore_options()
        //call a function to handle a first install
    }else if(details.reason == "update"){
        //call a function to handle an update
    }
});

function save_options() {
  var format = document.getElementById('format').value;
  var convert = document.getElementById('convert').checked;

  var downloadpath = document.getElementById('downloadpath').value;
  var convertpath = document.getElementById('convertpath').value;
  chrome.storage.sync.set({
    favouriteFormat: format, //das rote ist der speicherkey, das weißte die zu speichernde variable
    wantsConvert: convert,
    CNVtpath: convertpath,
    DLpath: downloadpath
  }, function() {
    // Update status to let user know options were saved.
    var status = document.getElementById('status');
    status.textContent = 'Status: Options saved.';
    setTimeout(function() {
      status.textContent = 'Status: ';
    }, 750);
  });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
  // Use default value color = 'red' and likesColor = true.
  chrome.storage.sync.set({
    favouriteFormat: 'wav',
    wantsConvert: false,
    CNVtpath: "C:",
    DLpath: "C:/Users/Maddin/Downloads"
  }, function(items) {
    document.getElementById('format').value = items.favouriteFormat;
    document.getElementById('convert').checked = items.wantsConvert;
    document.getElementById('convertpath').value = items.CNVtpath;
    document.getElementById('downloadpath').value = items.DLpath;
    var status = document.getElementById('status');
    status.textContent = 'Status: Options Reset.';
    setTimeout(function() {
      //chrome.extension.getBackgroundPage().window.location.reload()
      status.textContent = 'Status: ';
    }, 1050);
  });
  get_options()
}

function get_options() {
  // Use default value color = 'red' and likesColor = true.
  chrome.storage.sync.get({
    favouriteFormat: format, //das rote ist der speicherkey, das weißte die zu speichernde variable
    wantsConvert: convert,
    CNVtpath: convertpath,
    DLpath: downloadpath
  }, function(items) {
    document.getElementById('format').value = items.favouriteFormat;
    document.getElementById('convert').checked = items.wantsConvert;
    document.getElementById('convertpath').value = items.CNVtpath;
    document.getElementById('downloadpath').value = items.DLpath;
    var status = document.getElementById('status');
    status.textContent = 'Status: Options Loaded.';
    setTimeout(function() {
      status.textContent = 'Status: ';
    }, 1550);
  });
}

function restore_options_KRSE() {
  // Use default value color = 'red' and likesColor = true.
  chrome.storage.sync.set({
    favouriteFormat: 'wav',
    wantsConvert: true,
    CNVtpath: "E:/RENDER OUTPUT",
    DLpath: "E:/Runterladungen!"
  }, function(items) {
    document.getElementById('format').value = items.favouriteFormat;
    document.getElementById('convert').checked = items.wantsConvert;
    document.getElementById('convertpath').value = items.CNVtpath;
    document.getElementById('downloadpath').value = items.DLpath;
    var status = document.getElementById('status');
    status.textContent = 'Status: Options Reset.';
    setTimeout(function() {
      //chrome.extension.getBackgroundPage().window.location.reload()
      status.textContent = 'Status: ';
    }, 1050);
  });
  get_options()
}

function update_script() {
  alert("function update_script()")
  chrome.runtime.sendMessage({Message: "UPDATE"})
  var status = document.getElementById('status');
  status.textContent = 'Status: Update invoked. Close this page and wait.';
}

document.addEventListener('DOMContentLoaded', get_options);
document.getElementById('reset').addEventListener('click',
    restore_options);
document.getElementById('save').addEventListener('click',
    save_options);
document.getElementById('KRSE').addEventListener('click',
    restore_options_KRSE);
document.getElementById('UPDATE').addEventListener('click',
    update_script);
