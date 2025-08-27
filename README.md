# GitHub actions, AWS Lambda med API Gateway og AWS SAM

* I denne øvingen skal vi se på Github actions og hvordan vi kan sette opp en CD pipeline for en AWS Lambdafunksjon. 
Vi skal bruke AWS tjenesten "Comprehend" for å finne "stemningen" (Sentiment) i en tekst- og om den er negativt eller positivt 
ladet. 

* Deployment og bygg skal gjøres med verktøyet "AWS SAM", både i pipeline med GitHub actions, men også fra dit CodeSpaces miljø
## Trouble-shooting 

Du kan oppleve at du går tom for disk i CodeSpaces miljøet når du kjører SAM operasjoner. Du må da fjerne docker images.  

```shell
docker images ls
```

Se etter Image ID, og slett med 

```shell
docker image rm  <Image ID>
```

Slett gjerne all images, og forsøk å kjøre SAM kommandoen på nytt 


## Beskrivelse 

Denne øvingen bruker fire AWS tjenestester 

* AWS LAMBDA - Serverless Compute. Tjenesten kjører en enkelt funksjon og avslutter. Du Betaler for antall millisekunder koden kjører. Du velger språk
* API GATEWAY - Gir AWS Lambda et HTTP grensesnitt ut mot verden.Støtter autentisering, caching, throttling, rate limiting osv.
* AWS SAM - Verktøy for å lage,deploye og vedlikeholde applikasjoner basert på Serverless teknologi
* API COMPREHEND- AWS tjeneste for tekstanalyse. Kan finne ut av om sentimentet eller “stemningen” i en tekst er god eller dårlig.

## Lag en fork

Du må start med å lage en fork av dette repoet til din egen GitHub konto.

![Alt text](img/fork.png  "a title")

## Logg i Cloud 9 miljøet ditt 

![Alt text](img/aws_login.png  "a title")

* URL for innlogging er https://244530008913.signin.aws.amazon.com/console
* Logg på med brukernavn og passord gitt i klassrommet
* Gå til tjenesten CodeSpaces (Du nå søke på CodeSpaces uten mellomrom i søket) 
* Velg "Open IDE" 
* Hvis du ikke ser ditt miljø, kan det hende du har valgt feil region. Hvilken region du skal bruke vil bli oppgitt i klasserommet.

### Lag et Access Token for GitHub

* Når du skal autentisere deg mot din GitHub konto fra Cloud 9 trenger du et access token.  Gå til  https://github.com/settings/tokens og lag et nytt.
* NB. Ta vare på tokenet et sted, du trenger dette senere når du skal gjøre ```git push```

![Alt text](img/generate.png  "a title")

Access token må ha "repo" tillatelser, og "workflow" tillatelser.

![Alt text](img/new_token.png  "a title")

### Lage en klone av din Fork (av dette repoet) inn i ditt Cloud 9 miljø

Fra Terminal i Cloud 9. Klone repository med HTTPS URL. Eksempel ; 

```
git clone https://github.com/≤github bruker>/02-CD-AWS-lamda-sls
```

Får du denne feilmeldingen ```bash: /02-CD-AWS-lamda-sls: Permission denied``` - så glemte du å bytte ut <github bruker> med 
ditt eget Github brukernavn :-) 

![Alt text](img/clone.png  "a title")

OBS Når du gjør ```git push``` senere og du skal autentisere deg, skal du bruke GitHub Access token når du blir bedt om passord, 
så du trenger å ta vare på dette et sted. 

## Konfigurer Git i CodeSpaces 
Følgende steg trenger du bare gjøre en gang i CodeSpaces miljøet ditt. Du kan hoppe over hele steget hvis du har gjort det tidligere. 
For å slippe å autentisere seg hele tiden kan man få git til å cache nøkler i et valgfritt antall sekunder på denne måten.
 
```shell
git config --global credential.helper "cache --timeout=86400"
```

Konfigurer også brukernavnet og eposten din for GitHub CLI. Da slipepr du advarsler i terminalen
når du gjør commit senere.

````shell
git config --global user.name <github brukernavn>
git config --global user.email <email for github bruker>

````

## Test bygg og lokal utvikling fra Cloud 9 med SAM

I cloud 9, åpne en Terminal

```shell
cd 02-CD-AWS-lamda-sls
cd sentiment-demo/
sam build --use-container
```

## Test 

Du kan teste funksjonen uten å deploye den til AWS ved å kjøre kommandoen 

```shell
sam local invoke -e event.json 
```

Event.json filen inneholder en request, nøyaktig slik API Gateway sender den til "handler" metoden/funksjonen. 

Du skal få en respons omtrent som denne 
```
{"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": "{\"sentiment \": \"{\\\"Sentiment\\\": \\\"NEGATIVE\\\", \\\"SentimentScore\\\": {\\\"Positive\\\": 0.00023614335805177689, \\\"Negative\\\": 0.9974453449249268, \\\"Neutral\\\": 0.00039782875683158636, \\\"Mixed\\\": 0.0019206495489925146}, \\\"ResponseMetadata\\\": {\\\"RequestId\\\": \\\"c3367a61-ee05-4071-82d3-e3aed344f9af\\\", \\\"HTTPStatusCode\\\": 200, \\\"HTTPHeaders\\\": {\\\"x-amzn-requestid\\\": \\\"c3367a61-ee05-4071-82d3-e3aed344f9af\\\", \\\"content-type\\\": \\\"application/x-amz-json-1.1\\\", \\\"content-length\\\": \\\"168\\\", \\\"date\\\": \\\"Mon, 18 Apr 2022 12:00:06 GMT\\\"}, \\\"RetryAttempts\\\": 0}}\"}"}END RequestId: d37e4849-b175-4fa6-aa4b-0031af6f41a0
REPORT RequestId: d37e4849-b175-4fa6-aa4b-0031af6f41a0  Init Duration: 0.42 ms  Duration: 1674.95 ms    Billed Duration: 1675 ms        Memory Size: 128 MB     Max Memory Used: 128 MB
```

