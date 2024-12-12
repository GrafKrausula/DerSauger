async function save_options() {
    const format = document.getElementById('format').value;
    const convert = document.getElementById('convert').checked;
    const downloadpath = document.getElementById('downloadpath').value;
    const convertpath = document.getElementById('convertpath').value;
  
    await browser.storage.sync.set({
      favouriteFormat: format,
      wantsConvert: convert,
      CNVtpath: convertpath,
      DLpath: downloadpath
    });
  
    let status = document.getElementById('status');
    status.textContent = 'Status: Options saved.';
    setTimeout(function() {
      status.textContent = 'Status: ';
    }, 750);
  }
  
  async function restore_options() {
    await browser.storage.sync.set({
      favouriteFormat: 'wav',
      wantsConvert: false,
      CNVtpath: "C:",
      DLpath: "C:"
    });
  
    await get_options(true);
    let status = document.getElementById('status');
    status.textContent = 'Status: Options Reset.';
    setTimeout(function() {
      status.textContent = 'Status: ';
    }, 1050);
  }
  
  async function restore_options_prttyp() {
    await browser.storage.sync.set({
      favouriteFormat: 'wav',
      wantsConvert: true,
      CNVtpath: "E:/RENDER OUTPUT",
      DLpath: "E:/Runterladungen!"
    });
  
    await get_options(true);
    let status = document.getElementById('status');
    status.textContent = 'Status: Options Reset.';
    setTimeout(function() {
      status.textContent = 'Status: ';
    }, 1050);
  }
  
  async function get_options(isFromReset=false) {
    let items = await browser.storage.sync.get(["favouriteFormat", "wantsConvert", "CNVtpath", "DLpath"]);
    
    let status = document.getElementById('status');
  
    // If no items found or incomplete, restore defaults
    if (!items || items.favouriteFormat === undefined) {
      status.textContent = "Status: No options found. Restoring options.";
      await restore_options();
      return;
    }
  
    document.getElementById('format').value = items.favouriteFormat;
    document.getElementById('convert').checked = items.wantsConvert || false;
    document.getElementById('convertpath').value = items.CNVtpath || "C:";
    document.getElementById('downloadpath').value = items.DLpath || "C:";
  
    if (!isFromReset) {
      status.textContent = 'Status: Options Loaded.';
      setTimeout(function() {
        status.textContent = 'Status: ';
      }, 10550);
    }
  }
  
  async function update_script() {
    alert("function update_script()");
    // Send message to background
    await browser.runtime.sendMessage({Message: "UPDATE"});
    let status = document.getElementById('status');
    status.textContent = 'Status: Update invoked. Close this page and wait.';
  }
  
  document.addEventListener('DOMContentLoaded', () => { get_options(); });
  document.getElementById('reset').addEventListener('click', restore_options);
  document.getElementById('save').addEventListener('click', save_options);
  document.getElementById('prttyp').addEventListener('click', restore_options_prttyp);
  document.getElementById('UPDATE').addEventListener('click', update_script);
  