# Rhasspy-Timer-Skill (Rhasspy-Hermes-App)
Simple stupid (german) timer skill.

Feel free to add the TimerObject to a list, so you can set up multiple timers. At the moment there is only one possible.

## Usage
`sudo sh setupAService.sh` to install it as a background service
`sh logs.sh` to show the logs of the service
`sudo sh reload.sh` to reload the service, if you changed some code

You may need to install Rhasspy-Hermes-App and paho-mqtt. On Debian Bullseye you might run into an error with the Rhasspy-Hermes-App, it can be fixed by upgrading rhasspy-hermes to at least version 0.6.2.

## Example Sentences

[Timerjob:start]

(stell|stelle|starte) einen timer auf (0..59) {seconds} Sekunden

(stell|stelle|starte) einen timer auf (0..59) {minutes} (Minuten|Minute)

(stell|stelle|starte) einen timer auf (0..59) {hours} (Stunde|Stunden)

(stell|stelle|starte) einen timer auf (0..59) {hours} (Stunde|Stunden) und (0..59) {minutes} Minuten

(stell|stelle|starte) einen timer auf (0..59) {hours} (Stunde|Stunden) und (0..59) {seconds} Sekunden

(stell|stelle|starte) einen timer auf (0..59) {minutes} (Minuten|Minute) und (0..59) {seconds} Sekunden

[Timerjob:remaining]

Wie lange (läuft|geht) der Timer noch

Wie viel Zeit verbleibt [beim timer] noch [beim timer]

[Timerjob:stop]

(Beende|Stoppe|Lösche) den Timer
