# Sentimentanalyse med AWS Comprehend, Lambda og SAM

* Vi i denne oppgaven bruke AWS-tjenesten **Comprehend** til å analysere **sentiment** i tekst, det vil si om teksten uttrykker en positiv, negativ, nøytral eller blandet stemning.
* Dette repoet inneholder er ferdiglaget SAM applikasjon. Vi skal senere lage disse selv. 
* Applikasjonen bygges og deployes med **AWS SAM**, både via GitHub Actions (Senere) og direkte fra ditt Codespaces-miljø.

## Beskrivelse

I øvelsen bruker vi fire sentrale AWS-tjenester:

* **AWS Lambda** – Serverless compute. Kjører en funksjon på forespørsel og stopper når den er ferdig. Du betaler kun for kjøretiden (millisekunder).
* **Amazon API Gateway** – Gir Lambda et HTTP-grensesnitt mot omverdenen. Støtter autentisering, caching, throttling og rate limiting.
* **AWS SAM (Serverless Application Model)** – Verktøy for å definere, bygge og deploye serverless-applikasjoner på en enkel måte.
* **Amazon Comprehend** – Tjeneste for naturlig språkprosessering. I denne øvelsen bruker vi funksjonen for **sentimentanalyse** til å vurdere om en tekst er positiv, negativ, nøytral eller blandet.

## Lag en fork

Du må start med å lage en fork av dette repoet til din egen GitHub konto.

![Alt text](img/fork.png  "a title")

## Lag AWS Credentials 

* Følg veiledningen her for å lage Access Key og Secret Access Key  - https://github.com/glennbechdevops/aws-iam-accesskeys

## Sett Access Key & secret  som CodeSpaces/Repository secrets

<img width="2652" height="1186" alt="image" src="https://github.com/user-attachments/assets/e5eb3cc1-8310-4515-b0f8-54acbd6b2db9" />

* I din fork, velg "settings" og "Secrets and Variables"
* Velg "Coee Spaces" og "New repository secret
* Du skal lage to repository secrets med navn: AWS_ACCESS_KEY_ID og AWS_SECRET_ACCESS_KEY
* Legg inn verdier du fikk oppgitt når du laget nøklene, eller fra filen du lastet ned 

## Start et Codespace & Installer nødvendig programvare 
* Fra din fork av dette repositoryet, starter du CodeSpaces. Keyboard shortcut er "."
* Alternativt, velg den grønne "Code", "Velg Codespaces" og "Create codespace from main"
* Fra ditt mnye CodeSpace - Åpne et **terminalvindu**, og velg "Continue working in GitHub Codespaces"
  
### Installer AWS CLI 

I terminalen kjør følgende kommandoer

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Test at CLI og Akesessnøkler er riktig satt opp ved å kjøre 

```
aws s3 ls
```

### Installer SAM

