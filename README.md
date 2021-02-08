# DerSauger

Nach dem ruterladen von "Der-Sauger-main", bitte "Der Sauger" extrahieren und die weiteren schritte der darin befindlichen README folgen. 


TODO:

Updater überarbeiten:

	Vergleicht eine irgendwo als Text hinterlegte Versionsnummer im "Der Sauger" Ordner, mit einer im repository hinterlegten Versionsnummer und lädt sie dann runter.

	timouts aus bat dateien raushauen

	Updater.py zu einer DATEI ändern, welche wie der host über ein cmd command "python {pfad}" aufgerufen wird um versehentliches updaten zu vermeiden

Uninstaller überarbeiten:

	Vernünftige uninstall bat mit löschung und detektierung aller ffmpeg und youtube-dl Pfadvariablen



Beim speichercheck (um den erfolgreichen download zu testen) auch ein fileanzahlcheck hinzufügen, da sich die größe des Ordner auch durch parralle downloads verändern kann
ohne das neue files erstellt werden, was zu einem falsch positiven download-response und damit zu einem nicht dowload führt.



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
