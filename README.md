# DerSauger

Installieren:

1. python 3.8 oder höhere version im "Microsoft Store" (App auf jedem Windows 10 Rechner vorhanden und durch suchfeld auffindbar) installieren

2. NUR Installer.py runterladen:

	2.1 -> https://raw.githubusercontent.com/GrafKrausula/DerSauger/main/installer.py aufrufen
	
	2.2 -> auf der in 2.1 aufgerufenen Seite STRG+S drücken

		-> 2.2.1 falls vorhanden, das ".txt" aus dem speicherpfad löschen
	
	2.3 -> Installer.py an FINALEM Speicherort speichern, sprich in der Ordner in dem am ende die Chrome Extension "Der Sauger" installiert werden soll

!!!! WARNUNG !!!! Installer.py muss ZWINGEND dort ausgeführt werden wo ihr den Sauger gespeichert haben wollt. Also spätestens jetzt die Datei in FINALEN Speicherort schieben !!!!

++++++++ Während der installation werden alle offenen explorer.exe Fenster geschlossen +++++++++


3. Am FINALEN Speicherort Installer.py ausführen, sprich doppelclick

	-> 3.1 falls die jetzt auf eurer Festplatte gespeicherte Datei NICHT AUSFÜHRBAR ist (also keine .py endung haben sollte) muss diese manuell hinzugefügt werden, indem
	ihr im Windows "Explorer" oben links "Ansicht" klickt, und dann oben rechts den Haken bei "Dateinamenerweiterungen" setzt. Jetzt könnt ihr einfach die Datei "installer" 	 in "installer.py" umbenennen.








##################################################################################################################################################################################################################################################################################################################################################################
################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################ONLY FOR DEVELOPERS#########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
TODO:

Beachrichtigungen:

	Text im github repo, welche beim start des saugers runtergeladen/überprüft/(halt iwie)ausgelesen wird und dann bei einem bestimmten ihnhalt
	eine nachricht in chrome als alert anzeigt.

Installer überarbeiten:

	registry suche nach schon vorhandenen saugern und diese deinstallieren
	
	suche nach schon vorhandenen, aber deplatzierten pfadvariablen und löschung derer


Updater überarbeiten:

	Vergleicht eine irgendwo als Text hinterlegte Versionsnummer im "Der Sauger" Ordner, mit einer im repository hinterlegten Versionsnummer und lädt sie dann runter.

	timouts aus bat dateien raushauen

	Updater.py zu einer DATEI ändern, welche wie der host über ein cmd command "python {pfad}" aufgerufen wird um versehentliches updaten zu vermeiden

Uninstaller überarbeiten:

	Vernünftige uninstall bat mit löschung und detektierung aller ffmpeg und youtube-dl Pfadvariablen



Downloads auf ausführung überprüfen: 

	Beim speichercheck (um den erfolgreichen download zu testen) auch ein fileanzahlcheck hinzufügen, da sich die größe des Ordner auch durch parralle downloads verändern kann
	ohne das neue files erstellt werden, was zu einem falsch positiven download-response und damit zu einem nicht dowload führt.



