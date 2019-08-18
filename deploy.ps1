docker build . -t roommatepredictor
docker tag roommatepredictor roommatepredictorcr.azurecr.io/roommatepredictor
az acr login --name roommatepredictorcr
docker push roommatepredictorcr.azurecr.io/roommatepredictor
az container restart --resource-group roommatepredictor-rg --name roommatepredictor-container