```
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
````

## Test bygg og lokal utvikling fra CodeSpaces med SAM

* Ta en kikk på koden som ligger i mappen "sentiment demo". Dette er en Lambda som tar imot en HTTP request - og som
sender en tekst videre til tjenesten AWS Comprehend for sentimentanalyse.

Gå til mappen og bygg lambdaen / SAM prosjektet.

```shell
cd sentiment-demo/
sam build --use-container
```

Du kan teste funksjonen uten å deploye den til AWS ved å kjøre kommandoen 

```shell
sam local invoke -e event.json 
```

Event.json filen inneholder en request, nøyaktig slik API Gateway sender den til "handler" metoden/funksjonen. 

Du skal få en respons omtrent som denne, legg merke til at både _Negative_,_Positive_ og _Neutral_ oppgis med probabilitet. 

```
{"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": "{\"sentiment \": \"{\\\"Sentiment\\\": \\\"NEGATIVE\\\", \\\"SentimentScore\\\": {\\\"Positive\\\": 0.00023614335805177689, \\\"Negative\\\": 0.9974453449249268, \\\"Neutral\\\": 0.00039782875683158636, \\\"Mixed\\\": 0.0019206495489925146}, \\\"ResponseMetadata\\\": {\\\"RequestId\\\": \\\"c3367a61-ee05-4071-82d3-e3aed344f9af\\\", \\\"HTTPStatusCode\\\": 200, \\\"HTTPHeaders\\\": {\\\"x-amzn-requestid\\\": \\\"c3367a61-ee05-4071-82d3-e3aed344f9af\\\", \\\"content-type\\\": \\\"application/x-amz-json-1.1\\\", \\\"content-length\\\": \\\"168\\\", \\\"date\\\": \\\"Mon, 18 Apr 2022 12:00:06 GMT\\\"}, \\\"RetryAttempts\\\": 0}}\"}"}END RequestId: d37e4849-b175-4fa6-aa4b-0031af6f41a0
REPORT RequestId: d37e4849-b175-4fa6-aa4b-0031af6f41a0  Init Duration: 0.42 ms  Duration: 1674.95 ms    Billed Duration: 1675 ms        Memory Size: 128 MB     Max Memory Used: 128 MB
```

* Ta en ekstra kikk på event.json. Dette er objektet AWS Lambda får av tjenesten API Gateway .
* Forsøke å endre teksten i "Body" delen av event.json - klarer å å endre sentimentet til positivt ?
  
## Deploy med SAM fra CodeSpaces

* Du kan også bruke SAM til å deploye lambdafunksjonen rett fra CodeSpaces 
* NB! Du må endre Stack name til noe unikt. Legg på ditt navn, for eksempel; ```--stack-name sam-sentiment-ola```

Som dere ser trenger vi IKKE bruke ```--guided``` flagget hvis vi oppgir de nødvendige parameterene på kommando-linjen

```shell
  sam deploy --no-confirm-changeset --no-fail-on-empty-changeset --stack-name sam-sentiment-<dine initialer eller noe>  --resolve-s3 --capabilities CAPABILITY_IAM --region eu-west-1      
 ```

NB. Hvis deploy feiler, av en eller annen årsak. Kan det hende du må gå til tjenesten "CloudFormation" og slette stacken som oppga i deploy-kommandoen. Hvis denne er i en tilstand "ROLLBACK_FAILED" så er det eneste alternativet å slette den.

Når jobben er ferdig, vil du blant annet se hva URL'en til lambdafunksjonen ble. Let etter output som ser slikt ut; 

```text
Key                 SentimentAPI                                                                
Description         API Gateway endpoint URL for Prod stage for Sentiment function              
Value               https://orpbuzoiik.execute-api.us-west-1.amazonaws.com/Prod/sentiment/      
```

Du kan nå bruke postman eller Curl til å teste ut tjenesten. Erstat URL med URL'en til lambdafunksjonen. 

```shell
export URL=<URL fra "Value" i output >
curl -X POST $URL -H 'Content-Type: text/plain'  -H 'cache-control: no-cache' -d 'The laptop would not boot up when I got it.'
```

## Bonus: Gjør APIet mer brukervennlig

* Se på Python-koden og se hvordan lambda-funksjonen er implementert
* APIet er ikke veldig brukervennlig. Koden bare sender responsen fra AWS Comprehend videre til klienten.
* Endre responsen etter eget ønske
  
## Bonusoppgave: Endre lambdaen til å bruke en annen Comprehend-tjeneste

AWS Comprehend har en lang rekke funksjoner utover sentimentanalyse, se på https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
og finn inspirasjon til å endre Lambdafunksjonen så den gjør noe annet en sentimentanalyse

## Bonusoppgave: GitHub Actions

Leg en Github actions workflo som bygger funksjonen ved en push til main branch.

Du må først legge inn Access Key ID og Secret access key i repository'et sitt "Secrets and vatiables" under settings. 
Du har tidligere lagt inn disse under "Codespaces" nå må de legges til under "Acrtions"

* Lag en ny mappe i rotkatalogen til repositoriet du klonet som heter .github/workflows
* Kopier denne koden inn i  ```.github/workflows/``` katalogen, og kall den for eksempel sam-deploy.yml eller noe tilsvarende.
* NB! Bruk samme verdi i "stack name" som i den tidligere `sam deploy` kommandoen  

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

Commit og push denne filen til ditt repositoru.

På git push blir du bedt om brukernavn og passord. Bruk brukernavnet ditt, og Access Token du laget tidligere som passord.

## Sjekk at pipeline virker

* før du kan teste pipeline må du slå på "Actions" for din fork.
* Gå til "actions" i ditt repository i GitHub 

![Alt text](img/enable_actions.png "a title")

* Gjør kodeendringer på main branch i Lambdaen
* Commit & push endringen
* Se at endringene blir deployet av GitHub Actions workflow.