* Ta en ekstra kikk på event.json. Dette er objektet AWS Lambda får av tjenesten API Gateway .
* Forsøke å endre teksten i "Body" delen av event.json - klarer å å endre sentimentet til positivt ?

## Deploy med SAM fra Cloud 9

* Du kan også bruke SAM til å deploye lambdafunksjonen rett fra Cloud 9 
* NB! Du må endre Stack name til noe unikt. Legg på ditt brukeranvn eller noe i slutten av navnet, for eksempel; ```--stack-name sam-sentiment-ola```

Som du ser under, trenger vi IKKE bruke ```--guided``` flagget hvis vi oppgir de nødvendige parameterene på kommando-linjen

```shell
  sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-sentiment-<dine initialer eller noe>  --capabilities CAPABILITY_IAM --region eu-west-1      
 ```

Når jobben er ferdig, vil du blant annet se hva URL'en til lambdafunksjonen ble. Let etter output som ser slikt ut; 

```text
Key                 SentimentAPI                                                                
Description         API Gateway endpoint URL for Prod stage for Sentiment function              
Value               https://orpbuzoiik.execute-api.us-west-1.amazonaws.com/Prod/sentiment/      
```

Du kan deretter bruke postman eller Curl til å teste ut tjenesten. Erstat URL med URL'en til lambdafunksjonen. Dere finner denne
etter dete har gjort deploy 

```shell
export URL=<URL du fikk vite ved deploy>
curl -X POST $URL -H 'Content-Type: text/plain'  -H 'cache-control: no-cache' -d 'The laptop would not boot up when I got it.'
```

Men... dette er jo ikke veldig "DevOps" og vil ikke fungere i et større team. Vi trenger både CI og CD for å kunne jobbe 
effektivt sammen om denne funksjonen.

## GitHub Actions

Vi skal nå lage en workflow eller pipeline som ved hver eneste commit til main branch i github bygger og deployer 
en ny version av lambdafunksjonen.

* NB! For å få se filer som er "skjulte" i AWS CodeSpaces må du velge "show hidden files" i fil-utforskeren.
  (trykk på "tannhjulet")
* 
![Alt text](img/hiddenfiles.png  "a title")

* Lag en ny mappe i rotkatalogen til repositoriet du klonet som heter .github/workflows
* Kopier denne koden inn i  ```.github/workflows/``` katalogen, og kall den for eksempel sam-deploy.yml eller noe tilsvarende. Du må endre parameter ```--stack-name``` i  ```sam deploy``` kommandoen. 
* Bruk samme stack navn som du brukte når du deployet direkte fra cloud 9.

```yaml
on:
  push:
    branches:
      - main

defaults:
  run:
    working-directory: ./sentiment-demo

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - uses: aws-actions/setup-sam@v1
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-1
      - run: sam build --use-container
      - run: sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-sentiment-<studentid>  --s3-bucket lambda-bucket-grb  --capabilities CAPABILITY_IAM --region eu-west-1
```

For å pushe endringen til ditt repo må du stå i riktig katalog i CodeSpaces terminalen 
```bash
cd ~/environment/02-CD-AWS-lamda-sls
git add .github/
git commit -m"added workflow file" 
git push 
```

På git push blir du bedt om brukernavn og passord. Bruk brukernavnet ditt, og Access Token du laget tidligere som passord.

## Hemmeligheter

GitHub actions trenger våre API nøkler for å kunne deploye kode i AWS på våre vegne. 

![Alt text](img/topsecret.png  "a title")

Vi skal _absolutt ikke_ sjekke inn API nøkler og hemmeligheter inn i koden. GitHub har heldigvis en mekanisme for å lagre hemmeligheter utenfor koden. 
* I Repository settings og under menyvalget "secrets" og "Action secrets"  kan vi legge inn verdier og bruke de fra workflowene våre ved å referere de ved navn for eksempel på denne måten
``` aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}```

Lag to repository secrets. 

* AWS_ACCESS_KEY_ID 
* AWS_SECRET_ACCESS_KEY

* Du må gå til tjenesten IAM i AWS og fine din egen IAM bruker. 
* Velg "Security credentials" tabben
* Velg "Create Access Key"
* Ta vare på verdiene, last de gjerne ned som en fil

## Sjekk at pipeline virker

* før du kan teste pipeline må du slå på "Actions" for din fork.
* Gå til "actions" i ditt repository i GitHub 

![Alt text](img/enable_actions.png "a title")

* Gjør kodeendringer på main branch i Lambdaen
* Commit & push endringen
* Se at endringene blir deployet av GitHub Actions workflow.
* Hvis jobben har feilet tidligere på grunn av manglende secrets, og du har lagt de inn kan du velge din workflow, og så trykke knappen "re-run all jobs" i GitHub Actions UI.
* 

![Alt text](img/finished.png  "a title")

* Test lambdafunksjonen med feks Curl (eller Postman om du har) 
```shell
export URL=<Hvordan finner du URL? Det er flere måter.....>
curl -X POST $URL -H 'Content-Type: text/plain' -H 'cache-control: no-cache' -d 'The laptop would not boot up'
```

## Bonusoppgave 

* Du kan lage en applikasjon fra scratch ved å bruke "sam init" - forsøk gjerne å lage en ny sam app. Dt kan være lurt å velge Python eller Javascript som språk, siden disse er tolkede språk og ikke trenger  kompilering
