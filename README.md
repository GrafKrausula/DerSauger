# DerSauger

Installieren:

1. python 3.8 oder höhere version im windows app store installieren

2. NUR Installer.py runterladen:

	2.1 -> https://raw.githubusercontent.com/GrafKrausula/DerSauger/main/installer.py aufrufen
	
	2.2 -> auf der in 2.1 aufgerufenen Seite STRG+S drücken

		-> falls vorhanden, das ".txt" aus dem speicherpfad löschen
	
	2.3 -> Installer.py an FINALEM Speicherort speichern, sprich in der Ordner in dem am ende die Chrome Extension "Der Sauger" installiert werden soll

!!!! WARNUNG !!!! Installer.py muss ZWINGEND dort ausgeführt werden wo ihr den Sauger gespeichert haben wollt. Also spätestens jetzt die Datei in FINALEN Speicherort schieben !!!!

++++++++ Während der installation werden alle offenen explorer.exe Fenster geschlossen +++++++++

3. Am FINALEN Speicherort Installer.py ausführen









######################################################################################################################################################################################

TODO:

Installer überarbeiten:

	registry suche nach schon vorhandenen saugern und diese deinstallieren
	
	suche nach schon vorhandenen, aber deplatzierten pfadvariablen und löschung derer


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
