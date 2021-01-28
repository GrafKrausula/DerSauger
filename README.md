# DerSauger

Nach dem ruterladen von "Der-Sauger-main", bitte "Der Sauger" extrahieren und die weiteren schritte der darin befindlichen README folgen. 


TODO:

Beim speichercheck (um den erfolgreichen download zu testen) auch ein fileanzahlcheck hinzufügen, da sich die größe des Ordner auch durch parralle downloads verändern kann
ohne das neue files erstellt werden, was zu einem falsch positiven download-response und damit zu einem nicht dowload führt.


Button für Check Update schreiben.
Vergleicht eine irgendwo als Text hinterlegte Versionsnummer im "Der Sauger" Ordner, mit einer im repository hinterlegten Versionsnummer und lädt sie dann runter.


Updater.py in der Sauger schreiben, welcher die zip hier aus dem repository in temp ordner zieht, dann den alten "Der Sauger" Order löscht und durch den neu-heruntergeladenen aus dem temp-ordner Ersetzt. Temp ordner wird dann gelöscht.


Vernünftige uninstall bat mit löschung und detektierung aller ffmpeg und youtube-dl Pfadvariablen
Installer bat: Detektierung, ob pfadvariablen wirklich eingefügt wurden



Hotkeys für verschiede formate einführen:

STRG+ALT+3 -> MP3
STRG+ALT+W -> WAV
STRG+ALT+M -> MKV
STRG+ALT+4 -> MP4


"Initialize the extension 
Listen to the runtime.onInstalled event to initialize an extension on installation. Use this event to set a state or for one-time initialization, such as a context menu.

chrome.runtime.onInstalled.addListener(function() {
  chrome.contextMenus.create({
    "id": "sampleContextMenu",
    "title": "Sample Context Menu",
    "contexts": ["selection"]
  });
}); "

